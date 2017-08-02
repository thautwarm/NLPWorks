# config.py

from algorithm.utils import manager, getCSVInfo, np, makedir_from
from freestyle.collections import globals_manager,block,richIterator,richList

from algorithm.classifier import wrap, cluster
from sklearn.preprocessing import StandardScaler
from algorithm.stats import stats,undersampling  
import os
import sys
from pack_imp import *
from userdefine import gramModels
class getW2V:
    _model = None
    def __new__(self, version_name: {'mix', '1gram', '2gram', '3gram'}=None):
        if not self._model:
            self._model =  Word2Vec.load(gramModels[version_name])
            return self._model
        else:
            pass
        return self._model
    



# 便于可读性定义一些用作符号的变量
Ontology = 'ontology'
Instance = 'instance'
Path = 'path'
Datasets : np.array = 'datasets'
Word2vector_model = 'word2vector_model'
Experiment = 'experiment'
Manager = manager
Method  = 'method'
# =================
closure = globals_manager(globals())


traindata = '{desktop}/TrainDatas'
testdata =  '{desktop}/TestDataSets.csv'
stats_to_where = '{root_dir}/{ontology}/{method}'
def makeData(desktop:Path, debug = False)->[Manager, Manager]:
    test_path    = testdata.format(desktop = desktop)
    test:Manager = getCSVInfo(test_path)
    
    train_path   = traindata.format(desktop = desktop)
    
    initial_mac = dict()
    for ontology in os.listdir(train_path):
        csv_path     =  os.path.join( train_path, ontology, 'datas.csv')
        csv_manager : Manager  = getCSVInfo(csv_path)
        initial_mac[ontology]  = csv_manager
    train = manager(**initial_mac)
    return manager(test = test, train = train)



methods = {'Birch': wrap(cluster, lazy_clf=wrap(Birch, n_clusters=2)),
           'DecisionTree': DecisionTreeClassifier,
           'ExtraTree': ExtraTreesClassifier,
           'KMeans': wrap(cluster, lazy_clf=wrap(KMeans, n_clusters=2)),
           'KNeighborsClassifier': KNeighborsClassifier,
           'MeanShift': MeanShift,
           'Naive_Bayes': GaussianNB,
           'RandomForest': RandomForestClassifier,
           'SVM-rbf': wrap(SVC, probability=True),
           'Dummy': DummyClassifier}
cluster_kinds = ['Birch', 'KMeans', 'MeanShift']



