# Code cuistomized from  various online resources
# mainly from https://github.com/chasinginfinity/ml-from-scratch/tree/master/02%20Linear%20Regression%20using%20Gradient%20Descent

import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (12.0, 9.0)


#Preprocessing / taking Input from the DataFile 
##  You can use your own method to load the data from a file

data=pd.read_csv('toydata.csv')

X=data.iloc[:,0]
Y=data.iloc[:,1]

plt.scatter(X,Y)

plt.show()
 

# Initialize our regression coefficients 

# in this case m and C

m=0
c=0
n= float(len(X)) ####  just to get the number of rows/elements in X

##Set the Learning Rate
L=0.0001

epochs=2000 # The number of iterations to perform the gradient descent

### We can have different stopping criteria , this is the most trivial one

for i in range(epochs):
    Y_Pred =m*X +c
    D_m=(-2/n) *sum(X * (Y - Y_Pred))  ## Derivative wrt m
    D_c=(-2/n) *sum(Y - Y_Pred)  ## Derivative with respect to c
    m= m - L * D_m
    c= c - L*D_c
print (m,c)


# Making Prediction
Y_Pred=m*X +c

### Visualize the reg. line

plt.scatter(X, Y)
plt.plot([min(X), max(X)], [min(Y_Pred), max(Y_Pred)], color ='green') 
plt.savefig('predicted.png')
plt.show()

##calculating error term / min. value here means better learning model
##Plotting the residuals , important task, look into slides to know why it is important

residual=Y -Y_Pred
residual_mean = statistics.mean(residual) 

Square_Residual_Sum=(residual*residual).sum() ###  adding up the square of the error terms

print (Square_Residual_Sum)

plt.scatter(X, residual)  ###  Y axis is where we plot our residuals
plt.plot([min(X), max(X)], [residual_mean, residual_mean], color='red')
plt.savefig('residual.png')
plt.show()



