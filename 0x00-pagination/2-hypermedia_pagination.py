#!/usr/bin/env python3

"""
Advanced pagination module.

This module extends the Server class with a `get_hyper` method that provides
additional pagination information in the form of a dictionary. The module
is designed to work with a dataset of popular baby names stored in a CSV file.
"""

import csv
from math import ceil
from typing import List, Dict

# Import the index_range function from a separate module
index_range = __import__('0-simple_helper_function').index_range


class Server:
    """
    Server class to paginate a database of popular baby names.

    This class loads a dataset from a CSV file and allows for retrieval of
    specific pages of data. It also provides additional metadata about the
    pagination through the `get_hyper` method.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initialize a new Server instance.

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
        """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        start, end = index_range(page, page_size)
        try:
            return self.dataset()[start:end]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size:
                  int = 10) -> Dict[str, int or List[List] or None]:
        """
        Returns a dictionary containing pagination information and the data
        for the given page.

        Args:
            page (int): The page number (1-indexed). Defaults to 1.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            dict: A dictionary with the following key-value pairs:
                - page_size (int): The number of items on the current page.
                - page (int): The current page number.
                - data (List[List]): The data on the current page.
                - next_page (int or None): The next page number, or None if
                there is no next page.
                - prev_page (int or None): The previous page number, or None if
                there is no previous page.
                - total_pages (int): The total number of pages in the dataset.

        Example:
            If the dataset has 100 items and you request page 1 with a page
            size of 10:
                server.get_hyper(1, 10) might return:
                {
                    "page_size": 10,
                    "page": 1,
                    "data": [...],
                    "next_page": 2,
                    "prev_page": None,
                    "total_pages": 10
                }
        """
        page_data = self.get_page(page, page_size)
        total_data = len(self.dataset())
        total_pages = ceil(total_data / page_size)

        return {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }
