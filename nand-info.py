#!/usr/bin/env python3
"""NAND OOB Remover."""

import argparse
import logging
import sys

from nand_tools.common import auto_int
from nand_tools.nand import NAND


def main():
    """NAND OOB Remover."""
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

    args = parser.parse_args()

    if (not args.input_file) or (not args.oob_size) or (not args.page_size):
        parser.print_help()

    nand = NAND(
        block_size=args.block_size,
        file=args.input_file,
        oob_size=args.oob_size,
        page_size=args.page_size,
    )
    nand.show_info()


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
main()
