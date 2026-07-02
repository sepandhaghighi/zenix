# -*- coding: utf-8 -*-
"""zenix functions."""

import os
import wave
import tempfile
from typing import Any, Optional
import numpy as np
from nava import play
from .errors import ZenixValidationError
from .params import DEFAULT_SAMPLE_RATE, DEFAULT_DURATION
from .params import DEFAULT_VOLUME, DEFAULT_FADE_IN, DEFAULT_FADE_OUT
from .params import NoiseType
from .params import INVALID_NOISE_TYPE_ERROR
from .params import INVALID_DURATION_ERROR
from .params import INVALID_SAMPLE_RATE_ERROR
from .params import INVALID_VOLUME_ERROR
from .params import INVALID_FADE_IN_ERROR
from .params import INVALID_FADE_OUT_ERROR
from .params import INVALID_AUDIO_ERROR
from .params import INVALID_LOOP_TYPE_ERROR, INVALID_FILEPATH_ERROR
from .params import DEFAULT_SEED, INVALID_SEED_ERROR


def _validate_audio_buffer(
    audio: Any,
    sample_rate: Any,
) -> None:
    """
    Validate PCM int16 mono audio buffer.

    :param audio: PCM int16 numpy array
    :param sample_rate: Sample rate in Hz
    """
    if not isinstance(audio, np.ndarray):
        raise ZenixValidationError(INVALID_AUDIO_ERROR)

    if audio.dtype != np.int16:
        raise ZenixValidationError(INVALID_AUDIO_ERROR)

    if audio.ndim != 1:
        raise ZenixValidationError(INVALID_AUDIO_ERROR)

    if len(audio) == 0:
        raise ZenixValidationError(INVALID_AUDIO_ERROR)

    if not isinstance(sample_rate, int):
        raise ZenixValidationError(INVALID_SAMPLE_RATE_ERROR)

    if sample_rate <= 0:
        raise ZenixValidationError(INVALID_SAMPLE_RATE_ERROR)


def _validate_save_noise(
    filepath: Any,
    audio: Any,
    sample_rate: Any,
) -> None:
    """
    Validate save_noise inputs.

    :param filepath: Output file path
    :param audio: PCM int16 numpy array
    :param sample_rate: Sample rate in Hz
    """
    _validate_audio_buffer(audio=audio, sample_rate=sample_rate)
    if not isinstance(filepath, str) or not filepath:
        raise ZenixValidationError(INVALID_FILEPATH_ERROR)


def _validate_generate_noise(
    noise_type: Any,
    duration: Any,
    sample_rate: Any,
    volume: Any,
    fade_in: Any,
    fade_out: Any,
    seed: Any,
) -> None:
    """
    Validate generate_noise inputs.

    :param noise_type: Noise type (NoiseType)
    :param duration: Duration in seconds
    :param sample_rate: Sample rate in Hz
    :param volume: Volume (0.0 - 1.0)
    :param fade_in: Fade-in duration in seconds
    :param fade_out: Fade-out duration in seconds
    :param seed: Seed
    """
    if not isinstance(noise_type, NoiseType):
        raise ZenixValidationError(INVALID_NOISE_TYPE_ERROR)

    if not isinstance(duration, (int, float)):
        raise ZenixValidationError(INVALID_DURATION_ERROR)

    if duration <= 0:
        raise ZenixValidationError(INVALID_DURATION_ERROR)

    if not isinstance(sample_rate, int):
        raise ZenixValidationError(INVALID_SAMPLE_RATE_ERROR)

    if sample_rate <= 0:
        raise ZenixValidationError(INVALID_SAMPLE_RATE_ERROR)

    if not isinstance(volume, (int, float)):
        raise ZenixValidationError(INVALID_VOLUME_ERROR)

    if not (0.0 <= volume <= 1.0):
        raise ZenixValidationError(INVALID_VOLUME_ERROR)

    if not isinstance(fade_in, (int, float)):
        raise ZenixValidationError(INVALID_FADE_IN_ERROR)

    if fade_in < 0:
        raise ZenixValidationError(INVALID_FADE_IN_ERROR)

    if fade_in > duration:
        raise ZenixValidationError(INVALID_FADE_IN_ERROR)

    if not isinstance(fade_out, (int, float)):
        raise ZenixValidationError(INVALID_FADE_OUT_ERROR)

    if fade_out < 0:
        raise ZenixValidationError(INVALID_FADE_OUT_ERROR)

    if fade_out > duration:
        raise ZenixValidationError(INVALID_FADE_OUT_ERROR)
    
    if seed is not None:
        if not isinstance(seed, int):
            raise ZenixValidationError(INVALID_SEED_ERROR)
        if seed < 0:
            raise ZenixValidationError(INVALID_SEED_ERROR)


