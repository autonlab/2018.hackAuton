import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.tree import export_graphviz
import csv
import numpy as np
from sklearn import metrics
from sklearn.model_selection import KFold, StratifiedKFold

kf = KFold(n_splits=10, shuffle=True)

X = []
Y = []
with open('synthetic_encoded.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(len(row)):
            row[i] = float(row[i])
        X.append(row[:-1])
        Y.append(row[-1])

X = np.array(X)
Y = np.array(Y)



def getErrors(y_pred, y_true):
    fp, fn=0,0
    for i in range(len(y_pred)):
        if y_pred[i]==1 and y_true[i]==0:
            fp += 1
        elif y_pred[i]==0 and y_true[i]==1:
            fn += 1
    return (fp, fn)


class RF():
    def __init__(self, max_depth):
        self.clf = RandomForestClassifier(max_depth=max_depth)
        self.scores = []


    def train(self):
        N = len(Y)
        FP=0
        FN=0
        averages = [0]*28
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = Y[train_index], Y[test_index]

            self.clf.fit(X_train, y_train)
            score = self.clf.score(X_test, y_test)
            y_pred = self.clf.predict(X_test)
            fp, fn = getErrors(y_pred, y_test)
            print(N, fp, fn)
            FP+=fp
            FN+=fn
            importance = self.clf.feature_importances_
            for i in range(len(importance)):
                averages[i] += importance[i]
            print(importance)
            print(score)
            self.scores.append(score)

        for i in range(len(averages)):
            averages[i] = averages[i]/10
        print(averages)
        print(np.mean(self.scores))
        print("FP:", FP/N)
        print("FN:", FN/N)



def main(args): 
    model = RF(20)
    model.train()

# 0,2,5: percent below poverty, 


if __name__ == '__main__':
    main(sys.argv)