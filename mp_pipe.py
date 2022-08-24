import multiprocessing as mp
import time, os, random


# Define a function to act as the consumer
def g(l, v, c):
    # Run a predetermined number of loops of consuming data.
    for i in range(10):
        print('Consumption Round: ', i, time.perf_counter())
        # set a value to ensure data was received and consumed. Then run a loop
        # that does not end until data has been consumed.
        consumed = 0
        while consumed == 0:
            l.acquire()
            print("Consumer acquired", time.perf_counter())
            try:
                # if the number of objects in the Pipe is less than or equal to 0
                # we cannot receive anything, and thus will not call the receive
                # function. If we do, we can potentially continue holding onto the
                # lock, never allowing the producer to acquire it and add data to
                # the pipe. Once we have received the data, print it and set the
                # indicator to indicate that data has been consumed. Then decrement
                # the shared Value to denote that there is one less object in the pipe.
                if v.value > 0:
                    print(c.recv())
                    for _ in range(10000000):
                        random.random()
                    consumed = 1
                    v.value -= 1
                    print("Consumed", time.perf_counter())
            finally:
                l.release()
                print("Consumer released", time.perf_counter())
            if consumed == 0:
                print("Consumer Sleeping", time.perf_counter())
                time.sleep(1)




if __name__ == '__main__':

    start = time.perf_counter()

    # Define a Lock (to control access to the Pipe), a Value (representing the
    # number of objects in the pipe), a Pipe, and a Process.
    l = mp.Lock()
    v = mp.Value('d', 0)
    parent, child = mp.Pipe()
    p = mp.Process(target=g, args=(l, v, child))

    p.start()
    # Run a loop a predetermined number of times to produce random data
    for i in range(10):
        print('Production Round: ', i, time.perf_counter())
        product = random.random()
        for _ in range(10000000):
            random.random()
        # define a variable to determine whether or not the producer has sent
        # the data it produced. Then run a loop where the producer attempts
        # to send the data to the consumer.
        produced = 0
        while produced == 0:
            l.acquire()
            print("Producer acquired", time.perf_counter())
            try:
                # We only send the data if the number of items in the pipe is less
                # than a certain amount. Once we send, we changed "produced" to
                # indicate that we have sent, and increase the shared Value that
                # stores the number of objects in the pipe.
                if v.value < 10:
                    parent.send(product)
                    produced = 1
                    v.value += 1
                    print("Produced", time.perf_counter())
            finally:
                l.release()
                print("Producer Released", time.perf_counter())
            if produced == 0:
                print("Producer Sleeping", time.perf_counter())
                time.sleep(1)
    p.join()

    end = time.perf_counter()

    print('With MP: ', end - start)
