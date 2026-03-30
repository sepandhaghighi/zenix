# -*- coding: utf-8 -*-
"""zenix params."""
from enum import Enum

ZENIX_VERSION = "0.1"


class NoiseType(Enum):
    """Noise type enum."""

    WHITE = "white"
    PINK = "pink"
    BROWN = "brown"


DEFAULT_SAMPLE_RATE = 44100
DEFAULT_DURATION = 30.0
DEFAULT_VOLUME = 0.3
DEFAULT_FADE_IN = 2.0
