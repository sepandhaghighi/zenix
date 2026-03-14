# -*- coding: utf-8 -*-
"""zenix modules."""
from .params import ZENIX_VERSION, NoiseType
from .function import generate_noise, play_noise
__version__ = ZENIX_VERSION

__all__ = ["NoiseType", "generate_noise", "play_noise"]
