"""
Main Program - Producer-Consumer Pattern Demonstration

This program demonstrates the producer-consumer pattern with thread synchronization.
It creates producer and consumer threads that communicate through a shared
bounded blocking queue.
"""

from bounded_blocking_queue import BoundedBlockingQueue
from source_container import SourceContainer
from destination_container import DestinationContainer
from producer import Producer
from consumer import Consumer


def main():
    """
    Main function to demonstrate producer-consumer pattern.
    """
    print("=" * 60)
    print("Producer-Consumer Pattern Demonstration")
    print("=" * 60)
    print()
    
    # Configuration
    queue_capacity = 5
    source_items = [f"Item-{i}" for i in range(1, 21)]  # 20 items
    producer_delay = 0.1  # 100ms delay between producing items
    consumer_delay = 0.15  # 150ms delay between consuming items
    
    print(f"Configuration:")
    print(f"  Queue Capacity: {queue_capacity}")
    print(f"  Source Items: {len(source_items)}")
    print(f"  Producer Delay: {producer_delay}s")
    print(f"  Consumer Delay: {consumer_delay}s")
    print()
    
    # Create components
    print("Creating components...")
    queue = BoundedBlockingQueue[str](queue_capacity)
    source = SourceContainer[str](source_items)
    destination = DestinationContainer[str]()
    
    print(f"  Queue created with capacity: {queue.capacity()}")
    print(f"  Source container created with {source.size()} items")
    print(f"  Destination container created")
    print()
    
    # Create producer and consumer threads
    print("Creating threads...")
    producer = Producer(
        source=source,
        queue=queue,
        name="Producer-1",
        delay=producer_delay
    )
    
    consumer = Consumer(
        queue=queue,
        destination=destination,
        name="Consumer-1",
        delay=consumer_delay,
        sentinel="STOP"
    )
    
    print(f"  Producer thread created: {producer.name}")
    print(f"  Consumer thread created: {consumer.name}")
    print()
    
    # Start threads
    print("Starting threads...")
    print("-" * 60)
    consumer.start()
    producer.start()
    
    # Wait for producer to finish
    producer.join()
    print("-" * 60)
    print(f"Producer thread finished")
    
    # Wait a bit to ensure all items are consumed
    import time
    time.sleep(0.5)
    
    # If queue is not empty, wait for consumer to finish consuming items
    while queue.size() > 0:
        time.sleep(0.1)
    
    # Put a sentinel value to signal consumer to stop
    # This will wake up consumer if it's waiting for items
    try:
        queue.put("STOP", timeout=0.1)
    except:
        pass
    
    # Wait for consumer to finish (it will stop when it receives the sentinel)
    consumer.join()
    
    # Remove sentinel from queue if it's still there (consumer doesn't store it)
    if queue.size() > 0:
        try:
            queue.get(timeout=0.1)
        except:
            pass
    print(f"Consumer thread finished")
    print()
    
    # Display results
    print("=" * 60)
    print("Results")
    print("=" * 60)
    print(f"Items in source container: {source.size()}")
    print(f"Items produced: {producer.get_items_produced()}")
    print(f"Items consumed: {consumer.get_items_consumed()}")
    print(f"Items in destination container: {destination.size()}")
    print(f"Items remaining in queue: {queue.size()}")
    print()
    
    print("Source items:")
    print(f"  {source.get_all_items()}")
    print()
    
    print("Destination items:")
    dest_items = destination.get_all_items()
    print(f"  {dest_items}")
    print()
    
    # Verify correctness
    print("Verification:")
    if producer.get_items_produced() == consumer.get_items_consumed() == destination.size():
        print("  ✓ All items successfully transferred from source to destination")
    else:
        print("  ✗ Item count mismatch!")
    
    if set(source.get_all_items()) == set(dest_items):
        print("  ✓ All source items match destination items")
    else:
        print("  ✗ Item mismatch between source and destination!")
    
    print()
    print("=" * 60)
    print("Program completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

