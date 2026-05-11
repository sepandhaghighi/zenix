# -*- coding: utf-8 -*-
"""zenix params."""
from enum import Enum

ZENIX_VERSION = "0.5"


class NoiseType(Enum):
    """Noise type enum."""

    WHITE = "white"
    PINK = "pink"
    BROWN = "brown"


DEFAULT_SAMPLE_RATE = 44100
DEFAULT_DURATION = 30.0
DEFAULT_VOLUME = 0.3
DEFAULT_FADE_IN = 2.0
DEFAULT_FADE_OUT = 2.0

INVALID_NOISE_TYPE_ERROR = "`noise_type` must be an instance of NoiseType."

INVALID_DURATION_ERROR = "`duration` must be a number greater than 0."

INVALID_SAMPLE_RATE_ERROR = "`sample_rate` must be a positive integer."

INVALID_VOLUME_ERROR = "`volume` must be a number between 0.0 and 1.0."

INVALID_FADE_IN_ERROR = "`fade_in` must be a non-negative number not exceeding `duration`."

INVALID_FADE_OUT_ERROR = "`fade_out` must be a non-negative number not exceeding `duration`."

INVALID_AUDIO_ERROR = "`audio` must be a non-empty 1D numpy.ndarray with dtype int16."

INVALID_LOOP_TYPE_ERROR = "`loop` must be bool."

INVALID_FILEPATH_ERROR = "`filepath` must be a non-empty string."
