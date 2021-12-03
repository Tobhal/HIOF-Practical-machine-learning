import sys
from typing import OrderedDict, Tuple, Type

from collections import Counter, OrderedDict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pretty_errors
from mpl_toolkits.mplot3d import Axes3D
from pandas.core.tools.datetimes import Scalar
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler, normalize

trainingData = pd.read_csv("ALS_TrainingData_2223.csv").drop('ID', axis=1)
testingData = pd.read_csv("ALS_TestingData_78.csv").drop('ID', axis=1) 

def printData():
    global trainingData, testingData
    print('Training data:')
    print(trainingData.info())

    print('Testing data:')
    print(testingData.info())

def normalizePCAData(data, components):
    # Scale and normalize the data
    scaler = StandardScaler()
    dataScaled = scaler.fit_transform(data)
    dataNormalized = normalize(dataScaled)

    # Generate the coloums to extract from the reduction
    columns = [f'C{i+1}' for i in range(components)]
    
    # Reduce the dimentions of the data
    pca = PCA(n_components=components)
    dataPricipal = pd.DataFrame(pca.fit_transform(dataNormalized))
    dataPricipal.columns = columns

    return dataPricipal


def calculateKMeans(nCluster, maxIter=300, plotType=None, pcaComponents=2):
    global trainingData

    dataPricipal = normalizePCAData(trainingData, 2)

    kmeans = KMeans(n_clusters=nCluster, random_state=0, max_iter=maxIter)
    predict = kmeans.fit_predict(dataPricipal)

    if plotType == 'scatter':
        plt.figure(figsize = (6,6))
        plt.title(f'Scatter {nCluster} clusters') 
        plt.scatter(dataPricipal['C1'], dataPricipal['C2'], c=predict, cmap='rainbow', s=10)

    if plotType == 'denrogram' or plotType == 'dend':
        plt.figure(figsize = (6,6))
        plt.title('Dendogram')
        dendrogram((linkage(dataPricipal, method ='ward')))

    count = Counter(kmeans.labels_)
    count = OrderedDict(sorted(count.items()))

    highest = 0
    lowest = 10000

    for key, val in count.items():
        print(f'Key: {key:2} has {val:4} number of items')
        highest = val if highest < val else highest
        lowest = val if lowest > val else lowest

    print(f'Higest num of values:{highest:5} | Lowest num of values:{lowest:5} | The diff: {highest - lowest}')

    return kmeans, dataPricipal, predict

def scoreModel(plotType=None, scoreRange=None, showProgress=True, scoreType='slihouette'):
    global testingData

    scores = []

    if scoreRange == None:
        scoreRange = (2,5)

    # Calculate the scores for kmeans
    for i in range(scoreRange[0], scoreRange[1]):
        model, pricipal, predict = calculateKMeans(i)

        if scoreType == 'slihouette' or scoreType == 'slih':
            scores.append(silhouette_score(pricipal, predict))

        if scoreType == 'wss':
            scores.append(model.inertia_)

        # Show a progress present of how mutch is left
        if showProgress:
            progress = (i-scoreRange[0])/((scoreRange[1]-1)-scoreRange[0]) * 100
            sys.stdout.write(f'\rProgress: {round(progress,1)}%')
            sys.stdout.flush()
        
    print()

    if scoreType == 'slihouette' or scoreType == 'slih':
        plt.title(f'Slihouette, min={scoreRange[0]}, max ={scoreRange[1]-1}')
    if scoreType == 'wss':
        plt.title(f'WSS, min={scoreRange[0]}, max ={scoreRange[1]-1}')

    # Print the bar diagram if spesefied in the console
    if plotType == 'bar':
        plt.bar(range(scoreRange[0], scoreRange[1]), scores)
        plt.xlabel('Number of clusters')
        plt.ylabel('S(i)')

    if plotType == 'line':
        plt.plot(range(scoreRange[0], scoreRange[1]), scores)
        plt.xlabel('Number of clusters')
        plt.ylabel('S(i)')

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

    try:
        scoreType = sys.argv[4]
    except:
        scoreType = 'slihouette'
    else:
        scoreType = scoreType.lower()

    kmeans = calculateKMeans(numOfClusters, plotType=plotType)
    
    if not scoreRange == None:
        scoreModel(plotType=plotType, scoreRange=scoreRange, scoreType=scoreType)
    
    plt.show()


    

"""
Chouse K:
    - k = sqrt(number of data points)
    - dendogram

"""
    






    