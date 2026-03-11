# -*- coding: utf-8 -*-
"""zenix cli."""

import argparse
import tempfile
import os
from .functions import write_wav, generate_noise


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

def _run(args: argparse.Namespace) -> None:
    """
    Run zenix.

    args: arguments
    """
    if not 0.0 <= args.volume <= 1.0:
        print("Volume must be between 0 and 1.")
        sys.exit(1)

    print(f"Playing {args.type} noise... Press Ctrl+C to stop.")

    audio = generate_noise(
        noise_type=args.type,
        duration=args.duration,
        sample_rate=DEFAULT_SAMPLE_RATE,
        volume=args.volume,
        fade_in=args.fade_in,
    )

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = tmp.name

    try:
        write_wav(temp_path, audio, DEFAULT_SAMPLE_RATE)

        if args.loop:
            while True:
                play(temp_path)
        else:
            play(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def main() -> None:
    """
    CLI entry point.
    """
    args = _parse_args()
    _run(args)

    