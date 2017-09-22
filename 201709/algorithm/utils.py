# algorithm.py
import numpy as np

class manager(dict):
    def __init__(self, *args, **kwargs):
        super(manager, self).__init__(*args, **kwargs)
        for key in self.keys():
            setattr(self, key, self[key])

