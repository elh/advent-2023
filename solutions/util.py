import time


def timed(fn):
    start_t = time.time()
    res = fn()
    print("time:", time.time() - start_t)
    return res
