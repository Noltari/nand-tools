# -*- coding: utf-8 -*-
"""NAND."""

import logging
import os

from .common import convert_size

_LOGGER = logging.getLogger(__name__)


class NAND:
    """NAND."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, file, oob_size, page_size, block_size=None):
        """Init NAND Tools."""
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
            _LOGGER.error(
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
                    _LOGGER.debug("Erased block %d/%d", blck_cnt, self.num_blocks)

            progress = int(round(page * 100 / self.num_pages, 0))
            if progress != last_progress:
                _LOGGER.info("Removing OOB: %d%%...", progress)
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

        if self.block_size:
            erase_percent = int(round(erased_blocks * 100 / self.num_blocks, 0))
            _LOGGER.info(
                "Erased blocks: %d/%d (%d%%)",
                erased_blocks,
                self.num_blocks,
                erase_percent,
            )

        in_f.close()
        out_f.close()

    def show_info(self):
        """Show NAND info."""
        separator = "--------------------"
        _LOGGER.info("NAND Info:")
        _LOGGER.info("\tRaw Size: %s", convert_size(self.raw_size))
        _LOGGER.info("\tSize: %s", convert_size(self.size))

        _LOGGER.info("\t%s", separator)
        _LOGGER.info("\tTotal Pages: %d", self.num_pages)
        if self.num_blocks:
            _LOGGER.info("\tTotal Blocks: %d", self.num_blocks)
        if self.block_pages:
            _LOGGER.info("\tBlock Pages: %d", self.block_pages)

        if self.block_size:
            _LOGGER.info("\t%s", separator)
            _LOGGER.info("\tRaw Block Size: %s", convert_size(self.raw_block_size))
            _LOGGER.info("\tBlock Size: %s", convert_size(self.block_size))

        _LOGGER.info("\t%s", separator)
        _LOGGER.info("\tOOB Size: %d", self.oob_size)

        _LOGGER.info("\t%s", separator)
        _LOGGER.info("\tRaw Page size: %d", self.raw_page_size)
        _LOGGER.info("\tPage size: %d", self.page_size)
