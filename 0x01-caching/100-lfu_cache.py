#!/usr/bin/python3
"""
Least Frequently Used (LFU) Caching Module.

This module defines a caching system that follows the Least Frequently Used
(LFU) eviction policy. When the cache exceeds the maximum allowed items,
the least frequently used item is removed.
"""
from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache class.

    This class implements a caching system with an LFU (Least Frequently Used)
    eviction policy. When the cache exceeds its maximum allowed number of items
    the least frequently used item is removed. In case of a tie, the Least
    Recently Used (LRU) item among the least frequently used is removed.
    """

    def __init__(self):
        """
        Initializes the cache.
        """
        super().__init__()
        # OrderedDict to maintain the order of key access (Least Recently Used)
        self.lru_order_cache = OrderedDict()
        # Dictionary to track the frequency of access for each key
        self.frequency_tracker = {}

    def put(self, key, item):
        """
        Adds an item to the cache using the LFU algorithm.

        If the cache is full, the least frequently used (LFU) item will be
        removed. If there is a tie (multiple items have the same minimum
        frequency), the Least Recently Used (LRU) item among them will be
        removed.

        Args:
            key (str): The key to store the item under.
            item (any): The value to be associated with the key.

        Returns:
            None
        """
        if key is None or item is None:
            return

        # If the key is already in the cache, remove it first to update its
        # value
        if key in self.lru_order_cache:
            del self.lru_order_cache[key]

        # Check if the cache exceeds the maximum allowed items
        if len(self.lru_order_cache) >= BaseCaching.MAX_ITEMS:
            # Find the minimum frequency in the frequency tracker
            min_frequency = min(self.frequency_tracker.values())
            # List all keys that have the minimum frequency
            least_frequent_keys = [k for k, v in self.frequency_tracker.items()
                                   if v == min_frequency]

            # If there's exactly one LFU key, discard it
            if len(least_frequent_keys) == 1:
                least_frequent_key = least_frequent_keys[0]
                print("DISCARD:", least_frequent_key)
                # Remove from LRU cache
                self.lru_order_cache.pop(least_frequent_key)
                # Remove from frequency tracker
                del self.frequency_tracker[least_frequent_key]

            # If there are multiple LFU keys, discard the Least Recently Used
            # (LRU) one
            else:
                for lru_key, _ in list(self.lru_order_cache.items()):
                    if lru_key in least_frequent_keys:
                        print("DISCARD:", lru_key)
                        # Remove from LRU cache
                        self.lru_order_cache.pop(lru_key)
                        # Remove from frequency tracker
                        del self.frequency_tracker[lru_key]
                        break

        # Add the new key-value pair to the LRU cache
        self.lru_order_cache[key] = item
        # Move to the end to mark it as recently used
        self.lru_order_cache.move_to_end(key)

        # Update the frequency count in the frequency tracker
        if key in self.frequency_tracker:
            self.frequency_tracker[key] += 1
        else:
            self.frequency_tracker[key] = 1

        # Update the main cache data dictionary
        self.cache_data = dict(self.lru_order_cache)

    def get(self, key):
        """
        Retrieves an item from the cache by its key.

        If the key exists in the cache, its frequency is incremented.
        The item is also moved to the end of the LRU cache to mark it as
        recently used.

        Args:
            key (str): The key of the item to retrieve.

        Returns:
            any: The value associated with the key, or None if the key is not
            found.
        """
        if key is None or key not in self.lru_order_cache:
            return None

        # Move the key to the end of the LRU cache to mark it as recently used
        value = self.lru_order_cache[key]
        self.lru_order_cache.move_to_end(key)

        # Increment the access frequency in the frequency tracker
        if key in self.frequency_tracker:
            self.frequency_tracker[key] += 1
        else:
            self.frequency_tracker[key] = 1

        return value
