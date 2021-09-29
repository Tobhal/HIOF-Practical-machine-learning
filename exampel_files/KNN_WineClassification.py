###https://www.datacamp.com/community/tutorials/k-nearest-neighbor-classification-scikit-learn


#Import scikit-learn dataset library

from sklearn import datasets

#Load dataset
wine = datasets.load_wine()
###  you can load your own dataset from a textfile stored in your disk using regular python functions


# print the names of the features
print(wine.feature_names)

# print the label species(class_0, class_1, class_2)
print(wine.target_names)


# print data(feature)shape
print(wine.data.shape)


# print target(or label)shape
print(wine.target.shape)



# Import train_test_split function
from sklearn.model_selection import train_test_split

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.3) # 70% training and 30% test

#Import knearest neighbors Classifier model
from sklearn.neighbors import KNeighborsClassifier

#Create KNN Classifier
knn = KNeighborsClassifier(n_neighbors=5) ##specify the value of K here

#Train the model using the training sets
knn.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = knn.predict(X_test)



#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


