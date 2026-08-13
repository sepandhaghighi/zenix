# -*- coding: utf-8 -*-
"""zenix cli."""

import argparse
import sys
from .params import DEFAULT_SAMPLE_RATE, DEFAULT_DURATION
from .params import DEFAULT_VOLUME, DEFAULT_FADE_IN, DEFAULT_FADE_OUT
from .params import ZENIX_VERSION, NoiseType, EXIT_MESSAGE
from .errors import ZenixError
from .functions import generate_noise, play_noise, save_noise


def _print_cli_error(message: str, exit_code: int = 1) -> None:
    """
    Print a formatted CLI error message and exit.

    :param message: Error message to display.
    :param exit_code: Exit status code (default: 1).
    """
    print(f"[ZENIX ERROR] {message}", file=sys.stderr)
    sys.exit(exit_code)


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
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
        "--fade-out",
        type=float,
        default=DEFAULT_FADE_OUT,
        help="Fade-out duration in seconds"
    )

    parser.add_argument(
        "--sample-rate",
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        help="Audio sample rate in Hz"
    )

    parser.add_argument(
        "--loop",
        action="store_true",
        help="Loop playback"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Save noise to WAV file"
    )

    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible noise"
    )

    return parser.parse_args()


def _run(args: argparse.Namespace) -> None:
    """
    Run zenix.

    :param args: arguments
    """
    if args.version:
        print(ZENIX_VERSION)
        return
    try:
        audio = generate_noise(
            noise_type=NoiseType(args.type),
            duration=args.duration,
            sample_rate=args.sample_rate,
            volume=args.volume,
            fade_in=args.fade_in,
            fade_out=args.fade_out,
            seed=args.seed
        )
        if args.output:
            print(f"Saving {args.type} noise to {args.output}...")
            save_noise(
                filepath=args.output,
                audio=audio,
                sample_rate=args.sample_rate
            )
        print(f"Playing {args.type} noise...\nPress Ctrl+C to stop.")
        play_noise(
            audio=audio,
            sample_rate=args.sample_rate,
            loop=args.loop
        )
    except (KeyboardInterrupt, EOFError):
        print(EXIT_MESSAGE)
        sys.exit(130)
    except ZenixError as e:
        _print_cli_error(str(e))
    except Exception as e:
        _print_cli_error(f"Unexpected error: {e}")


def main() -> None:
    """CLI entry point."""
    args = _parse_args()
    _run(args)
