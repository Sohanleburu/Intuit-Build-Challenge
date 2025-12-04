"""
Bounded Blocking Queue Implementation

A thread-safe bounded blocking queue that supports producer-consumer pattern.
Uses wait/notify mechanism for thread synchronization.
"""

import threading
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class BoundedBlockingQueue(Generic[T]):
    """
    A thread-safe bounded blocking queue implementation.
    
    This queue has a maximum capacity. When the queue is full, producers
    will block until space is available. When the queue is empty, consumers
    will block until items are available.
    
    Uses Python's threading.Condition for wait/notify synchronization.
    """
    
    def __init__(self, capacity: int):
        """
        Initialize the bounded blocking queue.
        
        Args:
            capacity: Maximum number of items the queue can hold.
                     Must be a positive integer.
        
        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        
        self._capacity = capacity
        self._queue: list[T] = []
        self._lock = threading.Condition()
        self._size = 0
    
    def put(self, item: T, timeout: Optional[float] = None) -> bool:
        """
        Add an item to the queue.
        
        If the queue is full, this method will block until space becomes
        available or timeout occurs.
        
        Args:
            item: The item to add to the queue.
            timeout: Maximum time to wait in seconds. None means wait indefinitely.
        
        Returns:
            True if item was successfully added, False if timeout occurred.
        
        Raises:
            RuntimeError: If timeout occurs.
        """
        with self._lock:
            # Wait until there's space in the queue
            while self._size >= self._capacity:
                if timeout is None:
                    self._lock.wait()
                else:
                    if not self._lock.wait(timeout):
                        raise RuntimeError("Timeout waiting to put item in queue")
            
            # Add item to queue
            self._queue.append(item)
            self._size += 1
            
            # Notify waiting consumers
            self._lock.notify()
            return True
    
    def get(self, timeout: Optional[float] = None) -> T:
        """
        Remove and return an item from the queue.
        
        If the queue is empty, this method will block until an item becomes
        available or timeout occurs.
        
        Args:
            timeout: Maximum time to wait in seconds. None means wait indefinitely.
        
        Returns:
            The item removed from the queue.
        
        Raises:
            RuntimeError: If timeout occurs.
        """
        with self._lock:
            # Wait until there's an item in the queue
            while self._size == 0:
                if timeout is None:
                    self._lock.wait()
                else:
                    if not self._lock.wait(timeout):
                        raise RuntimeError("Timeout waiting to get item from queue")
            
            # Remove and return item
            item = self._queue.pop(0)
            self._size -= 1
            
            # Notify waiting producers
            self._lock.notify()
            return item
    
    def size(self) -> int:
        """
        Get the current number of items in the queue.
        
        Returns:
            Current queue size.
        """
        with self._lock:
            return self._size
    
    def capacity(self) -> int:
        """
        Get the maximum capacity of the queue.
        
        Returns:
            Queue capacity.
        """
        return self._capacity
    
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if queue is empty, False otherwise.
        """
        with self._lock:
            return self._size == 0
    
    def is_full(self) -> bool:
        """
        Check if the queue is full.
        
        Returns:
            True if queue is full, False otherwise.
        """
        with self._lock:
            return self._size >= self._capacity

