Python-NLP
======

这里面所有的代码都是给人打工写的...
工作就是验证各种算法的词向量的效果，

-验证数据集：

  DBPedia 数据库

-验证方法：

  包括但不限于验证不同Ontology的Entities的可分性。

  算法包括：

    rbf-svm

    linear-svm

    randomforest

    naive-bayes

    kmeans

    ...

    (总之算法本身只是调用sklearn,参数默认，没什么意思...)

    (聚类算法模拟分类时，将聚类得到的多个子类做正负划分，寻找到MCC指标最高的划分，把这个结果视为聚类算法的预测)
