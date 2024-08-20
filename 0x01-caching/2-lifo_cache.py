#!/usr/bin/env python3
"""
Last-In First-Out (LIFO) caching module.

This module defines a caching system that follows the Last-In First-Out
(LIFO) eviction policy. When the cache exceeds the maximum allowed items,
the most recently added item is removed.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class.

    This class inherits from BaseCaching and implements a caching system
    with a LIFO (Last-In First-Out) eviction policy. Items are added to
    the cache, and when the cache exceeds the maximum allowed number of
    items, the most recently added item is removed.
    """

    def __init__(self):
        """
        Initializes the LIFO cache.

        The cache is implemented using an OrderedDict to preserve the insertion
        order and allow manipulation of item order. This is essential for the
        LIFO behavior.
        """
        super().__init__()
        # Use an OrderedDict to maintain the insertion order of items
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Adds an item to the cache.

        If either the `key` or `item` is None, this method does nothing. If the
        cache exceeds its size limit (as defined by BaseCaching.MAX_ITEMS), the
        most recently added item (the "last-in") is discarded.

        Args:
            key (str): The key under which the item is to be stored.
            item (any): The item to store in the cache.

        Returns:
            None
        """
        if key is None or item is None:
            return

        # If the key is not already in the cache, and the cache is full,
        # discard the last item added (LIFO)
        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # popitem(True) removes the last item added in the dictionary
                # (LIFO)
                last_key, _ = self.cache_data.popitem(last=True)
                print("DISCARD:", last_key)

        # Add or update the item in the cache
        self.cache_data[key] = item

        # Ensure the newly added or updated item is moved to the end of the
        # order
        self.cache_data.move_to_end(key, last=True)

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
