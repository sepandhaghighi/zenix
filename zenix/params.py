# -*- coding: utf-8 -*-
"""zenix params."""
from enum import Enum

ZENIX_VERSION = "1.0"

ZENIX_REPO = "https://github.com/sepandhaghighi/zenix"

OVERVIEW = """Zenix is a lightweight tool for generating procedural noise such as white, pink, and brown noise.
It can be used both as a command-line application and as a Python library, making it suitable for quick terminal
usage as well as integration into Python projects. Zenix generates noise programmatically using NumPy and plays it
through an audio backend, allowing developers to create continuous background sound for focus, concentration, relaxation, or acoustic masking.
With support for multiple noise types, configurable parameters, fade-in effects, and looping playback, Zenix provides a simple yet flexible way
to work with procedural noise in both interactive and programmatic environments.
"""


class NoiseType(Enum):
    """Noise type enum."""

    WHITE = "white"
    PINK = "pink"
    BROWN = "brown"
    BLUE = "blue"
    VIOLET = "violet"


class FadeType(Enum):
    """Fade curve type."""

    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    COSINE = "cosine"


DEFAULT_SEED = None
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

INVALID_SEED_ERROR = "`seed` must be a non-negative integer or None."

INVALID_FADE_TYPE_ERROR = "`fade_type` must be an instance of FadeType."

EXIT_MESSAGE = "See you. Bye!"
