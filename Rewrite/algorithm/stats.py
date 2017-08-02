from .utils import manager, np, globals_manager, block, richList
from sklearn.metrics import roc_auc_score
c = block()


def stats(y_true: 'np.ndarray', y_pred: 'np.ndarray'):
    TP = (y_true == 1) & (y_pred == 1)
    TN = (y_true == 0) & (y_pred == 0)
    FP = (y_true == 0) & (y_pred == 1)
    FN = (y_true == 1) & (y_pred == 0)
    tp = sum(TP)
    fp = sum(FP)
    fn = sum(FN)
    tn = sum(TN)
    acc = (sum(TP) + sum(TN)) / len(y_true)
    pos_pre = 0 if fp + tp == 0 else tp / (tp + fp)
    pos_rec = 0 if fn + tp == 0 else tp / (tp + fn)
    pos_f1 = 0 if pos_pre == 0 or pos_rec == 0 else 2 / \
        (1 / pos_pre + 1 / pos_rec)

    neg_pre = 0 if fn + tn == 0 else tn / (tn + fn)
    neg_rec = 0 if fp + tn == 0 else tn / (tn + fp)
    neg_f1 = 0 if neg_pre == 0 or neg_rec == 0 else 2 / \
        (1 / neg_pre + 1 / neg_rec)

    pos_auc = roc_auc_score(y_true, y_pred)
    neg_auc = roc_auc_score(~ (y_true.astype(bool)), ~( y_pred.astype(bool)) )

    detail_manager = manager(TP=TP, TN=TN, FN=FN, FP=FP)

    res = manager(pos_pre = pos_pre, neg_pre= neg_pre,
                  pos_rec = pos_rec, neg_rec= neg_rec,
                  pos_f1  = pos_f1,  neg_f1 = neg_f1, 
                  pos_auc = pos_auc, neg_auc= neg_auc,
                  acc=acc)
    return res, detail_manager


def undersampling(X, y, Ori):
    if not isinstance(X,np.ndarray): X = np.array(X)
    if not isinstance(y,np.ndarray): y = np.array(y)
    if not isinstance(Ori,np.ndarray): Ori = np.array(Ori)
    
    res = richList(y).groupBy(lambda x: x == 1)@(lambda this:
                this.map(lambda x: (x, len(this[x])))@(lambda this:dict(this.tolist())))
    to_under, lessCase = (False, True) if res[True] < res[False] else (True, False)
    
    index = np.random.permutation(res[to_under])

    def _getSmaple(var): return (
        var[y == to_under][index[:res[lessCase]]], var[y == lessCase])

    return np.hstack(_getSmaple(X)),\
           np.hstack(_getSmaple(y)),\
           np.hstack(_getSmaple(y))



def getSample(df: 'pandas.DataFrame', n:('sample_num',int), *columns:[("column",str),("column",str),...] ) :
    
    if not columns:
        return ValueError("Nothing Input.")
    
    index = np.random.permutation(df.shape[0])[:n]

    return tuple(df.loc[index,column] for column in columns)
