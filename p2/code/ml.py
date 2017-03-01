# scikit-learn imports
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn import svm
from sklearn import linear_model
from sklearn import hmm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier

# everything else
import sys
from inspect import isclass

def run(train_samples, train_labels, test_samples, test_labels):
    module = sys.modules[__name__]

    classes = get_subclasses(get_superclass(module), module)
    
    ret = []

    for c in classes:
        # instantiate object
        alg = c(train_samples, train_labels, test_samples, test_labels)

        alg.train()
        alg.test()

        ret.append(alg)
    return ret
        
def get_superclass(module):
    return getattr(module, "Alg")

def get_subclasses(super_class, module):
    return [obj for obj in [getattr(module, name) for name in dir(module)] \
            if isclass(obj) and issubclass(obj, super_class) and obj is not super_class]


def threshold(L, val):
    return [1 if el > val else 0 for el in L]

def true_positive(L1, L2):
    return sum([1 for i,l in enumerate(L1) if l and L2[i] == 1])

class Alg():
    def __init__(self, train_samples, train_labels, test_samples, test_labels):
        self.train_samples = train_samples
        self.train_labels = train_labels
        self.test_samples = test_samples
        self.test_labels = test_labels
    
    # assumes that train and test have been run
    # self.results should now be populated with 0/1's
    def P(self):
        assert all([el == 0 or el == 1 for el in self.results]), \
            "Invalid results list!\n%s" % self.results
        
        if sum(self.results) == 0:
            return 1
        else:
            return float(true_positive(self.results, self.test_labels))/sum(self.results)

    def R(self):
        if sum(self.test_labels) == 0:
            return 1
        else:
            return float(true_positive(self.results, self.test_labels))/sum(self.test_labels)

    def __str__(self):
        return "%s:\t%f\t%f" % (self.__class__.__name__, self.P(), self.R())
    
class DecisionTree(Alg):
    def train(self):
        self.clf = tree.DecisionTreeClassifier()
        self.clf = self.clf.fit(self.train_samples, self.train_labels)
        
    def test(self):
        self.results = self.clf.predict(self.test_samples)

class LinearRegression(Alg):
    def train(self):
        self.regr = linear_model.LinearRegression()
        self.regr.fit(self.train_samples, self.train_labels)

    def test(self):
        self.results = threshold(self.regr.predict(self.test_samples), 0.5)

class LogisticRegression(Alg):
    def train(self):
        self.regr = linear_model.LogisticRegression()
        self.regr.fit(self.train_samples, self.train_labels)

    def test(self):
        self.results = self.regr.predict(self.test_samples)


class SupportVectorMachine(Alg):
    def train(self):
        self.clf = svm.SVC()
        self.clf.fit(self.train_samples, self.train_labels)

    def test(self):
        self.results = self.clf.predict(self.test_samples)

class RandomForest(Alg):
    def train(self):
        self.clf = RandomForestClassifier(n_estimators=10)
        self.clf = self.clf.fit(self.train_samples, self.train_labels)
        
    def test(self):
        self.results = self.clf.predict(self.test_samples)
        
class kNN(Alg):
    def train(self):
        self.neigh = KNeighborsClassifier(n_neighbors=3)
        self.neigh.fit(self.train_samples, self.train_labels)
        
    def test(self):
        self.results = self.neigh.predict(self.test_samples)

class GaussianNaiveBayes(Alg):
    def train(self):
        self.clf = GaussianNB()
        self.clf.fit(self.train_samples, self.train_labels)
        
    def test(self):
        self.results = self.clf.predict(self.test_samples)

class AdaBoost(Alg):
    def train(self):
        self.clf = AdaBoostClassifier()
        self.clf.fit(self.train_samples, self.train_labels)
        
    def test(self):
        self.results = self.clf.predict(self.test_samples)
