from time import time
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import numpy as np
import pickle

def main():
    arr = np.ones((1024, 1024, 1024), dtype=np.uint8)
    expected_sum = np.sum(arr)

    with ThreadPool(1) as threadpool:
        start = time()
        assert (
            threadpool.apply(np.sum, (arr,)) == expected_sum
        )
        print("Thread pool:", time() - start)

    with mp.get_context("spawn").Pool(1) as processpool:
        start = time()
        assert (
            processpool.apply(np.sum, (arr,))
            == expected_sum
        )
        print("Process pool:", time() - start)

if __name__ == "__main__":
    main()
