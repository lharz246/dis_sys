import threading
import time
import json
from queue import Queue
import random

# Shared queue for communication between producers and consumers, with a limit on its size.
shared_queue = Queue(maxsize=10)

class Producer:
    def __init__(self, producer_id):
        self.producer_id = producer_id
        self.max_items = 20

    def produce_items(self, start_count=0):
        """Produces a specified number of items and adds them to the shared queue."""
        print(f"Producer {self.producer_id} started")
        counter = start_count
        while counter < self.max_items:
            try:
                # Simulate the production of an item with a random delay.
                sleep_duration = random.uniform(0.1, 1.0)
                item = {
                    "producer_id": self.producer_id,
                    "item": random.randint(0, 100)
                }
                serialized_item = json.dumps(item)

                # Add the item to the queue.
                shared_queue.put(serialized_item)
                print(f"Producer {self.producer_id} produced item: {item['item']}")

                counter += 1
                time.sleep(sleep_duration)
            except Exception as e:
                print(f"Error in Producer {self.producer_id}: {e}")
        
        # Signal the end of production for this producer.
        shared_queue.put(None)
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

# Create and start producer threads.
producers = [Producer(i + 1) for i in range(3)]
producer_threads = [
    threading.Thread(target=producer.produce_items) for producer in producers
]

# Create and start consumer threads.
consumer_threads = [
    threading.Thread(target=consume_items) for _ in range(2)
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

# Send termination signals to consumers once all producers are done.
for _ in range(len(consumer_threads)):
    shared_queue.put(None)

# Wait for all consumer threads to finish.
for thread in consumer_threads:
    thread.join()

print("All producers and consumers have finished.")
