# -*- coding: utf-8 -*-
"""
Created on Fri May 19 11:26:59 2017

@author: thautwarm
"""

import os,gc,sys,pickle,json
strict_map=lambda *x:list(map(*x))
strict_filter=lambda *x:list(filter(*x))
strict_zip=lambda *x:list(zip(*x))

"""
"Path" is the filename of root of training datas in the weka format
    like 
        -"training-data-root"
            -class1
                -instance1.txt
                -instance2.txt
                -instance3.txt
                ...
            -class2
                -instances1.txt
                -instance2.txt
                -instance3.txt
                ...
            ...
            
"WekaResults" is the filename of results about dealing with the training datas by using W2C.java.
"W2Cmodel" is the filename of output W2C-model which be used in Python like gensim.models.Word2Vec
"""



Path=sys.argv[1] 
WekaResults=sys.argv[2]
W2Cmodel=sys.argv[3]

dirs= strict_map(lambda x:"%s/%s"%(Path,x),os.listdir(Path))
entities=sum(map(lambda x: strict_filter(lambda x:x[-3:]=='txt',os.listdir(x) ),dirs),[])
entities=strict_map(lambda x: x[:-4],entities)




with open(WekaResults,'r') as f:
    datas=f.read()
datas=datas[datas.index('@data')+6:]
gc.collect()
def tryfloat(x):
    try:
        return float(x)
    except:
        return 0.0
datas=datas.split('\n')
gc.collect()
def structure(tuples):
    try:
        a,b=tuples.split(' ')
    except:
        return None
    return int(a),tryfloat(b)
def parser(datas):
   return  strict_map(lambda x: dict(filter(lambda x:x,map(structure,x[1:-1].split(',')))), datas)
datas=parser(datas)
gc.collect()
dic=dict(zip(entities,datas))
with open(W2Cmodel,'w',encoding='utf-8') as f:
    json.dump(dic,f)
#from sklearn.externals import joblib
#indices,values=list(zip(*datas))
#N=len(indices)
#ids=[]
#vs=[]
#k=[]
#from itertools import repeat
#N=len(datas)
#for i,(index,value) in enumerate(datas):
#    
#    print(i/N ) if i %1000 else None
#    ids+=list(index)
#    vs+=list(value)
#    k+=list(repeat(0,len(ids)))
#    gc.collect()
#ids=sum(strict_map(lambda x:list(x),ids),[])
#vs=sum(strict_map(lambda x:list(x),vs),[])
#k=sum(strict_map(lambda x:list(x),k),[])
#datas=sparse.coo_matrix((vs,(k,ids)),shape=(1,81831))
#joblib.dump(dic,'./model/DictMd')
##发现共有29111重复


