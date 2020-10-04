from contextlib import contextmanager
import time


@contextmanager
def timeit(description: str):
    start = time.time()
    yield
    took = time.time() - start
    print(f"{description} took {took}")
