# -*- coding: utf-8 -*-
"""NAND Tools."""

import logging
import os

from .common import convert_size

_LOGGER = logging.getLogger(__name__)


class NAND:
    """NAND Tools."""

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
            self.block_pages = self.block_size / self.page_size
            self.raw_block_size = self.block_pages * self.raw_page_size
        else:
            self.block_pages = None
            self.raw_block_size = None

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

        block_cnt = 0
        block_offset = 0
        last_progress = -1
        for page in range(self.num_pages):
            block_skip = False

            raw_bytes = in_f.read(self.raw_page_size)
            page_bytes = raw_bytes[: self.page_size]

            if (not block_offset) and self.block_size:
                block_cnt += 1
                if skip_erased and (list(page_bytes) == [0xFF] * len(page_bytes)):
                    block_skip = True
                    _LOGGER.debug("Skipping erased block %d...", block_cnt)

            progress = int(round(page * 100 / self.num_pages, 0))
            if progress != last_progress:
                _LOGGER.info("Removing OOB: %d%%...", progress)
                last_progress = progress

            if block_skip:
                page = page + (self.block_pages - 1)
                block_offset = 0
            else:
                out_f.write(page_bytes)
                if self.block_size:
                    block_offset = (block_offset + self.page_size) % (self.block_size)

        in_f.close()
        out_f.close()

    def show_info(self):
        """Show NAND info."""
        separator = "--------------------"
        _LOGGER.info("NAND Info:")
        _LOGGER.info("\tRaw Size: %s", convert_size(self.raw_size))
        _LOGGER.info("\tSize: %s", convert_size(self.size))
        _LOGGER.info("\tTotal Pages: %d", self.num_pages)
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
