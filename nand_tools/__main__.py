#!/usr/bin/env python3
"""NAND Tools."""

import argparse
import logging
import sys

from .common import auto_int
from .nand import NAND


def main():
    """NAND Tools."""
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--block-size",
        dest="block_size",
        action="store",
        type=auto_int,
        help="Block Size",
    )

    parser.add_argument(
        "--input-file",
        dest="input_file",
        action="store",
        type=str,
        help="Input file",
    )

    parser.add_argument(
        "--oob-size",
        dest="oob_size",
        action="store",
        type=auto_int,
        help="OOB Size",
    )

    parser.add_argument(
        "--output-file",
        dest="output_file",
        action="store",
        type=str,
        help="Output file",
    )

    parser.add_argument(
        "--page-size",
        dest="page_size",
        action="store",
        type=auto_int,
        help="Page Size",
    )

    parser.add_argument(
        "--show-info",
        dest="show_info",
        action="store_true",
        help="Show NAND info",
    )

    parser.add_argument(
        "--skip-erased",
        dest="skip_erased",
        action="store_true",
        help="Skip erased blocks",
    )

    parser.add_argument(
        "--remove-oob",
        dest="remove_oob",
        action="store_true",
        help="Remove OOB",
    )

    args = parser.parse_args()

    if args.show_info:
        if (not args.input_file) or (not args.page_size) or (not args.oob_size):
            parser.print_help()
            return
    if args.remove_oob:
        # pylint: disable-msg=too-many-boolean-expressions
        if (
            (not args.input_file)
            or (not args.page_size)
            or (not args.oob_size)
            or (not args.output_file)
            or (not args.block_size and args.skip_erased)
        ):
            parser.print_help()
            return
    if (not args.show_info) and (not args.remove_oob):
        parser.print_help()
        return

    nand = NAND(
        block_size=args.block_size,
        file=args.input_file,
        oob_size=args.oob_size,
        page_size=args.page_size,
    )

    if args.show_info:
        nand.show_info()

    if args.remove_oob:
        nand.remove_oob(
            output_file=args.output_file,
            skip_erased=args.skip_erased,
        )


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
main()
