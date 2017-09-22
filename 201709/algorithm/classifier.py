from .utils import np

class cluster:
    def __init__(self, clf):
        self.clf = clf

    def fit(self, X, y):
        self.clf.fit(X, y)
        y_label = self.clf.predict(X)
        labels = sorted(set(y_label))
        def getPre(x): 
            return sum((y_label == x) & (y == 1))**2 /\
                   ((1 + sum(y_label == x)) *  (1 + sum(y == 1)) )
        pres = [getPre(label_i) for label_i in labels]
        maxpreind = np.argmax(pres)
        pos_label = labels[maxpreind]
        pos_label = labels[np.argmax([getPre(label_i) for label_i in labels])]
        self.pos_label = pos_label
        return self

    def predict(self, X):
        y_pred = self.clf.predict(X)
        y_pred = (y_pred == self.pos_label).astype(int)
        return y_pred


def wrap(method, **params):
    def _func():
        strict_params = dict()
        for param_name in params:
            if param_name.startswith("lazy_"):
                strict_params[param_name[5:]] = params[param_name]()
            else:
                strict_params[param_name] = params[param_name]
        return method(**strict_params)
    return _func


