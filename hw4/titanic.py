#
#
# titanic.py
#
#

import numpy as np
from sklearn import datasets
from sklearn import cross_validation
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# For Pandas's read_csv, use header=0 when you know row 0 is a header row
# df here is a "dataframe":
df = pd.read_csv('titanic.csv', header=0)
df.head()
df.info()

# let's drop columns with too few values or that won't be meaningful
df = df.drop(['name', 'ticket', 'cabin', 'home.dest',
                    'boat', 'embarked', 'body'], axis=1)

# let's drop all of the rows with missing data:
df = df.dropna()

# let's see our dataframe again...
# I ended up with 1045 rows (anything over 500-600 seems reasonable)
df.head()
df.info()

# conversion to numeric datatypes for all input columns
def tr_mf(s):
    """ from string to number
    """
    d = { 'male':0, 'female':1 }
    return d[s]

df['sex'] = df['sex'].map(tr_mf)  # apply the function to the column

# let's see our dataframe again...
df.head()
df.info()

# you will need others!

print("+++ end of pandas +++\n")

# import sys
# sys.exit(0)

print("+++ start of numpy/scikit-learn +++")

# We'll stick with numpy - here's the conversion to a numpy array

# extract the underlying data with the values attribute:
X_data_full = df.drop('survived', axis=1).values
y_data_full = df[ 'survived' ].values      # also addressable by column name(s)


##################################################
##                                              ##
##   Preliminary Work to determine k value      ##
##                                              ##
##################################################
# drop the initial (unknown) rows to test with known data
X_data = X_data_full[42:,:]   # 2d array
y_data= y_data_full[42:]     # 1d column

# scramble the data
indices = np.random.permutation(len(X_data))  # this scrambles the data each time
X_data = X_data[indices]
y_data = y_data[indices]

# feature engineering.
X_data[:,0] *= 5
X_data[:,1] *= 25
X_data[:,2] *= 10
X_data[:,3] *= 10
X_data[:,4] *= 10

# The first twenty are our test set - the rest are our training
X_test = X_data_full[0:20,:]              # the final testing data
X_train = X_data_full[20:,:]              # the training data

y_test = y_data_full[0:20]                # the final testing outputs/labels (unknown)
y_train = y_data_full[20:]                 # the training outputs/labels (known)


# 10-fold cross-validate (use part of the training data for training - and part for testing)
#   first, create cross-validation data (here 3/4 train and 1/4 test)
#   Iterates through the n_neighbors model parameter, also called k, in order
#   to determine which one performs best by 10-fold cross-validate.
def findBestScore():
    """ FindBestScore iterates through the n_neighbors model parameter, k
        between 1 and 20 to determine which one performs best by returning
        the maximum testing_avgScore and the corresponding k value.
    """
    resultList = []
    BestScore = 0
    kList = [ k for k in range(1,21) if k%2 != 0]
    for k in kList:
        knn = KNeighborsClassifier(n_neighbors=k)
        trainng_score = []
        testing_score = []
        for index in range(10):
            cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
                cross_validation.train_test_split(X_train, y_train,
                                test_size=0.1) # random_state=0

            # fit the model using the cross-validation data
            #   typically cross-validation is used to get a sense of how well it works
            #   and tune any parameters, such as the k in kNN (3? 5? 7? 41?, etc.)
            knn.fit(cv_data_train, cv_target_train)
            trainng_score += [knn.score(cv_data_train,cv_target_train)]
            testing_score += [knn.score(cv_data_test,cv_target_test)]

        # Compute the average score for both traning and testing data
        trainng_avgScore = 1.0 * sum(trainng_score)/len(trainng_score)
        testing_avgScore = 1.0 * sum(testing_score)/len(testing_score)
        if testing_avgScore > BestScore:
            BestScore = testing_avgScore
            bestK = k
        resultList += [[k, trainng_avgScore, testing_avgScore]]
    return BestScore, bestK

# Run multiple trials and determine k value
# for i in range(40):
#     print (findBestScore())

##############################
##                          ##
##       Prediction         ##
##                          ##
##############################

# feature engineering.
X_data_full[:,0] *= 2
X_data_full[:,1] *= 20
X_data_full[:,2] *= 10
X_data_full[:,3] *= 5
X_data_full[:,4] *= 5

# Divide up the dataset
X_test = X_data_full[0:42,:]              # the final testing data
X_train = X_data_full[42:,:]              # the training data
y_train = y_data_full[42:]                  # the training outputs/labels

#
# Train, predecit and then see two sets of unknown-label data.
#
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=11)   # 7 is the "k" in kNN based on testing
# this next line is where the full training data is used for the model
knn.fit(X_train, y_train)
print("\nCreated and trained a knn classifier")  #, knn

# printed out:
print("X_test1's predicted outputs for full-data are")
print(knn.predict(X_test))

print("+++ end of numpy/scikit-learn +++")
"""
Comments and results:
Briefly mention how this went:
  + what value of k did you decide on for your kNN?
    I decide to use 7 as the k value for kNN.
  + how high were you able to get the average cross-validation (testing) score?
    The highest average cross-validation score I got is 0.79702970297029696
   + how smoothly did this kNN workflow go
    Overall the prediction of this kNN workflow goes smoothly. It takes about
    1.20s to predict all 42 values.

The predicted survival of the 42 people:
Past those labels (just labels) here:
You'll have 42 lines:
[0 0 0 0 0 0 1 1 1 1 0 1 0 0 0 0 0 0 1 1 0 1 0 1 1 1 1 0 0 1 1 1 1 1 0 0 0
 1 0 1 0 1]
"""
