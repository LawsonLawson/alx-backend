#!/usr/bin/env python3
"""
Simple pagination module.

This module provides a `Server` class that can be used to paginate
through a dataset of popular baby names stored in a CSV file. It also
includes a helper function `index_range` to calculate the start and end
indexes for each page.
"""

import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end indexes for a given page and page size.

    This function is used to retrieve the range of indexes that correspond
    to the items on a specific page when paginating a collection of items.

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


class Server:
    """
    Server class to paginate a database of popular baby names.

    This class loads a CSV file containing baby names and allows for
    retrieval of specific pages of data based on pagination parameters.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initializes a new Server instance.

        This constructor initializes the dataset to `None`. The dataset
        will be loaded from the CSV file the first time it is accessed.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Cached dataset.

        Loads the dataset from the CSV file if it hasn't been loaded yet.
        The dataset is cached to avoid reloading the file multiple times.

        Returns:
            List[List]: A list of lists where each inner list represents
            a row from the dataset (excluding the header row).
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header row

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a page of data from the dataset.

        Args:
            page (int): The page number (1-indexed). Defaults to 1.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            List[List]: A list of rows corresponding to the given page. Each
            row is a list of values representing a record in the dataset.

        Raises:
            AssertionError: If `page` or `page_size` are not positive integers.

        Example:
            To retrieve the first 10 records:
                server.get_page(1, 10)
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0

        start, end = index_range(page, page_size)
        data = self.dataset()

        if start >= len(data):  # Check if the start index is out of range
            return []

        return data[start:end]
