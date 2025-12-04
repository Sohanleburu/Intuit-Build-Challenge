"""
Producer Thread Implementation

A producer thread that reads from a source container and places items
into a shared blocking queue.
"""

import threading
import time
from typing import Generic, TypeVar

from bounded_blocking_queue import BoundedBlockingQueue
from source_container import SourceContainer

T = TypeVar('T')


class Producer(threading.Thread, Generic[T]):
    """
    Producer thread that reads items from a source container
    and places them into a shared blocking queue.
    
    The producer will continue reading items until the source
    container is empty.
    """
    
    def __init__(
        self,
        source: SourceContainer[T],
        queue: BoundedBlockingQueue[T],
        name: str = "Producer",
        delay: float = 0.0
    ):
        """
        Initialize the producer thread.
        
        Args:
            source: Source container to read items from.
            queue: Shared blocking queue to place items into.
            name: Name of the producer thread.
            delay: Optional delay between producing items (in seconds).
        """
        super().__init__(name=name, daemon=False)
        self._source = source
        self._queue = queue
        self._delay = delay
        self._items_produced = 0
        self._lock = threading.Lock()
    
    def run(self) -> None:
        """
        Main execution method for the producer thread.
        
        Reads items from the source container and places them
        into the shared queue until the source is empty.
        """
        print(f"[{self.name}] Started producing items")
        
        while self._source.has_next():
            item = self._source.get_next()
            if item is not None:
                try:
                    # Put item into queue (will block if queue is full)
                    self._queue.put(item)
                    
                    with self._lock:
                        self._items_produced += 1
                    
                    print(f"[{self.name}] Produced item: {item}")
                    
                    # Optional delay to simulate processing time
                    if self._delay > 0:
                        time.sleep(self._delay)
                
                except Exception as e:
                    print(f"[{self.name}] Error producing item: {e}")
                    break
        
        print(f"[{self.name}] Finished producing. Total items produced: {self.get_items_produced()}")
    
    def get_items_produced(self) -> int:
        """
        Get the number of items produced by this producer.
        
        Returns:
            Number of items produced.
        """
        with self._lock:
            return self._items_produced

