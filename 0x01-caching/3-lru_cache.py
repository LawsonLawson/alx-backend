#!/usr/bin/env python3
"""
Least Recently Used (LRU) Caching Module.

This module defines a caching system that follows the Least Recently Used
(LRU) eviction policy. When the cache exceeds the maximum allowed items,
the least recently used item is removed.
"""
from collections import OrderedDict

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class.

    This class inherits from BaseCaching and implements a caching system
    with an LRU (Least Recently Used) eviction policy. The least recently
    used item will be removed from the cache when it exceeds the maximum
    allowed number of items.
    """

    def __init__(self):
        """
        Initializes the cache.

        The cache is represented by an OrderedDict, which automatically
        maintains the order in which items are added. The oldest item
        (i.e., the least recently used) is stored at the end of the OrderedDict
        and the newest (i.e., most recently used) at the beginning.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Adds an item to the cache.

        If the key is already in the cache, it will be updated and moved to the
        most recently used (MRU) position. If the cache exceeds its size limit,
        the least recently used (LRU) item will be removed.

        Args:
            key (str): The key to store the item under.
            item (any): The value to be associated with the key.

        Returns:
            None
        """
        if key is None or item is None:
            return

        # If the key is new and cache exceeds its max size, remove the least
        # recently used (LRU) item
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                # Remove the least recently used item (last entry)
                lru_key, _ = self.cache_data.popitem(last=True)
                print("DISCARD:", lru_key)

            # Add the new key-value pair to the cache and move it to the most
            # recently used (front) position
            self.cache_data[key] = item
            # Move to front (MRU position)
            self.cache_data.move_to_end(key, last=False)

        else:
            # If the key already exists, update its value
            self.cache_data[key] = item
            # Ensure the key is moved to the most recently used (front)
            # position
            self.cache_data.move_to_end(key, last=False)

    def get(self, key):
        """
        Retrieves an item from the cache by its key.

        If the key exists in the cache, it is moved to the most recently used
        (MRU) position.
        If the key does not exist, None is returned.

        Args:
            key (str): The key of the item to retrieve.

        Returns:
            any: The value associated with the key, or None if the key is not
            found.
        """
        if key is not None and key in self.cache_data:
            # Move the key to the most recently used (front) position
            self.cache_data.move_to_end(key, last=False)
        # Return the value associated with the key (or None if not found)
        return self.cache_data.get(key, None)
