"""
Source Container Implementation

A container that holds items to be consumed by the producer.
"""

import threading
from typing import List, Generic, TypeVar, Optional

T = TypeVar('T')


class SourceContainer(Generic[T]):
    """
    A container that holds source items for the producer to read.
    
    This is a simple container that stores items and provides
    methods to read them sequentially.
    """
    
    def __init__(self, items: List[T]):
        """
        Initialize the source container with items.
        
        Args:
            items: List of items to store in the container.
        """
        self._items = items.copy()
        self._index = 0
        self._lock = threading.Lock()
    
    def has_next(self) -> bool:
        """
        Check if there are more items to read.
        
        Returns:
            True if there are more items, False otherwise.
        """
        with self._lock:
            return self._index < len(self._items)
    
    def get_next(self) -> Optional[T]:
        """
        Get the next item from the container.
        
        Returns:
            The next item, or None if no more items are available.
        """
        with self._lock:
            if self._index < len(self._items):
                item = self._items[self._index]
                self._index += 1
                return item
            return None
    
    def get_all_items(self) -> List[T]:
        """
        Get all items in the container (for testing purposes).
        
        Returns:
            List of all items in the container.
        """
        with self._lock:
            return self._items.copy()
    
    def size(self) -> int:
        """
        Get the total number of items in the container.
        
        Returns:
            Total number of items.
        """
        with self._lock:
            return len(self._items)
    
    def remaining(self) -> int:
        """
        Get the number of remaining items to be read.
        
        Returns:
            Number of remaining items.
        """
        with self._lock:
            return len(self._items) - self._index

