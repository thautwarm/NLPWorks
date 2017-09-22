
# test for freestyle.py
from freestyle.collections import richIterator, globals_manager, op, lisp
globals_manager(globals())
class richList(richIterator, list):
    pass
from numpy.random import randn
var = richList(randn(5))
print(var.map(lambda x: x + 1))
print(var.tolist())
print(var@(lambda x: x.tolist() + ['end']))
print(var.let(c=1).then(list, lisp(map, lambda v: v + c, this)))


# test for stats.getSample
from stats import getSample
from sklearn.datasets import load_iris
import pandas as pd
sets = load_iris()
D = pd.DataFrame(sets.data, columns=['a', 'b', 'c', 'd'])
print(getSample(D, 5, 'a', 'b'))

