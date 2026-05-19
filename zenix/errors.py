# -*- coding: utf-8 -*-
"""zenix errors."""


class ZenixError(Exception):
    """Base exception for Zenix."""


class ZenixValidationError(ZenixError, ValueError):
    """Raised for invalid input parameters."""
