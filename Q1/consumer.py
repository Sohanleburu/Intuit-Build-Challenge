"""
Consumer Thread Implementation

A consumer thread that reads items from a shared blocking queue
and stores them in a destination container.
"""

import threading
import time
from typing import Generic, TypeVar

from bounded_blocking_queue import BoundedBlockingQueue
from destination_container import DestinationContainer

T = TypeVar('T')


class Consumer(threading.Thread, Generic[T]):
    """
    Consumer thread that reads items from a shared blocking queue
    and stores them in a destination container.
    
    The consumer will continue reading items until it receives
    a sentinel value indicating no more items will be produced.
    """
    
    def __init__(
        self,
        queue: BoundedBlockingQueue[T],
        destination: DestinationContainer[T],
        name: str = "Consumer",
        delay: float = 0.0,
        sentinel: T = None
    ):
        """
        Initialize the consumer thread.
        
        Args:
            queue: Shared blocking queue to read items from.
            destination: Destination container to store items.
            name: Name of the consumer thread.
            delay: Optional delay between consuming items (in seconds).
            sentinel: Sentinel value to indicate end of production.
                     When this value is received, consumer will stop.
        """
        super().__init__(name=name, daemon=False)
        self._queue = queue
        self._destination = destination
        self._delay = delay
        self._sentinel = sentinel
        self._items_consumed = 0
        self._lock = threading.Lock()
        self._stop_requested = False
    
    def request_stop(self) -> None:
        """
        Request the consumer to stop after processing current items.
        """
        with self._lock:
            self._stop_requested = True
    
    def run(self) -> None:
        """
        Main execution method for the consumer thread.
        
        Reads items from the shared queue and stores them in the
        destination container until stop is requested or sentinel is received.
        """
        print(f"[{self.name}] Started consuming items")
        
        while True:
            # Check if stop was requested
            with self._lock:
                if self._stop_requested:
                    break
            
            try:
                # Get item from queue (will block if queue is empty)
                item = self._queue.get()
                
                # Check for sentinel value
                if self._sentinel is not None and item == self._sentinel:
                    print(f"[{self.name}] Received sentinel, stopping")
                    break
                
                # Store item in destination
                self._destination.add(item)
                
                with self._lock:
                    self._items_consumed += 1
                
                print(f"[{self.name}] Consumed item: {item}")
                
                # Optional delay to simulate processing time
                if self._delay > 0:
                    time.sleep(self._delay)
            
            except Exception as e:
                print(f"[{self.name}] Error consuming item: {e}")
                break
        
        print(f"[{self.name}] Finished consuming. Total items consumed: {self.get_items_consumed()}")
    
    def get_items_consumed(self) -> int:
        """
        Get the number of items consumed by this consumer.
        
        Returns:
            Number of items consumed.
        """
        with self._lock:
            return self._items_consumed

