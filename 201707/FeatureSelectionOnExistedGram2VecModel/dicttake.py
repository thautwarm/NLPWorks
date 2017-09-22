import json
import sys,os

methods = ['entropy','relief','corr']

class FeatureSelection:
    def go(env):

        maxNum = 0

        def calMax(x):
            nonlocal maxNum
    
            if maxNum < x:
                maxNum = x


        def unitAction(x):
            a,b = x
            calMax(a)
            return f"{a} {b}"



        def makeAttr(n):
            return "@attribute @@class@@ {a} \n"+'\n'.join(["@attribute '%d' numeric"%i for i in range(n)])

        def ARffToJSON(keys,filename):
            haskmap=lambda *x:list(map(*x))
            haskfil=lambda *x:list(filter(*x))
            haskzip=lambda *x:list(zip(*x))
            import gc
            with open(filename,'r',encoding='utf8') as f:
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
                   return  haskmap(lambda x: haskzip(*haskfil(lambda x:x,haskmap(structure,x[1:-1].split(',')))),datas)
            datas=parser(datas)
            gc.collect()
            dic=dict(zip(keys,datas))
            return dic


        with open( env.JSONFileName ,encoding='utf8') as f:
            dic1 = json.load(f)
        print(f"has loaded {env.JSONFileName} ...")
        keys = dic1.keys()
        dic2 = "@data\n"+"\n".join(  map(lambda x: "{{{vector}}}".format ( vector = ",".join(map(unitAction, filter(lambda x: x[0]!=0 ,zip(*dic1[x]) )  )  ) ), dic1) )
        Attrs = makeAttr(maxNum)
        print("has parser the json to arff yet ...")

        content =\
f"""@relation ""

{Attrs}

{dic2}
"""
        with open( env.to_ArffFileName ,'w',encoding='utf8') as f:
            f.write(content)
        with open(env.jarRunFileName,encoding='utf8') as f:
            cmd = f.read().format(filename = env.to_ArffFileName , selectNum = env.selectFeatureNum )
        print(f'doing the cmd codes \n {cmd}  \n...')
        os.system(cmd)

        outPutFileNames = list( map(lambda suffix: f"{env.to_ArffFileName}_{suffix}", methods) )
        print(f"ready to write new json model to the files with feature selection methods {methods} . \n {outPutFileNames}")
        for filename in outPutFileNames:
                outDic = ARffToJSON(keys,filename)
                with open(filename+".json",'w',encoding='utf8') as f:
                    json.dump(outDic,f)
                os.remove(filename)
                print(f'one method has done : {filename}')
        os.remove(env.to_ArffFileName)

class Env:
    def __init__(self, jarRunFileName="javaRun.bat",JSONFileName= None,to_ArffFileName =None,
                            selectFeatureNum = None):
        self.jarRunFileName=jarRunFileName #"javaRun.bat"
        self.JSONFileName  =JSONFileName #sys.argv[1]
        self.to_ArffFileName=to_ArffFileName #sys.argv[2]
        self.selectFeatureNum=selectFeatureNum #int(sys.argv[3])


if __name__ == "__main__":

    with open(sys.argv[1]) as f:
        configs = json.load(f)
    for config in configs:
        print("task now:\n",config)
        FeatureSelection.go(Env(**config))
        














    
    






