import multiprocessing as mp
import time, os, random


def f(n):
    print(os.getpid(), "Start ", time.perf_counter())
    for i in range(0, 100000000):
        random.random()
    print(os.getpid(), "End ", time.perf_counter())

"""
def g(f, a, l):
    for i in range(10):
        avail = 0
        temp = []
        while avail == 0:
            l.acquire()
            print("Lock acquired (Consumer)", time.perf_counter())
            try:
                if f.value == 1:
                    print("Consuming data (batch: ", i, ")", time.perf_counter())
                    for i in range(len(a)):
                        temp.append(a[i])
                    f.value = 0
                    avail = 1
                    print("Data consumed", time.perf_counter())
                else:
                    print("Consumer Sleeping", time.perf_counter())
                    time.sleep(1)
            finally:
                l.release()
                print("Lock Released (Consumer)", time.perf_counter())
        for j in range(10):
            print(temp[j])
        print("Artificial wait start (Consumer)", time.perf_counter())
        for _ in range(10000000):
            random.random()
        print("Artificial wait end (Consumer)", time.perf_counter())
"""

def g(l, v, c):
    for i in range(10):
        print('Consumption Round: ', i, time.perf_counter())
        consumed = 0
        while consumed == 0:
            l.acquire()
            print("Consumer acquired", time.perf_counter())
            try:
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
    """
	start = time.perf_counter()

	f(1)
	#f()

	end = time.perf_counter()

	print('Sequential: ', end-start)

	start2 = time.perf_counter()

	p = mp.Process(target=f, args=(1,))
	q = mp.Process(target=f, args=(2,))
	#r = mp.Process(target=f, args=(3,))
	#s = mp.Process(target=f, args=(4,))

	p.start()
	q.start()
	#r.start()
	#s.start()
	p.join()
	q.join()
	#r.join()
	#s.join()

	end2 = time.perf_counter()

	print('Multiprocess: ', end2-start2)
	"""


    start = time.perf_counter()

    l = mp.Lock()
    v = mp.Value('d', 0)
    parent, child = mp.Pipe()
    p = mp.Process(target=g, args=(l, v, child))
    p.start()
    for i in range(10):
        print('Production Round: ', i, time.perf_counter())
        product = random.random()
        for _ in range(10000000):
            random.random()
        produced = 0
        while produced == 0:
            l.acquire()
            print("Producer acquired", time.perf_counter())
            try:
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


    """
    start = time.perf_counter()

    flag = mp.Value('d', 0)
    arr = mp.Array('d', range(10))
    lock = mp.Lock()
    p = mp.Process(target=g, args=(flag, arr, lock))

    p.start()
    for i in range(10):
        available = 0
        temp = []
        for _ in range(10):
            temp.append(random.random())
        while available == 0:
            lock.acquire()
            print("Lock acquired (Producer)", time.perf_counter())
            try:
                if flag.value == 0:
                    print("Producing data (batch: ", i, ")", time.perf_counter())
                    for j in range(len(arr)):
                        arr[j] = temp[j]
                    available = 1
                    flag.value = 1.0
                    print("Data produced", time.perf_counter())
                else:
                    print("Producer Sleeping", time.perf_counter())
                    time.sleep(1)
            finally:
                lock.release()
                print("Lock released (Producer)", time.perf_counter())
        print("Artificial wait start (Producer)", time.perf_counter())
        for _ in range(0, 10000000):
            random.random()
        print("Artificial wait end (Producer)", time.perf_counter())
    p.join()

    end = time.perf_counter()

    print('with MP', end - start)
    """