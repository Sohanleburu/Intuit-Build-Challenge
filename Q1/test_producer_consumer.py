"""
Comprehensive Unit Tests for Producer-Consumer Pattern

Tests cover:
- Thread synchronization
- Concurrent programming
- Blocking queues
- Wait/Notify mechanism
- Producer and Consumer functionality
"""

import unittest
import threading
import time
from typing import List

from bounded_blocking_queue import BoundedBlockingQueue
from source_container import SourceContainer
from destination_container import DestinationContainer
from producer import Producer
from consumer import Consumer


class TestBoundedBlockingQueue(unittest.TestCase):
    """Test cases for BoundedBlockingQueue."""
    
    def test_queue_initialization(self):
        """Test queue initialization with valid capacity."""
        queue = BoundedBlockingQueue[int](5)
        self.assertEqual(queue.capacity(), 5)
        self.assertEqual(queue.size(), 0)
        self.assertTrue(queue.is_empty())
        self.assertFalse(queue.is_full())
    
    def test_queue_invalid_capacity(self):
        """Test queue initialization with invalid capacity."""
        with self.assertRaises(ValueError):
            BoundedBlockingQueue[int](0)
        
        with self.assertRaises(ValueError):
            BoundedBlockingQueue[int](-1)
    
    def test_put_and_get_single_item(self):
        """Test putting and getting a single item."""
        queue = BoundedBlockingQueue[int](5)
        queue.put(42)
        self.assertEqual(queue.size(), 1)
        self.assertFalse(queue.is_empty())
        
        item = queue.get()
        self.assertEqual(item, 42)
        self.assertEqual(queue.size(), 0)
        self.assertTrue(queue.is_empty())
    
    def test_put_and_get_multiple_items(self):
        """Test putting and getting multiple items."""
        queue = BoundedBlockingQueue[int](10)
        items = [1, 2, 3, 4, 5]
        
        for item in items:
            queue.put(item)
        
        self.assertEqual(queue.size(), len(items))
        
        retrieved = []
        while not queue.is_empty():
            retrieved.append(queue.get())
        
        self.assertEqual(retrieved, items)
    
    def test_queue_full_condition(self):
        """Test that queue correctly identifies when full."""
        queue = BoundedBlockingQueue[int](3)
        
        queue.put(1)
        queue.put(2)
        self.assertFalse(queue.is_full())
        
        queue.put(3)
        self.assertTrue(queue.is_full())
        self.assertEqual(queue.size(), 3)
    
    def test_blocking_on_full_queue(self):
        """Test that put() blocks when queue is full."""
        queue = BoundedBlockingQueue[int](2)
        queue.put(1)
        queue.put(2)
        
        # Queue is now full
        self.assertTrue(queue.is_full())
        
        # Try to put with timeout - should timeout
        with self.assertRaises(RuntimeError):
            queue.put(3, timeout=0.1)
    
    def test_blocking_on_empty_queue(self):
        """Test that get() blocks when queue is empty."""
        queue = BoundedBlockingQueue[int](5)
        
        # Try to get with timeout - should timeout
        with self.assertRaises(RuntimeError):
            queue.get(timeout=0.1)
    
    def test_concurrent_put_and_get(self):
        """Test concurrent put and get operations."""
        queue = BoundedBlockingQueue[int](10)
        results = []
        errors = []
        
        def producer():
            try:
                for i in range(10):
                    queue.put(i)
                    time.sleep(0.01)
            except Exception as e:
                errors.append(e)
        
        def consumer():
            try:
                for _ in range(10):
                    item = queue.get()
                    results.append(item)
                    time.sleep(0.01)
            except Exception as e:
                errors.append(e)
        
        prod_thread = threading.Thread(target=producer)
        cons_thread = threading.Thread(target=consumer)
        
        prod_thread.start()
        cons_thread.start()
        
        prod_thread.join()
        cons_thread.join()
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 10)
        self.assertEqual(sorted(results), list(range(10)))
    
    def test_multiple_producers_and_consumers(self):
        """Test multiple producers and consumers."""
        queue = BoundedBlockingQueue[int](20)
        results = []
        lock = threading.Lock()
        
        def producer(start, count):
            for i in range(start, start + count):
                queue.put(i)
        
        def consumer(count):
            for _ in range(count):
                item = queue.get()
                with lock:
                    results.append(item)
        
        # Create 3 producers, each producing 5 items
        prod_threads = [
            threading.Thread(target=producer, args=(i * 5, 5))
            for i in range(3)
        ]
        
        # Create 2 consumers, each consuming 7-8 items
        cons_threads = [
            threading.Thread(target=consumer, args=(8,)),
            threading.Thread(target=consumer, args=(7,))
        ]
        
        for t in prod_threads:
            t.start()
        for t in cons_threads:
            t.start()
        
        for t in prod_threads:
            t.join()
        for t in cons_threads:
            t.join()
        
        self.assertEqual(len(results), 15)
        self.assertEqual(sorted(results), list(range(15)))


