#!/usr/bin/env python3
"""
Basic caching module.

This module defines a basic caching system that allows storing
and retrieving items in memory using a dictionary.
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class.

    This class inherits from BaseCaching and implements basic caching
    functionality. It allows storing and retrieving items from a dictionary
    with no limit on the size of the cache. This means it won't enforce any
    eviction policy when the cache reaches a certain size.
    """

    def put(self, key, item):
        """
        Adds an item to the cache.

        If either the `key` or `item` is None, this method does nothing.

        Args:
            key (str): The key under which the item is to be stored.
            item (any): The item to store in the cache.

        Returns:
            None
        """
        if key is None or item is None:
            return
        # Store the item in the cache using the provided key
        self.cache_data[key] = item

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
        # Retrieve and return the item from the cache if it exists, or None
        # if not found
        return self.cache_data.get(key, None)
