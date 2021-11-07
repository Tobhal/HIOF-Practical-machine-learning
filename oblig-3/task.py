import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

trainingData = pd.read_csv("/Users/tobiashallingstad/Prog/HIOF/HIOF-Practical-machine-learning/oblig-3/ALS_TrainingData_2223.csv")
testingData = pd.read_csv("/Users/tobiashallingstad/Prog/HIOF/HIOF-Practical-machine-learning/oblig-3/ALS_TestingData_78.csv")

print(trainingData)