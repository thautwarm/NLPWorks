from validate import validateW2COn
from gensim.models import Word2Vec
from algorithm.Methods import  methods
src= "/home/hz/Desktop/lem/mode5100l.w2c"
Model = Word2Vec.load(src)
for method_name in methods:
        validateW2COn(method_name, Model)
