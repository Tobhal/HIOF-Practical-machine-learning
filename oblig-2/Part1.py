import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits

digits = load_digits()

# X = Data
# Y = Classification
X, y = load_digits(return_X_y=True)

trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.30)

randomState = 1
maxIter = 300
nLayers = (200,100)
clf = MLPClassifier(random_state=randomState, max_iter=maxIter, hidden_layer_sizes=nLayers).fit(trainX, trainY)

print(clf.score(testX, testY))

# predict = clf.predict_proba(testX[:8])
# plt.matshow(predict)
# plt.show()




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