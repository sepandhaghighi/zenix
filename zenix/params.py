# -*- coding: utf-8 -*-
"""zenix params."""
from enum import Enum

ZENIX_VERSION = "0.2"


class NoiseType(Enum):
    """Noise type enum."""

    WHITE = "white"
    PINK = "pink"
    BROWN = "brown"


DEFAULT_SAMPLE_RATE = 44100
DEFAULT_DURATION = 30.0
DEFAULT_VOLUME = 0.3
DEFAULT_FADE_IN = 2.0

INVALID_NOISE_TYPE_ERROR = "`noise_type` must be an instance of NoiseType."

INVALID_DURATION_TYPE_ERROR = "`duration` must be int or float."
INVALID_DURATION_VALUE_ERROR = "`duration` must be greater than 0."

INVALID_SAMPLE_RATE_TYPE_ERROR = "`sample_rate` must be int."
INVALID_SAMPLE_RATE_VALUE_ERROR = "`sample_rate` must be greater than 0."

INVALID_VOLUME_TYPE_ERROR = "`volume` must be int or float."
INVALID_VOLUME_RANGE_ERROR = "`volume` must be between 0.0 and 1.0."

INVALID_FADE_IN_TYPE_ERROR = "`fade_in` must be int or float."
INVALID_FADE_IN_VALUE_ERROR = "`fade_in` must be greater than or equal to 0."
INVALID_FADE_IN_RANGE_ERROR = "`fade_in` must not exceed `duration`."
