from validate import validateOn, model
from algorithm.Methods import  methods
from algorithm.decomposition import nameAssemble
for gram in ('gram-1', 'gram-2','gram-3','gram-mix'):
    for decomp in nameAssemble:
        for method_name in methods:
            validateOn(method_name, decomp, gram)
