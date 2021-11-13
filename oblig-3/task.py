from typing import Tuple, Type
import pretty_errors
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.tools.datetimes import Scalar

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score

trainingData = pd.read_csv("/Users/tobiashallingstad/Prog/HIOF/HIOF-Practical-machine-learning/oblig-3/ALS_TrainingData_2223.csv").drop('ID', axis=1)
testingData = pd.read_csv("/Users/tobiashallingstad/Prog/HIOF/HIOF-Practical-machine-learning/oblig-3/ALS_TestingData_78.csv").drop('ID', axis=1)    

def normalizePCAData(data, components):
    # Scale and normalize the data
    scaler = StandardScaler()
    dataScaled = scaler.fit_transform(data)
    dataNormalized = normalize(dataScaled)

    # Reduce the dimentions of the data
    pca = PCA(n_components=components)
    dataPricipal = pd.DataFrame(pca.fit_transform(dataNormalized))
    dataPricipal.columns = ['C1', 'C2']

    return dataPricipal


def calculateKMeans(nCluster, maxIter=300, plotType=None, pcaComponents=2):
    global trainingData

    dataPricipal = normalizePCAData(trainingData, 2)

    kmeans = KMeans(n_clusters=nCluster, random_state=0, max_iter=maxIter)
    predict = kmeans.fit_predict(dataPricipal)

    if plotType == 'scatter':
        plt.figure(figsize = (6,6))
        plt.title('Visulize the data') 
        plt.scatter(dataPricipal['C1'], dataPricipal['C2'], c=predict, cmap='rainbow', s=10)
        plt.show()

    if plotType == 'denrogram' or plotType == 'dend':
        plt.figure(figsize = (6,6))
        plt.title('Visulize the data')
        dendrogram((linkage(dataPricipal, method ='ward')))
        plt.show()

    return kmeans, dataPricipal, predict

def scoreModel(plotType=None, scoreRange=None, showProgress=True):
    scores = []

    if scoreRange == None:
        scoreRange = (2,5)

    # Calculate the scores for kmeans
    for i in range(scoreRange[0], scoreRange[1]):
        model, pricipal, predict = calculateKMeans(i)
        scores.append(silhouette_score(pricipal, predict))

        # Show a progress present of how mutch is left
        if showProgress:
            progress = (i-scoreRange[0])/((scoreRange[1]-1)-scoreRange[0]) * 100
            sys.stdout.write(f'\rProgress: {round(progress,1)}%')
            sys.stdout.flush()
    
    # Print the bar diagram if spesefied in the console
    if plotType == 'bar':
        plt.bar(range(scoreRange[0], scoreRange[1]), scores)
        plt.xlabel('Number of clusters')
        plt.ylabel('S(i)')
        plt.show()

if __name__ == '__main__':
    try:
        plotType = sys.argv[1]
    except:
        plotType = None
    else:
        plotType = plotType.lower()

    try:
        numOfClusters = int(sys.argv[2])
    except:
        numOfClusters = 5

    try:
        scoreRange = (int(sys.argv[2]), int(sys.argv[3])+1)
    except:
        scoreRange = None

    kmeans = calculateKMeans(numOfClusters, plotType=plotType)
    
    #scoreModel(plotType=plotType, scoreRange=scoreRange)

    

"""
Chouse K:
    - k = sqrt(number of data points)
    - dendogram

"""
    






    