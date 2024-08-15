#!/usr/bin/env python3
"""
Pagination helper module.

This module contains a helper function for determining the start and end
indexes for paginating a list of items based on the given page number and
page size.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end indexes for a given page and page size.

    This function is used to retrieve the range of indexes that correspond to
    the items on a specific page when paginating a collection of items.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index and end index for
        the given page. The start index is inclusive, and the end index is
        exclusive.

    Example:
        If you have a list of 100 items and you want to paginate it with
        `page_size` = 10:
            - `index_range(1, 10)` will return (0, 10)
            - `index_range(2, 10)` will return (10, 20)
            - `index_range(3, 10)` will return (20, 30)
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)
