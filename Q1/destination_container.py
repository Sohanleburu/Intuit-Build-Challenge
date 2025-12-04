"""
Destination Container Implementation

A container that stores items consumed from the queue.
"""

import threading
from typing import List, Generic, TypeVar

T = TypeVar('T')


class DestinationContainer(Generic[T]):
    """
    A container that stores items consumed from the queue.
    
    This container is thread-safe and provides methods to add items
    and retrieve all stored items.
    """
    
    def __init__(self):
        """Initialize an empty destination container."""
        self._items: List[T] = []
        self._lock = threading.Lock()
    
    def add(self, item: T) -> None:
        """
        Add an item to the destination container.
        
        Args:
            item: The item to add.
        """
        with self._lock:
            self._items.append(item)
    
    def get_all_items(self) -> List[T]:
        """
        Get all items stored in the container.
        
        Returns:
            List of all items in the container.
        """
        with self._lock:
            return self._items.copy()
    
    def size(self) -> int:
        """
        Get the number of items in the container.
        
        Returns:
            Number of items in the container.
        """
        with self._lock:
            return len(self._items)
    
    def clear(self) -> None:
        """
        Clear all items from the container.
        """
        with self._lock:
            self._items.clear()

