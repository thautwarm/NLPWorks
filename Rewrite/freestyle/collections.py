from typing import List, Dict, Any
from collections import defaultdict, deque
import pandas as pd
import numpy as np
import numba as nb
from copy import deepcopy
from functools import reduce

class op:
    @staticmethod
    def mul(a, b): return a * b


    def sub(a, b): return a - b


    def add(a, b): return a + b


    def div(a, b): return a / b


    def mod(a, b): return a % b


    def anno(a, b): return a@b


    def e_method(method, a, b): return eval(f"a.{method}(b)")


    def e_func(func, a, b): return eval(f"{func}(a,b)")


class block:
    pass


class globals_manager:
    def __new__(self, global_vars=None):
        try:
            if not global_vars:
                return self.globals_
            else:
                self.globals_ = global_vars
                return self.globals_
        except AttributeError:
            self.globals_ = global_vars


def lisp(*targs, **kwargs):
    argNums = len(targs)
    if not argNums:
        return None
    elif argNums is 1:
        value, = targs
        return value
    else:
        f, *ttargs = targs
        ttargs = map(lambda x: lisp(x), ttargs)
        kw = dict(map(lambda x: (x, lisp(kwargs[x])), kwargs))
        return f(*ttargs, **kw)


class richIterator:
    def __init__(self, *args, **kwargs):
        super(richIterator, self).__init__(*args, **kwargs)
        self.recovery_vars = {}

    def filter(self, f):
        return richGenerator((each for each in self if f(each)))

    def recovery(self):
        globals_vars = globals_manager()
        if self.recovery_vars:
            recovery_vars = self.recovery_vars
            for key in recovery_vars:
                globals_vars[key] = recovery_vars[key]

    def __matmul__(self, f):
        return f(self)

    def groupBy(self, f, containerType=list):
        if containerType is list:
            res: Dict[Any, eval("self.__class__")] = defaultdict(
                eval("self.__class__"))
            for each in self:
                res[f(each)].append(each)
        elif containerType is set:
            res: Dict = dict()
            for each in self:
                key = f(each)
                if key not in res:
                    res[key] = each
        else:
            return TypeError(f"method .groupBy for containerType '{containerType}'\
                             is not defined yet,\
                             you can define it by yourself.")
        return richDict(res)

    def let(self, **kwargs):
        globals_vars = globals_manager()
        if 'this' not in kwargs:
            kwargs['this'] = self
        for key in kwargs:
            if key in globals_vars:
                value = globals_vars[key]
                self.recovery_vars[key] = value if value != "this" else self
            value = kwargs[key]
            globals_vars[key] = value if value != "this" else self
        return self

    def then(self, *args, **kwargs):
        ret = lisp(*args, **kwargs)
        self.recovery()
        return ret

    def map(self, f, *args, **kwargs):
        args = (self,) + args
        return richIterator.thenMap(f, *args, **kwargs)

    def mapIndexed(self, f: "function<Int,T>", *args, **kwargs):
        args = (range(len(self)), self) + args
        return richIterator.thenMap(f, *args, *kwargs)
    def connectedWith(self, *cases:tuple):
        def test(item):
            for case_judge, case_action in cases[:-1]:
                if case_judge(item) is True:
                    return case_action(item)
            return cases[-1](item)
        return richGenerator(map(test, self))

    def tolist(self):
        return [each for each in self]

    def totuple(self):
        return tuple(each for each in self)

    def toset(self):
        return set(self)

    def todict(self):
        return dict(self)

    def zip(self, iterator):
        return richGenerator(zip(self, iterator))

    def togen(self):
        return richGenerator(self)

    @staticmethod
    def thenMap(f, *args, **kwargs):
        if kwargs:
            kwargsKeys = kwargs.keys()
            kwargsValues = zip(* kwargs.values())
        args = zip(*args)
        if kwargs:
            return richGenerator(f(*arg, **dict(zip(kwargsKeys, kwargsValue))) for arg, kwargsValue in zip(args, kwargsValues))
        else:
            return richGenerator(f(*arg) for arg in args)


class generator:
    def __init__(self, iterable):
        self.obj = iterable

    def __iter__(self):
        for each in self.obj:
            yield each

    def togen(self):
        return self.obj


class richGenerator(richIterator, generator):pass

class richDict(richIterator, dict):pass

class richList(richIterator,list):pass
