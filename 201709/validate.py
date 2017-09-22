from OldCodes import makeX
from ooutils.io import loadJson, load
import os
from algorithm.decomposition import *
from algorithm.stats import stats
from algorithm.Methods import methods
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
import pandas as pd
import numpy as np
from typing import Dict, Tuple
model = lambda x: loadJson(f'./Models/pythonMd-{x}.json')
ontology_index = load('ontology_index')
entities       = load('entities')

def validateOn(fitMethod:str, decomp:str , model_name:str):
    Model: Dict[str, Tuple[Dict[int, float]]] = model(model_name)
    decomper = eval(decomp)
    saver    = []
    path     = f"results/{model_name}/{decomp}/{fitMethod}"
    try:
        os.makedirs(path)
    except:pass
    for entity, relatedEntities, referedOntologies in entities:
        stats_to_here = f"{path}/{entity}"
        pos_datas         = list(relatedEntities)
        neg_datas         = []
        total_pos     = len(pos_datas)
        total_neg     = 0
        targets       = np.hstack((np.ones((total_pos,)), np.zeros((total_pos,))))
        for neg_entity, neg_ref_ontos in ontology_index.items():
            if not neg_ref_ontos.isdisjoint(referedOntologies) and neg_entity not in relatedEntities:
                neg_datas.append(neg_entity)
                total_neg += 1
                if total_neg == total_pos:break

        shuffled = np.random.permutation(2*total_pos)
        pos_vecs, neg_vecs = makeX([Model[pos_data] for pos_data in pos_datas],
                                   [Model[neg_data] for neg_data in neg_datas])
        ori_names         = np.hstack((pos_datas, neg_datas))
        datas             = np.vstack((pos_vecs, neg_vecs))
        datas_shuffled    = np.take(datas, shuffled, axis=0)
        targets_shuffled  = np.take(targets, shuffled, axis=0)
        ori_names_shuffled= np.take(ori_names, shuffled, axis=0)
        if hasattr(methods[fitMethod], "isCluster"):
            train_X = datas_shuffled
            train_y = test_y = targets_shuffled
            std     = Normalizer()
            train_X = std.fit_transform(train_X)
            train_X, test_X = decomper(train_X, train_y)(train_X, train_X)
            ori_names_test  = ori_names_shuffled

        else:
            train_X, test_X, \
            train_y, test_y, \
            _, ori_names_test = train_test_split(datas_shuffled,
                                                 targets_shuffled,
                                                 ori_names_shuffled,
                                                 test_size = 0.33)
            std=Normalizer()
            std.fit(train_X);train_X=std.transform(train_X);test_X=std.transform(test_X)
            train_X, test_X = decomper(train_X, train_y)(train_X, test_X)
        clf = methods[fitMethod]()
        clf.fit(train_X, train_y)
        y_pred = clf.predict(test_X)
        res, details=stats(test_y, y_pred)
        df_results = pd.DataFrame( [
                                    ori_names_test[details.TP],
                                    ori_names_test[details.TN],
                                    ori_names_test[details.FP],
                                    ori_names_test[details.FN],
                                   ]
                                   ).T
        df_results.columns = ('TP','TN','FP','FN')
        df_results.fillna(value = "").to_csv(f"{stats_to_here}.csv", index=False, encoding='utf8')
        print(entity,' / ', fitMethod )
        print(pd.Series(res))
        res['fitMethod']  = fitMethod
        res['fromEntity'] = entity
        saver.append(res)
    database              = pd.DataFrame(saver)
    database.fillna(value = "").to_csv(f"{path}.csv", index=False, encoding='utf8')