def _validate_play_noise(
    audio: Any,
    sample_rate: Any,
    loop: Any,
) -> None:
    """
    Validate play_noise inputs.

    :param audio: PCM int16 numpy array
    :param sample_rate: Sample rate in Hz
    :param loop: Loop flag
    """
    _validate_audio_buffer(audio=audio, sample_rate=sample_rate)
    if not isinstance(loop, bool):
        raise ZenixValidationError(INVALID_LOOP_TYPE_ERROR)


def _generate_white_noise(samples: int) -> np.ndarray:
    """
    Generate white noise.

    :param samples: Number of samples
    """
    return np.random.normal(0, 1, samples).astype(np.float32)


def _generate_pink_noise(samples: int) -> np.ndarray:
    """
    Generate pink noise using Voss-McCartney algorithm approximation.

    :param samples: Number of samples
    """
    rows = 16
    array = np.random.randn(rows, samples)
    array = np.cumsum(array, axis=1)
    pink = np.sum(array, axis=0)
    return pink.astype(np.float32)


def _generate_brown_noise(samples: int) -> np.ndarray:
    """
    Generate brown (Brownian) noise.

    :param samples: Number of samples
    """
    white = np.random.normal(0, 1, samples)
    brown = np.cumsum(white)
    return brown.astype(np.float32)


def _generate_blue_noise(samples: int) -> np.ndarray:
    """
    Generate blue noise.

    :param samples: Number of samples
    """
    white = np.random.normal(0, 1, samples + 1)
    blue = np.diff(white)
    return blue.astype(np.float32)


def _apply_fade_in(audio: np.ndarray, sample_rate: int, fade_duration: float) -> None:
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


def _apply_fade_out(audio: np.ndarray, sample_rate: int, fade_duration: float) -> None:
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


def _normalize(audio: np.ndarray) -> np.ndarray:
    """
    Normalize audio signal.

    :param audio: Input audio
    """
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
    return audio


NOISE_GENERATORS = {
    NoiseType.WHITE: _generate_white_noise,
    NoiseType.PINK: _generate_pink_noise,
    NoiseType.BROWN: _generate_brown_noise,
    NoiseType.BLUE: _generate_blue_noise,
}

def generate_noise(
    noise_type: NoiseType = NoiseType.WHITE,
    duration: float = DEFAULT_DURATION,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    volume: float = DEFAULT_VOLUME,
    fade_in: float = DEFAULT_FADE_IN,
    fade_out: float = DEFAULT_FADE_OUT,
    seed: Optional[int] = DEFAULT_SEED
) -> np.ndarray:
    """
    Generate selected noise type with fade-in and smoothing.

    :param noise_type: white | pink | brown | blue
    :param duration: Duration in seconds
    :param sample_rate: Sample rate
    :param volume: Volume multiplier
    :param fade_in: Fade-in duration in seconds
    :param fade_out: Fade-out duration in seconds
    :param seed: Seed
    """
    _validate_generate_noise(
        noise_type=noise_type,
        duration=duration,
        sample_rate=sample_rate,
        volume=volume,
        fade_in=fade_in,
        fade_out=fade_out,
        seed=seed)

    samples = int(duration * sample_rate)

    if seed is not None:
        np.random.seed(seed)

    audio = NOISE_GENERATORS[noise_type](samples)

    audio = _normalize(audio)

    _apply_fade_in(audio, sample_rate, fade_in)

    _apply_fade_out(audio, sample_rate, fade_out)

    audio *= volume

    return (audio * 32767).astype(np.int16)


def _write_wav(filepath: str, audio: np.ndarray, sample_rate: int) -> None:
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


def play_noise(audio: np.ndarray, sample_rate: int = DEFAULT_SAMPLE_RATE, loop: bool = False) -> None:
    """
    Play noise.

    :param audio: PCM int16 array
    :param sample_rate: Sample rate
    :param loop: Loop flag
    """
    _validate_play_noise(audio=audio, sample_rate=sample_rate, loop=loop)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        filepath = tmp.name
    try:
        _write_wav(filepath, audio, sample_rate)
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


def save_noise(
    filepath: str,
    audio: np.ndarray,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> None:
    """
    Save noise to WAV file.

    :param filepath: Output file path
    :param audio: PCM int16 array
    :param sample_rate: Sample rate
    """
    _validate_save_noise(filepath=filepath, audio=audio, sample_rate=sample_rate)
    _write_wav(filepath, audio, sample_rate)
