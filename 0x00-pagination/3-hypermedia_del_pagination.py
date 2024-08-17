#!/usr/bin/env python3

"""
Adaptive pagination module.

This module provides an advanced pagination system that ensures users don't
miss items from the dataset even if some rows are removed between queries.
The main functionality is encapsulated in the `Server` class, which manages
a dataset of popular baby names.
"""

import csv
import math
from typing import List, Dict


class Server:
    """
    Server class to paginate a database of popular baby names.

    This class provides methods to load and index a dataset, enabling
    efficient pagination that adapts to changes in the dataset, such as
    rows being removed between page requests.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initialize a new Server instance.

        This constructor initializes the dataset and its indexed version to
        `None`. The dataset will be loaded and indexed when first accessed.
        """
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Load and cache the dataset.

        Loads the dataset from the CSV file if it hasn't been loaded yet. The
        dataset is cached to avoid reloading the file multiple times.

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

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Index the dataset by sorting position, starting at 0.

        Creates an indexed version of the dataset where each key is the
        original row number (starting from 0) and each value is the
        corresponding row data. This indexed dataset is useful for maintaining
        consistent pagination even if rows are removed.

        Returns:
            Dict[int, List]: A dictionary mapping the original row number to
            the row data.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in
                                      range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Return paginated data ensuring no items are skipped.

        This method returns a dictionary containing pagination information,
        starting from a specific index in the dataset. It ensures that even if
        some rows are removed from the dataset between queries, the user won't
        miss any data when moving between pages.

        Args:
            index (int): The starting index for pagination. Defaults to 0.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            Dict: A dictionary with the following key-value pairs:
                - index (int): The index of the first item on the current page.
                - next_index (int): The index of the first item on the next
                page.
                - page_size (int): The number of items on the current page.
                - data (List[List]): The list of rows corresponding to the
                current page.

        Example:
            If rows are removed from the dataset between requests, this method
            will adjust the page to ensure no rows are skipped:
                server.get_hyper_index(index=0, page_size=10) might return:
                {
                    'index': 0,
                    'next_index': 10,
                    'page_size': 10,
                    'data': [...]
                }
        """
        assert 0 <= index < len(self.dataset())

        indexed_dataset = self.indexed_dataset()
        indexed_page = {}

        i = index
        while len(indexed_page) < page_size and i < len(self.dataset()):
            if i in indexed_dataset:
                indexed_page[i] = indexed_dataset[i]
            i += 1

        page = list(indexed_page.values())
        page_indices = indexed_page.keys()

        return {
            'index': index,
            'next_index': max(page_indices) + 1,
            'page_size': len(page),
            'data': page
        }
