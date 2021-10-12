import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits

def run(randomState = 1, maxIter = 300, nLayers = (100,), plot = False):
    # digits = load_digits()

    # X = Data
    # Y = Classification
    X, y = load_digits(return_X_y=True)

    trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.30)

    clf = MLPClassifier(random_state=randomState, max_iter=maxIter, hidden_layer_sizes=nLayers).fit(trainX, trainY)

    # predict = clf.predict_proba(testX[:8])
    # plt.matshow(predict)
    # plt.show()

    return clf.score(testX, testY)

if __name__ == '__main__':
    for i in range(5):
        score = run(randomState=1,
                    maxIter=10,
                    nLayers=(50,))

        print(f'Run {i+1}| Score: {round(score * 100, 2)}%')
















#   o==+--
#   |  |\ \
#   |  | \ \    ____________________
#   |   \ \ \   |                  |
#   |    \ \ \  |  +------------+  |
#   |     \ \ \ |  |     (__)   |  |
#   |      \ \ \|  |     (oo)   |  |
#   |       \ \ |  | o\  .\/.   |  |
#   |        \ \|  | | \/    \  |  |
# /---\       \ |  +------------+  |
#/     \       \|                  |
#|     |        |                  |
#\     /        |                  |
# \---/         |                  |
#               |                  |
#            --------------------------
#           (                          )
#            --------------------------
#          Cow-struction worker.


# ______________________   _______________________
# |                    |   |                     |
# |            (__)    |   |  (__)               |
# |            (oo)    |   |  (oo)               |
# |     /-------\/     |   |---\/           /----|
# |    / |     ||      |   |  ||           / |   |
# |   *  ||----||      |   |--||          *  ||--|
# |      ^^    ^^      |   |  ^^             ^^  |
# |--------------------|   |---------------------|
#       Normal Cow         0   Cow  modulo one   1