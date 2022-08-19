import threading, queue
import os
import torch

def consumer(queue):
    print("Consumer Process ID: ", os.getpid())
    i = 0
    while True:
        product = queue.get()
        if product == 'done': break

        print("Consumer Product ", i, " ID: ", id(product))

        print("Product ", i, ": ", product)
        i += 1

def producer(queue):
    print("Producer Process ID: ", os.getpid())
    for i in range(10):
        product = torch.tensor([i,2,3]) if i % 2 == 0 else torch.tensor([i, 4, 5])

        print("Producer Product ", i, " ID: ", id(product))
        queue.put(product)

    queue.put('done')


if __name__ == '__main__':

    queue = queue.Queue()
    consumer_t = threading.Thread(target=consumer, args=(queue,))

    consumer_t.start()
    producer(queue)
    consumer_t.join()