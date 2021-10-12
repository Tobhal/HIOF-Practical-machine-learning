import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits

def runMLPC(randomState = 1, maxIter = 300, nLayers = (100,), plot = False):
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

def run(iterations, randomState = 1, maxIter = 300, nLayers = (100,), print = False):
    scores = []
    
    for i in range(5):
        score = runMLPC(randomState=randomState,
                    maxIter=maxIter,
                    nLayers=nLayers,)

        scores.append(score)

    if print:
        for i in range(len(scores)):
            print(f'Run {i+1}| Score: {round(score * 100, 2)}%')

    return scores

def plotThing(iter, iterations, layers, iterationIncreas=0, layersIncrease=0, plot = False):
    scores = []

    for i in range(iter):
        it = iterations + (iterationIncreas * i)
        layer = layers + (layersIncrease * i)

        if it < 1:
            it = 1

        if layer < 1:
            layer = 1

        score = runMLPC(maxIter=it, nLayers=(layer,))
        score = np.mean(score)
        scores.append(score)

    # print(scores)
    if plot:
        plt.plot(range(iter), scores)
        plt.show()

    return scores

def plotMulti():
    i = 50

    plt.plot(plotThing(i,  0, 0, iterationIncreas=0, layersIncrease=10), label="1")
    plt.plot(plotThing(i, 10, 0, iterationIncreas=0, layersIncrease=10), label="2")
    plt.plot(plotThing(i, 20, 0, iterationIncreas=0, layersIncrease=10), label="3")
    plt.plot(plotThing(i, 30, 0, iterationIncreas=0, layersIncrease=10), label="4")
    plt.plot(plotThing(i, 40, 0, iterationIncreas=0, layersIncrease=10), label="5")
    plt.plot(plotThing(i, 50, 0, iterationIncreas=0, layersIncrease=10), label="6")

    plt.legend()
    plt.show()

if __name__ == '__main__':
    # Run iterations of the MMPLClassifier
    # Start with itterations of the model
    # Start with nodes in the hiddel layer
    # Incrase the itteration
    # Incrase the hidden layesr
    
    #plotThing(50, 50, 0, iterationIncreas=0, layersIncrease=10, plot=True)
    #plotThing(50, 0, 100, iterationIncreas=1, layersIncrease=0, plot=True)

    plotMulti()
    






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