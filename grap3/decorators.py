import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        end = time.time()
        print ('Executed %s in %2.2f seconds' % (func.__name__, end - start))
        return rv
    return wrapped
