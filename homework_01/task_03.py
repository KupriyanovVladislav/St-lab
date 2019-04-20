class FibIterator:
    def __iter__(self):
        return self

    def __init__(self):
        self.current, self.next = 0, 0
        self.counter = 0

    def __next__(self):
        self.counter += 1
        if self.counter > 100:
            raise StopIteration
        if self.next == 0 and self.current == 0:
            self.next = 1
            return 0
        self.current, self.next = self.next + self.current, self.current
        return self.current


def fib_generator():
    current, following = 0, 1
    yield current
    counter = 1
    while counter < 100:
        current, following = following + current, current
        counter += 1
        yield current


def strange_decorator(func):
    def wrapped(*args, **kwargs):
        if len(args)+len(kwargs) > 10:
            raise ValueError
        for arg in kwargs.values():
            print(arg)
            if isinstance(arg, bool):
                raise TypeError
        a = func(*args, **kwargs)
        if isinstance(a, int):
            a += 13
        return a
    return wrapped
