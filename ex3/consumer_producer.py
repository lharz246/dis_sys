import threading
import time
from queue import Queue
import random

shared_queue = Queue()
queue_lock = threading.Lock()


class Producer:

    def __init__(self, even, id):
        self.even = even
        self.id = id
        self.item_counter = 10

    def run(self, counter):
        print(f"Producer {self.id} started")
        while counter < self.item_counter:
            sleeping = random.randint(0, 1)
            item = {"id": self.id, "item": random.randint(0, 100)}
            queue_lock.acquire(blocking=True)
            shared_queue.put(item)
            queue_lock.release()
            counter += 1
            time.sleep(sleeping)


def consume():
    print("start")
    counter = 0
    while counter < 20:
        prodcued_item = shared_queue.get()
        print(f"Producer: {prodcued_item['id']} sent {prodcued_item['item']}")
        counter += 1


prod1 = Producer(True, 1)
prod2 = Producer(False, 2)

prod1_thread = threading.Thread(target=prod1.run, args=(0,))
prod2_thread = threading.Thread(target=prod2.run, args=(0,))
consumer_thread = threading.Thread(target=consume)

prod1_thread.start()
prod2_thread.start()
consumer_thread.start()
prod1_thread.join()
prod2_thread.join()
consumer_thread.join()
