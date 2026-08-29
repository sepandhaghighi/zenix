# -*- coding: utf-8 -*-
"""zenix noise."""

import numpy as np
from typing import Optional
from .params import DEFAULT_SAMPLE_RATE, DEFAULT_DURATION
from .params import DEFAULT_VOLUME, DEFAULT_FADE_IN, DEFAULT_FADE_OUT
from .params import DEFAULT_SEED
from .params import NoiseType, FadeType

from .functions import generate_noise
from .functions import play_noise
from .functions import save_noise
from .functions import _validate_generate_noise


class Noise:
    """Noise object."""

    def __init__(
        self,
        noise_type: NoiseType = NoiseType.WHITE,
        duration: float = DEFAULT_DURATION,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        volume: float = DEFAULT_VOLUME,
        fade_in: float = DEFAULT_FADE_IN,
        fade_out: float = DEFAULT_FADE_OUT,
        fade_type: FadeType = FadeType.LINEAR,
        seed: Optional[int] = DEFAULT_SEED
    ) -> None:
        """
        Initialize noise object.

        :param noise_type: Noise type
        :param duration: Duration in seconds
        :param sample_rate: Sample rate in Hz
        :param volume: Volume multiplier
        :param fade_in: Fade-in duration in seconds
        :param fade_out: Fade-out duration in seconds
        :param fade_type: Fade type
        :param seed: Random seed for reproducible noise
        """
        _validate_generate_noise(
            noise_type=noise_type,
            duration=duration,
            sample_rate=sample_rate,
            volume=volume,
            fade_in=fade_in,
            fade_out=fade_out,
            fade_type=fade_type,
            seed=seed
        )

        self._noise_type = noise_type
        self._duration = duration
        self._sample_rate = sample_rate
        self._volume = volume
        self._fade_in = fade_in
        self._fade_out = fade_out
        self._fade_type = fade_type
        self._seed = seed
        self._audio = None

    def __repr__(self) -> str:
        """
        Return object representation.

        :return: String representation
        """
        return (
            f"Noise("
            f"noise_type={self.noise_type.value!r}, "
            f"duration={self.duration}, "
            f"sample_rate={self.sample_rate}, "
            f"volume={self.volume}, "
            f"fade_in={self.fade_in}, "
            f"fade_out={self.fade_out}, "
            f"fade_type={self.fade_type.value!r}, "
            f"seed={self.seed})"
        )

    @property
    def noise_type(self) -> NoiseType:
        """
        Return noise type.

        :return: Noise type
        """
        return self._noise_type

    @property
    def duration(self) -> float:
        """
        Return duration.

        :return: Duration in seconds
        """
        return self._duration

    @property
    def sample_rate(self) -> int:
        """
        Return sample rate.

        :return: Sample rate in Hz
        """
        return self._sample_rate

    @property
    def volume(self) -> float:
        """
        Return volume.

        :return: Volume multiplier
        """
        return self._volume

    @property
    def fade_in(self) -> float:
        """
        Return fade-in duration.

        :return: Fade-in duration in seconds
        """
        return self._fade_in

    @property
    def fade_out(self) -> float:
        """
        Return fade-out duration.

        :return: Fade-out duration in seconds
        """
        return self._fade_out
    
    @property
    def fade_type(self) -> FadeType:
        """
        Return fade type.

        :return: Fade type
        """
        return self._fade_type

    @property
    def audio(self) -> np.ndarray:
        """
        Return generated audio buffer.

        Audio will be generated automatically on first access.

        :return: PCM int16 audio array
        """
        if self._audio is None:
            self.generate()
        return self._audio

    @property
    def seed(self) -> Optional[int]:
        """
        Return seed.

        :return: Random seed for reproducible noise
        """
        return self._seed

    def generate(self) -> np.ndarray:
        """
        Generate noise audio.

        :return: PCM int16 audio array
        """
        self._audio = generate_noise(
            noise_type=self.noise_type,
            duration=self.duration,
            sample_rate=self.sample_rate,
            volume=self.volume,
            fade_in=self.fade_in,
            fade_out=self.fade_out,
            fade_type=self.fade_type,
            seed=self.seed
        )
        return self._audio

    def play(self, loop: bool = False) -> None:
        """
        Play generated noise.

        :param loop: Loop playback
        """
        play_noise(
            audio=self.audio,
            sample_rate=self.sample_rate,
            loop=loop
        )

    def save(self, filepath: str) -> None:
        """
        Save generated noise to WAV file.

        :param filepath: Output file path
        """
        save_noise(
            filepath=filepath,
            audio=self.audio,
            sample_rate=self.sample_rate
        )
