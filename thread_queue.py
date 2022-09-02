import threading, queue
import os
import torch

# define a function to receive data from the producer, and perform a task.
def consumer(q, error_q):
    # print the Consumer's process ID. In contrast to multi-processing, we expect
    # this process ID to be the same as the producer's process ID.
    print("Consumer Process ID: ", os.getpid())

    # define a counter to keep track of how many iterations we have run
    i = 0
    # continually run the task we wish the consumer to perform, until we receive
    # a message from the producer telling us to stop
    while True:
        # utilize "try-except" here to catch any exceptions and prevent hangs.
        try:
            # check the error queue to see if the producer encountered an error.
            # If the producer did encounter an error, break the loop, which will bring
            # this function to its end.
            if error_q.qsize() > 0:
                err = error_q.get()
                if err == 'Error': break

            product = q.get()
            if product == 'done': break

            # print the object ID of the product we have received. We expect this ID
            # to be the same as the ID printed by the producer. If it is, it means
            # that the data put in queue was not copied, and thus did not take
            # additional memory space.
            print("Consumer Product ", i, " ID: ", id(product))

            # print the product that we received, to check if it matches the product
            # the producer sent.
            print("Product ", i, ": ", product)
            i += 1
            if i == 4: print(doesnotexist)
        # If an error occurs, send a message to the producer to let them know an error
        # has occurred, and then raise the error.
        except:
            print("An exception occurred")
            error_q.put("Error")
            raise



# define a function to generate products to send to the consumer
def producer(q, n, error_q):
    # print the Producer's process ID. In contrast to multi-processing, we expect
    # this process ID to be the same as the consumer's process ID.
    print("Producer Process ID: ", os.getpid())

    # loop through a predetermined number of iterations, producing some data each
    # time, and sending it to the consumer via a queue.
    for i in range(n):
        # utilize "try-except" here to catch any exceptions and prevent hangs.
        try:
            # check the error queue to see if the consumer encountered an error.
            # If the consumer did encounter an error, break the loop, which will bring
            # this function to its end.
            if error_q.qsize() > 0:
                err = error_q.get()
                if err == 'Error': break

            product = torch.tensor([i,2,3]) if i % 2 == 0 else torch.tensor([i, 4, 5])

            # print the object ID of the product we have generated. We expect this ID
            # to be the same as the ID printed by the consumer> If it is, it means that
            # the data put in the queue was not copied, and thus did not take additional
            # memory space.
            print("Producer Product ", i, " ID: ", id(product))
            q.put(product)
        except:
            print("An exception occurred")
            error_q.put("Error")
            raise

    # once we have generated all the data we want, send a message to the consumer
    # telling it that the task has been completed.
    queue.put('done')