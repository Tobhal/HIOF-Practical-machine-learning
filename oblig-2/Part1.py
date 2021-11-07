import numpy as np
from numpy.lib.function_base import iterable
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits

import random

def runMLPC(randomState = 1, maxIter = 50, nLayers = (8,), printProb = False, printNumber = 1):
    """
    Runs the MPLClassifier function and returns the score.
    Can also print the probability
    """
    digits = load_digits()

    X = digits.data
    y = digits.target

    # X = Data
    # Y = Classification
    # X, y = load_digits(return_X_y=True)

    trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.30)

    clf = MLPClassifier(random_state=randomState, max_iter=maxIter, hidden_layer_sizes=nLayers).fit(trainX, trainY)

    if printProb:
        predict = clf.predict_proba(X[:8])

        for n in range(0,10):
            print(f'{n}: {round(predict[0][n], 3)}')

        plt.matshow(digits.images[0])
        plt.show()

    return clf.score(testX, testY)

def run(iterations = 5, randomState = 1, maxIter = 300, nLayers = (100,), printScore = False):
    """
    Runs multiple of runMLPC() then takes the mean for the resoult.
    Can then print to consol
    """
    scores = []
    
    for i in range(iterations):
        score = runMLPC(randomState=randomState,
                    maxIter=maxIter,
                    nLayers=nLayers,)

        scores.append(score)

    if printScore:
        for i in range(len(scores)):
            print(f'Run {i+1}| Score: {round(score * 100, 2)}%')

    return scores

def plotThing1(iter, iterations, layers, iterationIncreas=0, layersIncrease=0, plot = False):
    """
    Plots the score over diffrent iterations of values for the model.
    Can iterate over:
        - Numer of iteration the model should take
        - Numer of noed in the first layer

    """
    scores = []

    for i in range(iter):
        it = iterations + (iterationIncreas * i)
        layer = layers + (layersIncrease * i)

        if it < 1:
            it = 1

        if layer < 1:
            layer = 1

        score = run(maxIter=it, nLayers=(8,8,8,8))
        score = np.mean(score)
        scores.append(score)

    # print(scores)
    if plot:
        plt.plot(range(iter), scores)
        plt.xlabel(f'Num of iteration')
        plt.ylabel(f'Score (median of 5 runs)')
        plt.show()

    return scores

def plotThing2(iter, iterations, layers, plot = False):
    """
    This is a more limited version of the plotThis1() for when there is no need for iteration increases.
    """
    scores = []

    for _ in range(iter):
        score = runMLPC(maxIter=iterations, nLayers=layers)
        score = np.mean(score)
        scores.append(score)

    # print(scores)
    if plot:
        plt.plot(range(iter), scores)
        plt.show()

    return scores

def plotMulti():
    i = 15

    plt.plot(plotThing1(i,  0, 0, iterationIncreas=0, layersIncrease=0), label="1")
    plt.plot(plotThing1(i, 10, 0, iterationIncreas=0, layersIncrease=0), label="2")
    plt.plot(plotThing1(i, 20, 0, iterationIncreas=0, layersIncrease=0), label="3")
    plt.plot(plotThing1(i, 30, 0, iterationIncreas=0, layersIncrease=0), label="4")
    plt.plot(plotThing1(i, 40, 0, iterationIncreas=0, layersIncrease=0), label="5")
    plt.plot(plotThing1(i, 50, 0, iterationIncreas=0, layersIncrease=0), label="6")

    plt.legend()
    plt.xlabel('Num itterations')
    plt.ylabel('Score')
    plt.show()

def plotMulti2():
    """
    Prints a bar diagram of the score with difrent logic for the hidden layers.
    This uses the run() so there is only 1 output form the run.
    """
    it = 300

    startLayers = 0
    startNumLayers = 1
    layersSize = 1

    for i in range(15):
        i+1

        labelString = f'{startNumLayers + (layersSize*i)}'

        plt.bar(i, run(iterations=2,
                       randomState=1,
                       maxIter=it,
                       # Select one to use

                       ## Increments the amout of nodes in the layer and increas the amount of layers
                       # nLayers=tuple(startNumLayers + (LayerSize*l) for l in range(startLayers+i))),

                       ## Incements the amount of layers but keep tha same number of nodes
                       # nLayers=tuple(startNumLayers + (layersSize) for l in range(startLayers+i))),

                       ## Incremenst the amount of nodes in the first layer
                       nLayers=((startNumLayers + (layersSize*i)),)),
                label=str(labelString))

    plt.legend(title='Num layers')
    plt.xlabel("Num nodes")
    plt.ylabel("Score")
    plt.show()

def plotMulti3():
    """
    Print a bar diagram of how the score is over difrent number of hidden layers.
    This uses the plotThing2() to get a mean of multiple runs of the same model creation.
    """
    it = 3

    iterations = 100

    startLayers = 1
    startNumLayers = 8
    layersSize = 0

    start = 1
    end = 15

    for i in range(start, end):
        labelString = f'{startNumLayers + (layersSize*i)}'

        plt.bar(i, plotThing2(it, # Number of model iterations
                             iterations, # Number of iterations used in the model
                             # Adds more layers to the hidden layer, all with the same amount of nodes
                             tuple(startNumLayers + (layersSize) for l in range(startLayers+i))),
                label=str(labelString))

    #plt.legend(title='Num layers')
    plt.title(f'Score for {iterations} iterations of {start} to {end}')
    plt.xlabel(f'Num hidden layers of {startNumLayers} nodes')
    plt.ylabel(f'Score (mean of {it} runs per layer)')
    plt.show()

if __name__ == '__main__':
    # Run iterations of the MMPLClassifier
    # Start with itterations of the model
    # Start with nodes in the hiddel layer
    # Incrase the itteration
    # Incrase the hidden layesr
    
    plotThing1(30, 0, 0, iterationIncreas=10, plot=True)
    # plotThing1(50, 0, 100, iterationIncreas=1, layersIncrease=0, plot=True)

    # plotMulti()
    # plotMulti2()
    # plotMulti3()

    # run(iterations=5, nLayers=(8,8,8,8), maxIter=150, printScore=True)

    # print(runMLPC(printProb=True))
    

    