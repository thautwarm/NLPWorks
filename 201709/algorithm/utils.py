# algorithm.py
import numpy as np
import pandas as pd
import os
from collections import deque
from freestyle.collections import richIterator, block, globals_manager, op, richList

class manager(dict):
    def __init__(self, *args, **kwargs):
        super(manager, self).__init__(*args, **kwargs)
        for key in self.keys():
            setattr(self, key, self[key])


def getCSVInfo(path):
    df = pd.read_csv(path)
    return manager(path=path, source=df, length=df.shape[0])



# other kind of surpport functions
def makedir_from(file):
    try:
        os.makedirs(file[:file.rfind("/") + 1])
    except:
        pass