def Test(W2V:Word2vector_model, Data:Manager, decomposition_method, root_dir:Path='results')->None:
    df_of_test : Manager = Data.test.source
    transform_ori_to_numeric : (Datasets,'->' ,Datasets)\
         =  lambda examples  : \
             richList(examples)\
                .map(lambda x: x.replace("DBPEDIA_ID/",""))\
                .map(lambda x: W2V[x]).let()\
                .then(np.array, this.tolist())  

    all_of_test_X : Datasets \
        = transform_ori_to_numeric(df_of_test.Example)  

    all_of_test_ori_y : Datasets \
        = df_of_test.classes.values

    all_of_test_ori_name : Datasets\
        = df_of_test.Example.values 

    # 获取所有instance数量大于20的ontology 作为 dataframe of train datas.
    
    dfs_of_train:Manager\
        = richList(Data.train.keys())\
                    .filter(lambda x :Data.train[x].length > 20)\
                    .map(lambda x:(x, Data.train[x]) ).let()\
                    .then(manager, this)
    inst_num_dist_for_training \
        = dict(richList(dfs_of_train).map(lambda ontology: (ontology, dfs_of_train[ontology].length) ))
    total_of_ontologies = sum(inst_num_dist_for_training.values())
    
    
    def search_negative_samples(except_ontology:Ontology, select_number:int , deepth=0) -> Datasets:
        indices = np.random.permutation( total_of_ontologies )[:select_number]
        
        cursor = iter(inst_num_dist_for_training.keys())
        right_summary = 0
        left_summary  = 0
        left_num = 0

        sample_ori = []
        sample_tag = []         
        for idx in sorted(indices):
            while idx >= right_summary:
                ontology = next(cursor)
                if ontology == except_ontology : 
                    num_inst = inst_num_dist_for_training[ontology]
                    left_summary  =  right_summary
                    right_summary += num_inst 
                    continue
                num_inst = inst_num_dist_for_training[ontology]
                right_summary += num_inst 
                left_summary  =  right_summary-num_inst 
                insts    = dfs_of_train[ontology].source
                examples = insts.Example.values
                tags     = insts.classes.values
            if ontology == except_ontology: 
                left_num += 1
                continue

            sample_ori.append(examples[idx - left_summary])
            sample_tag.append(    tags[idx - left_summary])
        
        if left_num == 0:
            return sample_ori, sample_tag
        else:
            sample_ori_left , sample_tag_left = search_negative_samples(except_ontology, left_num, deepth+1)
            return sample_ori+sample_ori_left, sample_tag+sample_tag_left
        
    def get_train_datas_from_ontology(ontology : Ontology)-> ['train_X','train_y','train_ori_name']:
        train_part1 = dfs_of_train[ontology].source.Example.values
        train_part2, maybe_neg_tags \
            = search_negative_samples(except_ontology = ontology, select_number = dfs_of_train[ontology].length)
        
        labels = richList(maybe_neg_tags).map(lambda classtag: ontology in classtag)\
                    .let(pos_num = len(train_part1))\
                    .then(np.hstack,  ( np.ones(pos_num, ), np.array(this.tolist()) ) )
                    
        train_datas  = np.hstack( (train_part1, train_part2) )
        numeric_datas = transform_ori_to_numeric(train_datas)
        return numeric_datas, labels, train_datas

    def get_test_datas_from_ontology(ontology : Ontology) -> ['test_X', 'test_y' ,'test_ori_name']:
        all_of_test_y = list(map(lambda classtag : ontology in classtag, all_of_test_ori_y) )
        return undersampling(all_of_test_X, all_of_test_y, all_of_test_ori_name)
    
    def Experiment_on_Classifier(method : Method, ontology : Ontology, stats_to_here:Path):
        
        # get test datas
        test_X,  test_y , test_ori_name   = get_test_datas_from_ontology(ontology)
        # get train datas
        train_X, train_y, train_ori_name  = get_train_datas_from_ontology(ontology)
        
        train_X, test_X = makeX( train_X, test_X ) 
        std = StandardScaler(); std.fit(train_X)
        train_X = std.transform(train_X); test_X = std.transform(test_X)
        
        # decomposition
        try:
            print(f'feature_num before decomposition :{test_X.shape[1]}')
            train_X_r, test_X_r = decomposition_method(train_X,train_y)(train_X, test_X)
            print(f'feature_num after decomposition :{test_X.shape[1]}')
            if train_X_r.shape[1] !=0:
                train_X, test_X = train_X_r, test_X_r
        except:
            pass
        
        # fit and predict
        clf = methods[method]()
        clf.fit(train_X, train_y)
        predict = clf.predict(test_X)
        res, details = stats(test_y, predict)
        
        if not os.path.exists(stats_to_here):
            os.makedirs(stats_to_here)
        
        df_results = pd.DataFrame( [
                                   test_ori_name[details.TP],
                                   test_ori_name[details.TN],
                                   test_ori_name[details.FP],
                                   test_ori_name[details.FN],
                                   ]
                                   ).T
        df_results.columns = ('TP','TN','FP','FN')
        df_results.fillna(value = "").to_csv(os.path.join(stats_to_here, 'res.csv'), index=False, encoding='utf8')
        print(ontology,' / ', method )
        print(pd.Series(res))
        return res

    def Experiment_on_Cluster(method : Method, ontology : Ontology, stats_to_here:Path):
        
        # get test datas
        test_X,  test_y , test_ori_name   = get_test_datas_from_ontology(ontology)
        train_X = test_X
        train_y = test_y
                
        test_X, train_X = makeX( test_X, train_X )
        std = StandardScaler(); std.fit(train_X)
        train_X = std.transform(train_X); test_X = std.transform(test_X)
        
        # decomposition
        try:
            print(f'feature_num before decomposition :{test_X.shape[1]}')
            train_X_r, test_X_r = decomposition_method(train_X,train_y)(train_X, test_X)
            print(f'feature_num after decomposition :{test_X.shape[1]}')
            if train_X_r.shape[1] !=0:
                train_X, test_X = train_X_r, test_X_r
        except:
            pass

        
        # fit and predict
        clf = methods[method]()
        clf.fit(train_X, train_y)
        predict = clf.predict(test_X)
        res, details = stats(test_y, predict)
        
        if not os.path.exists(stats_to_here):
            os.makedirs(stats_to_here)
        df_results = pd.DataFrame( [
                                   test_ori_name[details.TP],
                                   test_ori_name[details.TN],
                                   test_ori_name[details.FP],
                                   test_ori_name[details.FN],
                                   ]
                                   ).T
        df_results.columns = ('TP','TN','FP','FN')
        df_results.fillna(value = "").to_csv(os.path.join(stats_to_here, 'res.csv'), index=False, encoding='utf8')
        print(ontology,' / ', method )
        print(pd.Series(res))
        return res

    def foreach(ontology:(Ontology,str) ) :
        stats_to_here : (Path,'curry')\
            = lambda method: stats_to_where.format(root_dir = root_dir, ontology = ontology, method = method)
        res_of_cluster_and_classif \
            = richList(methods)\
             .groupBy(lambda method: method in cluster_kinds )\
             .let(isCluster=True)\
             .connectedWith(
                    (lambda case: case is True,  
                     lambda case: richList(this[isCluster])\
                                    .map(lambda method: (method,
                                        Experiment_on_Cluster(method, ontology, stats_to_here(method  )))).todict()
                    ), # if cluster
                     lambda case: richList(this[not isCluster])\
                                    .map(lambda method: (method,
                                        Experiment_on_Classifier(method,ontology,stats_to_here(method )))).todict()
                    # otherwise
                     ).tolist()
                                        
        res = res_of_cluster_and_classif[0]
        res.update(res_of_cluster_and_classif[1])
        return res
    res_all =  pd.DataFrame(  richList(dfs_of_train.keys()).map(foreach).tolist() )
    last = res_all.shape[0]
    res_all.loc[last] = res_all.mean()

    res_all.to_csv("{root_dir}/stats.all".format(root_dir = root_dir), index=False,encoding='utf8')

    
    




    
    



    



    


