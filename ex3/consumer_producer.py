import threading
import json
from queue import Queue
import random

# Shared queue for communication between producers and consumers, with a limit on its size.
shared_queue = Queue(maxsize=10)

class Producer:
    def __init__(self, producer_id, max_items=20):
        self.producer_id = producer_id
        self.max_items = max_items

    def produce_items(self, start_count=0):
        """Produces a specified number of items and adds them to the shared queue."""
        print(f"Producer {self.producer_id} started")
        counter = start_count
        while counter < self.max_items:
            try:
                item = {
                    "producer_id": self.producer_id,
                    "item": random.randint(0, 100)
                }
                serialized_item = json.dumps(item)

                # Add the item to the queue.
                shared_queue.put(serialized_item)
                print(f"Producer {self.producer_id} produced item: {item['item']}")

                counter += 1
            except Exception as e:
                print(f"Error in Producer {self.producer_id}: {e}")
        
        print(f"Producer {self.producer_id} finished")

def consume_items():
    """Consumes items from the shared queue until a termination signal is received."""
    print("Consumer started")
    while True:
        try:
            # Retrieve an item from the queue.
            serialized_item = shared_queue.get()

            # Check for the termination signal.
            if serialized_item is None:
                print("Consumer received termination signal")
                break

            # Deserialize and process the item.
            item = json.loads(serialized_item)
            print(f"Consumer received item from Producer {item['producer_id']}: {item['item']}")
        except json.JSONDecodeError:
            print("Error decoding item, skipping...")
        except Exception as e:
            print(f"Error in Consumer: {e}")

def run_producer_consumer_system(num_producers=3, num_consumers=2, max_items_per_producer=20):
    """Runs a producer-consumer system with the specified number of producers and consumers."""
    
    # Create producer threads.
    producers = [Producer(i + 1, max_items_per_producer) for i in range(num_producers)]
    producer_threads = [
        threading.Thread(target=producer.produce_items) for producer in producers
    ]

    # Create consumer threads.
    consumer_threads = [
        threading.Thread(target=consume_items) for _ in range(num_consumers)
    ]

    # Start all producer threads.
    for thread in producer_threads:
        thread.start()

    # Start all consumer threads.
    for thread in consumer_threads:
        thread.start()

    # Wait for all producer threads to finish.
    for thread in producer_threads:
        thread.join()

    # Send a termination signal for each consumer.
    for _ in range(num_consumers):
        shared_queue.put(None)

    # Wait for all consumer threads to finish.
    for thread in consumer_threads:
        thread.join()

    print("All producers and consumers have finished.")

# Example usage:
if __name__ == "__main__":
    # Configure the number of producers, consumers, and max items per producer.
    run_producer_consumer_system(num_producers=2, num_consumers=1, max_items_per_producer=20)
