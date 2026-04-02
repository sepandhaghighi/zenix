# -*- coding: utf-8 -*-
"""zenix cli."""

import argparse
import os
import sys
from .params import DEFAULT_SAMPLE_RATE, DEFAULT_DURATION
from .params import DEFAULT_VOLUME, DEFAULT_FADE_IN
from .params import ZENIX_VERSION, NoiseType
from .functions import generate_noise, play_noise


def _parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments.

    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Developer-focused procedural noise generator."
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Version",
    )

    parser.add_argument(
        "-t", "--type",
        choices=[x.value for x in NoiseType],
        default="white",
        help="Noise type"
    )

    parser.add_argument(
        "-d", "--duration",
        type=float,
        default=DEFAULT_DURATION,
        help="Duration in seconds"
    )

    parser.add_argument(
        "-v", "--volume",
        type=float,
        default=DEFAULT_VOLUME,
        help="Volume 0.0 - 1.0"
    )

    parser.add_argument(
        "--fade-in",
        type=float,
        default=DEFAULT_FADE_IN,
        help="Fade-in duration in seconds"
    )

    parser.add_argument(
        "--loop",
        action="store_true",
        help="Loop playback"
    )

    return parser.parse_args()


def _run(args: argparse.Namespace) -> None:
    """
    Run zenix.

    args: arguments
    """
    if args.version:
        print(ZENIX_VERSION)
        return
    if not 0.0 <= args.volume <= 1.0:
        print("Volume must be between 0 and 1.")
        sys.exit(1)

    print(f"Playing {args.type} noise...\nPress Ctrl+C to stop.")

    audio = generate_noise(
        noise_type=NoiseType(args.type),
        duration=args.duration,
        sample_rate=DEFAULT_SAMPLE_RATE,
        volume=args.volume,
        fade_in=args.fade_in,
    )

    play_noise(
        audio=audio,
        sample_rate=DEFAULT_SAMPLE_RATE,
        loop=args.loop
    )


def main() -> None:
    """CLI entry point."""
    args = _parse_args()
    _run(args)