class TestSourceContainer(unittest.TestCase):
    """Test cases for SourceContainer."""
    
    def test_container_initialization(self):
        """Test container initialization."""
        items = [1, 2, 3, 4, 5]
        container = SourceContainer[int](items)
        self.assertEqual(container.size(), 5)
        self.assertEqual(container.remaining(), 5)
    
    def test_get_next_items(self):
        """Test getting next items sequentially."""
        items = [1, 2, 3]
        container = SourceContainer[int](items)
        
        self.assertTrue(container.has_next())
        self.assertEqual(container.get_next(), 1)
        self.assertEqual(container.remaining(), 2)
        
        self.assertTrue(container.has_next())
        self.assertEqual(container.get_next(), 2)
        self.assertEqual(container.remaining(), 1)
        
        self.assertTrue(container.has_next())
        self.assertEqual(container.get_next(), 3)
        self.assertEqual(container.remaining(), 0)
        
        self.assertFalse(container.has_next())
        self.assertIsNone(container.get_next())
    
    def test_get_all_items(self):
        """Test getting all items."""
        items = [1, 2, 3, 4, 5]
        container = SourceContainer[int](items)
        all_items = container.get_all_items()
        self.assertEqual(all_items, items)
        # Original items should not be modified
        self.assertEqual(container.size(), 5)


class TestDestinationContainer(unittest.TestCase):
    """Test cases for DestinationContainer."""
    
    def test_container_initialization(self):
        """Test container initialization."""
        container = DestinationContainer[int]()
        self.assertEqual(container.size(), 0)
    
    def test_add_items(self):
        """Test adding items to container."""
        container = DestinationContainer[int]()
        
        container.add(1)
        self.assertEqual(container.size(), 1)
        
        container.add(2)
        self.assertEqual(container.size(), 2)
        
        container.add(3)
        self.assertEqual(container.size(), 3)
    
    def test_get_all_items(self):
        """Test getting all items from container."""
        container = DestinationContainer[int]()
        items = [1, 2, 3, 4, 5]
        
        for item in items:
            container.add(item)
        
        all_items = container.get_all_items()
        self.assertEqual(all_items, items)
    
    def test_clear(self):
        """Test clearing the container."""
        container = DestinationContainer[int]()
        container.add(1)
        container.add(2)
        
        self.assertEqual(container.size(), 2)
        container.clear()
        self.assertEqual(container.size(), 0)


class TestProducer(unittest.TestCase):
    """Test cases for Producer."""
    
    def test_producer_basic(self):
        """Test basic producer functionality."""
        source = SourceContainer[str](["a", "b", "c"])
        queue = BoundedBlockingQueue[str](10)
        
        producer = Producer(source, queue, name="TestProducer")
        producer.start()
        producer.join()
        
        self.assertEqual(producer.get_items_produced(), 3)
        self.assertEqual(queue.size(), 3)
    
    def test_producer_with_delay(self):
        """Test producer with delay."""
        source = SourceContainer[int](list(range(5)))
        queue = BoundedBlockingQueue[int](10)
        
        producer = Producer(source, queue, delay=0.05)
        start_time = time.time()
        producer.start()
        producer.join()
        elapsed = time.time() - start_time
        
        self.assertEqual(producer.get_items_produced(), 5)
        # Should take at least 5 * 0.05 = 0.25 seconds
        self.assertGreaterEqual(elapsed, 0.2)


class TestConsumer(unittest.TestCase):
    """Test cases for Consumer."""
    
    def test_consumer_basic(self):
        """Test basic consumer functionality."""
        queue = BoundedBlockingQueue[int](10)
        destination = DestinationContainer[int]()
        
        # Pre-populate queue
        for i in range(5):
            queue.put(i)
        
        consumer = Consumer(queue, destination, sentinel=-1)
        consumer.start()
        
        # Wait a bit for consumer to process
        time.sleep(0.2)
        consumer.request_stop()
        queue.put(-1)  # Send sentinel
        consumer.join()
        
        self.assertEqual(consumer.get_items_consumed(), 5)
        self.assertEqual(destination.size(), 5)
    
    def test_consumer_with_delay(self):
        """Test consumer with delay."""
        queue = BoundedBlockingQueue[int](10)
        destination = DestinationContainer[int]()
        
        # Pre-populate queue
        for i in range(3):
            queue.put(i)
        
        consumer = Consumer(queue, destination, delay=0.05, sentinel=-1)
        start_time = time.time()
        consumer.start()
        
        time.sleep(0.3)
        consumer.request_stop()
        queue.put(-1)
        consumer.join()
        elapsed = time.time() - start_time
        
        self.assertEqual(consumer.get_items_consumed(), 3)
        # Should take at least 3 * 0.05 = 0.15 seconds
        self.assertGreaterEqual(elapsed, 0.1)


