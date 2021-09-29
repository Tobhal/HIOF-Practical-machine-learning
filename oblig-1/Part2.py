import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

data = pd.read_csv('/Users/tobiashallingstad/prog_ting/HIOF-Practical-machine-learning/oblig-1/iris.data')

# Splt data and classefier
x = data.iloc[:,0:4]
y = data.iloc[:,4]

# Split data into test and training data
testSetPrecentage = 0.25
trainX, testX, trainY, testY = train_test_split(x, y, test_size=testSetPrecentage)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(trainX, trainY)

predY = knn.predict(testX)

# Messure the accracy of the model
print('Accracy:', metrics.accuracy_score(testY, predY))
