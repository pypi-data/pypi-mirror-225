#!/usr/bin/env python3

"""monitorio command line interface
"""

from argparse import ArgumentParser
from argparse import Namespace as Args
from pathlib import Path

import chime  # type: ignore[import]

from monitorio.server import Context, serve


def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = ArgumentParser()
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["ALL_DEBUG", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
        help="Sets the logging level - ALL_DEBUG sets all other loggers to DEBUG, too",
        type=str.upper,
        default="INFO",
    )
    parser.set_defaults(func=lambda *_: parser.print_usage())
    subparsers = parser.add_subparsers(help="available commands", metavar="CMD")

    parser_serve = subparsers.add_parser("serve")
    parser_serve.set_defaults(func=fn_serve)

    return parser.parse_args()


def fn_serve(args: Args) -> None:
    """Entry point for event consistency check"""
    chime.theme("big-sur")
    chime.notify_exceptions()
    serve(Context(), log_level=args.log_level).serve()


def main() -> int:
    """Entry point for everything else"""
    (args := parse_args()).func(args)
    return 0


if __name__ == "__main__":
    main()