class TestProducerConsumerIntegration(unittest.TestCase):
    """Integration tests for Producer-Consumer pattern."""
    
    def test_single_producer_single_consumer(self):
        """Test single producer and single consumer."""
        source_items = list(range(10))
        source = SourceContainer[int](source_items)
        queue = BoundedBlockingQueue[int](5)
        destination = DestinationContainer[int]()
        
        producer = Producer(source, queue, name="P1")
        consumer = Consumer(queue, destination, name="C1", sentinel=-1)
        
        consumer.start()
        producer.start()
        
        producer.join()
        
        # Wait a bit, then stop consumer
        time.sleep(0.2)
        consumer.request_stop()
        try:
            queue.put(-1, timeout=0.1)
        except:
            pass
        consumer.join()
        
        self.assertEqual(producer.get_items_produced(), 10)
        self.assertEqual(consumer.get_items_consumed(), 10)
        self.assertEqual(destination.size(), 10)
        self.assertEqual(set(destination.get_all_items()), set(source_items))
    
    def test_multiple_producers_single_consumer(self):
        """Test multiple producers and single consumer."""
        queue = BoundedBlockingQueue[int](10)
        destination = DestinationContainer[int]()
        
        source1 = SourceContainer[int](list(range(0, 5)))
        source2 = SourceContainer[int](list(range(5, 10)))
        
        producer1 = Producer(source1, queue, name="P1")
        producer2 = Producer(source2, queue, name="P2")
        consumer = Consumer(queue, destination, name="C1", sentinel=-1)
        
        consumer.start()
        producer1.start()
        producer2.start()
        
        producer1.join()
        producer2.join()
        
        time.sleep(0.3)
        consumer.request_stop()
        try:
            queue.put(-1, timeout=0.1)
        except:
            pass
        consumer.join()
        
        total_produced = producer1.get_items_produced() + producer2.get_items_produced()
        self.assertEqual(total_produced, 10)
        self.assertEqual(consumer.get_items_consumed(), 10)
        self.assertEqual(destination.size(), 10)
    
    def test_single_producer_multiple_consumers(self):
        """Test single producer and multiple consumers."""
        source = SourceContainer[int](list(range(20)))
        queue = BoundedBlockingQueue[int](10)
        destination1 = DestinationContainer[int]()
        destination2 = DestinationContainer[int]()
        
        producer = Producer(source, queue, name="P1")
        consumer1 = Consumer(queue, destination1, name="C1", sentinel=-1)
        consumer2 = Consumer(queue, destination2, name="C2", sentinel=-1)
        
        consumer1.start()
        consumer2.start()
        producer.start()
        
        producer.join()
        
        time.sleep(0.5)
        consumer1.request_stop()
        consumer2.request_stop()
        
        try:
            queue.put(-1, timeout=0.1)
            queue.put(-1, timeout=0.1)
        except:
            pass
        
        consumer1.join()
        consumer2.join()
        
        total_consumed = (
            consumer1.get_items_consumed() + consumer2.get_items_consumed()
        )
        self.assertEqual(producer.get_items_produced(), 20)
        self.assertEqual(total_consumed, 20)
        
        # All items should be in one of the destinations
        all_items = destination1.get_all_items() + destination2.get_all_items()
        self.assertEqual(len(all_items), 20)
        self.assertEqual(set(all_items), set(range(20)))
    
    def test_thread_synchronization(self):
        """Test that thread synchronization works correctly."""
        source = SourceContainer[str]([f"item-{i}" for i in range(50)])
        queue = BoundedBlockingQueue[str](5)  # Small queue to test blocking
        destination = DestinationContainer[str]()
        
        producer = Producer(source, queue, name="P1", delay=0.01)
        consumer = Consumer(queue, destination, name="C1", delay=0.02, sentinel="STOP")
        
        consumer.start()
        producer.start()
        
        producer.join()
        
        time.sleep(0.5)
        consumer.request_stop()
        try:
            queue.put("STOP", timeout=0.1)
        except:
            pass
        consumer.join()
        
        # Verify all items were transferred
        self.assertEqual(producer.get_items_produced(), 50)
        self.assertEqual(consumer.get_items_consumed(), 50)
        self.assertEqual(destination.size(), 50)
        self.assertEqual(
            set(source.get_all_items()),
            set(destination.get_all_items())
        )


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)

