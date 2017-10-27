from validate import validateW2COn
from gensim.models import Word2Vec
from algorithm.Methods import  methods
src= "/home/hz/Desktop/lem/mode5100l.w2c"
Model = Word2Vec.load(src)
validateW2COn('SVM-linear', Model)
