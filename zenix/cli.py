# -*- coding: utf-8 -*-
"""zenix cli."""

import argparse

def _parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments.

    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Developer-focused procedural noise generator."
    )

    parser.add_argument(
        "-t", "--type",
        choices=["white", "pink", "brown"],
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