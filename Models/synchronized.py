import functools

# Cada DAO concreta ira implementar seu proprio _lock
def synchronized(metodo):
    @functools.wraps(metodo)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return metodo(self, *args, **kwargs)
    return wrapper