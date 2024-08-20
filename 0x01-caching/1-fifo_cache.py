#!/usr/bin/env python3
"""
First-In First-Out (FIFO) caching module.

This module defines a caching system that follows the First-In First-Out
(FIFO) eviction policy. When the cache exceeds the maximum allowed items,
the oldest item (the first one added) is removed.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class.

    This class inherits from BaseCaching and implements a caching system
    with a FIFO (First-In First-Out) eviction policy. Items are added to
    the cache, and when the cache exceeds the maximum allowed number of
    items, the oldest (first-added) item is removed.
    """

    def __init__(self):
        """
        Initializes the FIFO cache.

        The cache is implemented using an OrderedDict to preserve the insertion
        order, which is essential for the FIFO behavior.
        """
        super().__init__()
        # Use an OrderedDict to maintain the insertion order of items
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Adds an item to the cache.

        If the `key` or `item` is None, this method does nothing. If the cache
        exceeds its size limit (as defined by BaseCaching.MAX_ITEMS), the
        first-added item is discarded.

        Args:
            key (str): The key under which the item is to be stored.
            item (any): The item to store in the cache.

        Returns:
            None
        """
        if key is None or item is None:
            return

        # Add the item to the cache, replacing any existing item with the same
        # key
        self.cache_data[key] = item

        # If the number of items exceeds the maximum allowed, discard the first
        # item added
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # popitem(False) removes the first item added in the dictionary
            first_key, _ = self.cache_data.popitem(last=False)
            print("DISCARD:", first_key)

    def get(self, key):
        """
        Retrieves an item from the cache by its key.

        If the `key` is None or doesn't exist in the cache, this method
        returns None.

        Args:
            key (str): The key to look up in the cache.

        Returns:
            any: The item associated with the key, or None if the key is not
            found.
        """
        # Retrieve and return the item from the cache if it exists, or None if
        # not found
        return self.cache_data.get(key, None)
