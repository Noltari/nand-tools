# -*- coding: utf-8 -*-
"""NAND."""

import os
import sys

from .common import convert_size
from .logger import INFO, Logger


class NAND:
    """NAND."""

    # pylint: disable=too-many-arguments,too-many-instance-attributes
    def __init__(
        self,
        file,
        oob_size,
        page_size,
        block_size=None,
        logger_level=INFO,
        logger_stream=sys.stdout,
    ):
        """Init NAND Tools."""
        self.log = Logger(level=logger_level, stream=logger_stream)
        self.block_size = block_size
        self.file = file
        self.oob_size = oob_size
        self.page_size = page_size

        in_st = os.stat(self.file)
        self.raw_size = in_st.st_size
        self.raw_page_size = self.oob_size + self.page_size
        self.num_pages = int(self.raw_size / self.raw_page_size)
        self.size = self.num_pages * self.page_size

        if self.block_size:
            self.block_pages = int(self.block_size / self.page_size)
            self.num_blocks = self.size / self.block_size
            self.raw_block_size = self.block_pages * self.raw_page_size
        else:
            self.block_pages = None
            self.num_blocks = None
            self.raw_block_size = None

    # pylint: disable=too-many-locals
    def remove_oob(self, output_file, skip_erased=False):
        """Remove NAND OOB."""
        if (self.raw_size % self.raw_page_size) != 0:
            self.log.error(
                "file size (%d) has to be a multiple of %d",
                self.raw_size,
                self.raw_page_size,
            )
            return

        in_f = open(self.file, "r+b")
        out_f = open(output_file, "w+b")

        if self.block_size:
            erased_page_bytes = [0xFF] * self.page_size
        else:
            erased_page_bytes = None

        blck_cnt = 0
        block_offset = 0
        erased_blocks = 0
        last_progress = -1
        page = 0
        while page < self.num_pages:
            block_skip = False

            raw_bytes = in_f.read(self.raw_page_size)
            page_bytes = raw_bytes[: self.page_size]

            if (not block_offset) and self.block_size:
                blck_cnt += 1
                if list(page_bytes) == erased_page_bytes:
                    erased_blocks += 1
                    block_skip = skip_erased
                    self.log.debug("Erased block %d/%d\n", blck_cnt, self.num_blocks)

            progress = int(round(page * 100 / self.num_pages, 0))
            if progress != last_progress:
                self.log.info("Removing OOB: %d%%...\r", progress)
                last_progress = progress

            if block_skip:
                page += self.block_pages
                in_f.seek(self.raw_block_size - self.raw_page_size, 1)
                block_offset = 0
            else:
                out_f.write(page_bytes)
                page += 1
                if self.block_size:
                    block_offset = (block_offset + self.page_size) % (self.block_size)

        self.log.info("\n")

        if self.block_size:
            erase_percent = int(round(erased_blocks * 100 / self.num_blocks, 0))
            self.log.info(
                "Erased blocks: %d/%d (%d%%)\n",
                erased_blocks,
                self.num_blocks,
                erase_percent,
            )

        in_f.close()
        out_f.close()

    def show_info(self):
        """Show NAND info."""
        separator = "--------------------"
        self.log.info("NAND Info:\n")
        self.log.info("\tRaw Size: %s\n", convert_size(self.raw_size))
        self.log.info("\tSize: %s\n", convert_size(self.size))

        self.log.info("\t%s\n", separator)
        self.log.info("\tTotal Pages: %d\n", self.num_pages)
        if self.num_blocks:
            self.log.info("\tTotal Blocks: %d\n", self.num_blocks)
        if self.block_pages:
            self.log.info("\tBlock Pages: %d\n", self.block_pages)

        if self.block_size:
            self.log.info("\t%s\n", separator)
            self.log.info("\tRaw Block Size: %s\n", convert_size(self.raw_block_size))
            self.log.info("\tBlock Size: %s\n", convert_size(self.block_size))

        self.log.info("\t%s\n", separator)
        self.log.info("\tOOB Size: %d\n", self.oob_size)

        self.log.info("\t%s\n", separator)
        self.log.info("\tRaw Page size: %d\n", self.raw_page_size)
        self.log.info("\tPage size: %d\n", self.page_size)
