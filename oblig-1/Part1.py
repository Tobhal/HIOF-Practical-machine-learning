import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import linear_model
from sklearn.model_selection import train_test_split

data = pd.read_csv('/Users/tobiashallingstad/prog_ting/HIOF-Practical-machine-learning/oblig-1/truckdata.csv')

x = data.iloc[:,0]
y = data.iloc[:,1]

# Split data to test data and training data
testSetPrecentage = 0.2
trainX, testX, trainY, testY = train_test_split(x, y, test_size=testSetPrecentage)

# Convert to np array
trainX = trainX.values
trainY = trainY.values
testX = testX.values
testY = testY.values

# Plot training data
plt.scatter(trainX, trainY, color="red")
plt.scatter(testX, testY, color="blue")

# Import the linear regression object
reg = linear_model.LinearRegression()

# fit the data into the linear regression
reg.fit(trainX.reshape(-1,1), trainY)

# Fit line for train data
idx = np.argsort(trainX)
y_pred = reg.predict(trainX[idx].reshape(-1,1))
plt.plot(trainX[idx], y_pred, color='red', linewidth=3)

# Plot test line
idx = np.argsort(testX)
y_pred = reg.predict(testX[idx].reshape(-1,1))
plt.plot(testX[idx], y_pred, color='blue', linewidth=3)

plt.show()