# logicMain_rewrite.py

from pack_imp import *
from config import Test , getW2V, makeData
from algorithm.decomposition import *
import sys
if len(sys.argv)>1:
    desktop, model_type, decomp_method ,  root_dir = sys.argv[1:]
    decomp_method = eval(decomp_method)
else:
    desktop, model_type, decomp_method, root_dir = '../','2gram',de_rf ,'./results'


W2V = getW2V(version_name = model_type)

Data = makeData(desktop = desktop)

Test(W2V,Data,decomp_method,root_dir)
