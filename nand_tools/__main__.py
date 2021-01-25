# -*- coding: utf-8 -*-
"""NAND Tools."""

import argparse

from .common import auto_int
from .logger import INFO
from .nand import NandTools


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
        action="store",
        type=str,
        help="Remove OOB (output file)",
    )

    args = parser.parse_args()

    if args.show_info:
        if (not args.input_file) or (not args.page_size) or (not args.oob_size):
            parser.print_help()
            return
    if args.remove_oob:
        if (
            (not args.input_file)
            or (not args.page_size)
            or (not args.oob_size)
            or (not args.block_size and args.skip_erased)
        ):
            parser.print_help()
            return
    if (not args.show_info) and (not args.remove_oob):
        parser.print_help()
        return

    nand = NandTools(
        logger_level=INFO,
        block_size=args.block_size,
        file=args.input_file,
        oob_size=args.oob_size,
        page_size=args.page_size,
    )

    if args.show_info:
        nand.show_info()

    if args.remove_oob:
        nand.remove_oob(
            output_file=args.remove_oob,
            skip_erased=args.skip_erased,
        )


main()
