# -*- coding: utf-8 -*-
"""zenix functions."""

import os
import wave
from typing import Literal
import numpy as np
from nava import play
from .params import NoiseType


def generate_white_noise(samples: int) -> np.ndarray:
    """
    Generate white noise.

    :param samples: Number of samples
    :return: Float32 numpy array
    """
    return np.random.normal(0, 1, samples).astype(np.float32)


def generate_pink_noise(samples: int) -> np.ndarray:
    """
    Generate pink noise using Voss-McCartney algorithm approximation.

    :param samples: Number of samples
    :return: Float32 numpy array
    """
    rows = 16
    array = np.random.randn(rows, samples)
    array = np.cumsum(array, axis=1)
    pink = np.sum(array, axis=0)
    return pink.astype(np.float32)


def generate_brown_noise(samples: int) -> np.ndarray:
    """
    Generate brown (Brownian) noise.

    :param samples: Number of samples
    :return: Float32 numpy array
    """
    white = np.random.normal(0, 1, samples)
    brown = np.cumsum(white)
    return brown.astype(np.float32)


def apply_fade_in(audio: np.ndarray, sample_rate: int, fade_duration: float) -> None:
    """
    Apply linear fade-in to audio in-place.

    :param audio: Audio array
    :param sample_rate: Sample rate
    :param fade_duration: Fade duration in seconds
    """
    fade_samples = int(sample_rate * fade_duration)
    fade_samples = min(fade_samples, len(audio))
    fade_curve = np.linspace(0.0, 1.0, fade_samples)
    audio[:fade_samples] *= fade_curve


def apply_fade_out(audio: np.ndarray, sample_rate: int, fade_duration: float) -> None:
    """
    Apply linear fade-out to audio in-place.

    :param audio: Audio array
    :param sample_rate: Sample rate
    :param fade_duration: Fade duration in seconds
    """
    fade_samples = int(sample_rate * fade_duration)
    fade_samples = min(fade_samples, len(audio))
    fade_curve = np.linspace(1.0, 0.0, fade_samples)
    audio[-fade_samples:] *= fade_curve


def normalize(audio: np.ndarray) -> np.ndarray:
    """
    Normalize audio signal.

    :param audio: Input audio
    :return: Normalized audio
    """
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
    return audio


def generate_noise(
    noise_type: NoiseType = NoiseType.WHITE,
    duration: float = DEFAULT_DURATION,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    volume: float = DEFAULT_VOLUME,
    fade_in: float = DEFAULT_FADE_IN
) -> np.ndarray:
    """
    Generate selected noise type with fade-in and smoothing.

    :param noise_type: white | pink | brown
    :param duration: Duration in seconds
    :param sample_rate: Sample rate
    :param volume: Volume multiplier
    :param fade_in: Fade-in duration in seconds
    :return: PCM int16 array
    """
    samples = int(duration * sample_rate)

    if noise_type == NoiseType.WHITE:
        audio = generate_white_noise(samples)
    elif noise_type == NoiseType.PINK:
        audio = generate_pink_noise(samples)
    elif noise_type == NoiseType.BROWN:
        audio = generate_brown_noise(samples)
    else:
        raise ValueError("Unsupported noise type")

    audio = normalize(audio)

    apply_fade_in(audio, sample_rate, fade_in)

    apply_fade_out(audio, sample_rate, 1.0)

    audio *= volume

    return (audio * 32767).astype(np.int16)


def write_wav(filepath: str, audio: np.ndarray, sample_rate: int) -> None:
    """
    Write PCM audio to WAV file.

    :param filepath: Target file path
    :param audio: PCM int16 array
    :param sample_rate: Sample rate
    """
    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())


def play_noise(audio: np.ndarray, sample_rate: int, loop: bool) -> None:
    """
    Play noise.

    :param audio: PCM int16 array
    :param sample_rate: Sample rate
    :param loop: Loop flag
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        filepath = tmp.name
    try:
        write_wav(filepath, audio, sample_rate)
        if loop:
            try:
                while True:
                    play(filepath)
            except KeyboardInterrupt:
                pass
        else:
            play(filepath)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
