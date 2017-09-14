from collections import defaultdict
from functools import reduce

def andthen(*func_stack):
    def _1(*args, **kwargs):
        for func in func_stack:
            try:
                mid=func(mid)
            except NameError:
                mid=func(*args, **kwargs)
        return mid

    return _1


def compose(*func_stack):
    def _1(*args, **kwargs):
        for func in func_stack[::-1]:
            try:
                mid=func(mid)
            except NameError:
                mid=func(*args, **kwargs)
        return mid

    return _1


def foreach(f: object) -> callable:
    def _1(self):
        for item in self:
            f(item)

    return _1


def groupBy(func : callable) -> defaultdict(list):
    def _1(self):
        that=defaultdict(list)
        foreach(lambda item: that[func(item)].append(item)) \
            (self)
        return that
    return _1

def flatten(seq:list):
    def _f():
        for item in seq:
            if not isinstance(item, list):
                yield item
            else:
                yield from _f(item)
    return _f()


def _flatten(seq: list):
    """
    this is the implementation of function flatten without recursion.
    """
    head=[]
    tmp=seq
    idx=[0]
    while True:
        try:
            item=tmp[idx[-1]]
        except IndexError:
            try:
                tmp=head.pop()
                idx.pop()
                continue
            except IndexError:
                break
        idx[-1]+=1
        if not isinstance(item, list):
            yield item
        else:
            head.append(tmp)
            tmp=item
            idx.append(0)

def __flatten(seq: list):
    """
    this is the implementation of function flatten without recursion.
    """
    head=[]
    store=[]
    tmp=seq
    idx=[0]
    while True:
        try:
            item=tmp[idx[-1]]
        except IndexError:
            try:
                tmp=head.pop()
                idx.pop()
                continue
            except IndexError:
                break
        idx[-1]+=1
        if not isinstance(item, list):
            store.append(item)
        else:
            head.append(tmp)
            tmp=item
            idx.append(0)
    return store



class fn:
    map    = lambda f : lambda *args  : map(f, *args)
    filter = lambda f : lambda *args  :filter(f, *args)
    reduce = lambda f : lambda *args  :reduce(f, *args)
    flatMap= lambda f : andThen(flatten, fn.map(f))
    pass
flatten.noRecur = _flatten
flatten.noRecur.strict = __flatten





