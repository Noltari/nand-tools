# -*- coding: utf-8 -*-
"""NAND Tools."""

import logging
import os

from .common import convert_size

_LOGGER = logging.getLogger(__name__)


class NAND:
    """NAND Tools."""

    def __init__(self, file, oob_size, page_size):
        """Init NAND Tools."""
        self.file = file
        self.oob_size = oob_size
        self.page_size = page_size

        in_st = os.stat(self.file)
        self.raw_size = in_st.st_size
        self.raw_page_size = self.oob_size + self.page_size
        self.num_pages = int(self.raw_size / self.raw_page_size)
        self.size = self.num_pages * self.page_size

    def remove_oob(self, output_file):
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
        last_progress = -1
        for page in range(self.num_pages):
            raw_bytes = in_f.read(self.raw_page_size)
            out_f.write(raw_bytes[: self.page_size])

            progress = int(round(page * 100 / self.num_pages, 0))
            if progress != last_progress:
                _LOGGER.info("Removing OOB: %d%%...", progress)
                last_progress = progress

        in_f.close()
        out_f.close()

    def show_info(self):
        """Show NAND info."""
        _LOGGER.info("NAND Info:")
        _LOGGER.info("\tSize: %s", convert_size(self.size))
        _LOGGER.info("\tRaw Size: %s", convert_size(self.raw_size))
        _LOGGER.info("\tPage size: %d", self.page_size)
        _LOGGER.info("\tOOB Size: %d", self.oob_size)
        _LOGGER.info("\tRaw Page size: %d", self.raw_page_size)
        _LOGGER.info("\tNumber of Pages: %d", self.num_pages)
