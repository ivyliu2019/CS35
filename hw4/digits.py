#
#
# digits.py
#
#

import numpy as np
from sklearn import cross_validation
import pandas as pd
#
# For Pandas's read_csv, use header=0 when you know row 0 is a header row
# df here is a "dataframe":
#
df = pd.read_csv('digits.csv', header=0)
df.head()
df.info()

#
# Convert feature columns as needed...
# You may to define a function, to help out:
#
def transform(s):
    """ from number to string
    """
    return 'digit ' + str(s)

df['label'] = df['64'].map(transform)  # apply the function to the column
print("+++ End of pandas +++\n")

# import sys
# sys.exit(0)

#
# implement the kNN model
#
print("+++ Start of numpy/scikit-learn +++")

# We'll stick with numpy - here's the conversion to a numpy array
X_data = df.iloc[:,0:64].values        # iloc == "integer locations" of rows/cols
y_data = df[ 'label' ].values      # also addressable by column name(s)

#
# feature engineering by re-scaleing column values
#
for index in range(8):
    col1 = index*8
    col2 = index*8 + 1
    col3 = index*8 + 2
    col4 = index*8 + 3
    col5 = index*8 + 4
    col6 = index*8 + 5
    col7 = index*8 + 6
    col8 = index*8 + 7
X_data[:, col1] *= 1   # worth 1x more!
X_data[:, col2] *= 2   # worth 2x more!
X_data[:, col3] *= 4   # worth 1x more!
X_data[:, col4] *= 5   # worth 2x more!
X_data[:, col5] *= 4   # worth 1x more!
X_data[:, col6] *= 3   # worth 2x more!
X_data[:, col7] *= 2   # worth 1x more!
X_data[:, col8] *= 1   # worth 2x more!

#
# Divide up dataset for two tests and trainings
#
X_test1 = X_data[10:22, :]            # the final testing data for full-data
X_train1 = X_data[22:, :]             # the training data data for full-data

X_test2 = X_data[:10, :40]            # the final testing data for partial-data
X_train2 = X_data[22:, :40]           # the training data for partial-data

y_train1 = y_data[22:]                # the training outputs full-data (unknown)
y_train2 = y_data[22:]                # the training outputs partial-data(unknown)


#
# Train, predecit and then see two sets of unknown-label data.
#
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)   # 1 is the "k" in kNN based on testing
# this next line is where the full training data is used for the model
knn.fit(X_train1, y_train1)
print("\nCreated and trained a knn classifier")  #, knn

# here are some examples, printed out:
print("X_test1's predicted outputs for full-data are")
print(knn.predict(X_test1))

# this next line is where the full training data is used for the model
knn.fit(X_train2, y_train2)
print("\nCreated and trained a knn classifier")  #, knn
# printed out
print("X_test2's predicted outputs for partial-data are")
print(knn.predict(X_test2))

#
# feature display - use %matplotlib to make this work smoothly
#
from matplotlib import pyplot as plt

def show_digit( Pixels ):
    """ input Pixels should be an np.array of 64 integers (from 0 to 15)
        there's no return value, but this should show an image of that
        digit in an 8x8 pixel square
    """
    print(Pixels.shape)
    Patch = Pixels.reshape((8,8))
    plt.figure(1, figsize=(4,4))
    plt.imshow(Patch, cmap=plt.cm.gray_r, interpolation='nearest')  # cm.gray_r   # cm.hot
    plt.show()

# try it!
row = 3
Pixels = X_data[row:row+1,:]
show_digit(Pixels)
print("That image has the label:", y_data[row])

##########################
##                      ##
##   Preliminary Work   ##
##                      ##
##########################

#
# Run cross-validation to turn parameters (Before actually predict)
#

# test with known data and scramble the remaining data
X_data = X_data[22:,:]   # 2d array
y_data = y_data[22:]     # 1d column

indices = np.random.permutation(len(X_data))  # this scrambles the data each time
X_data = X_data[indices]
y_data = y_data[indices]

#
# Divide up dataset to test
#
X_test = X_data[:,:]              # the final testing data
X_train = X_data[:,:]             # the training data

y_test = y_data[:]                 # the final testing outputs/labels (unknown)
y_train = y_data[:]                # the training outputs/labels (known)


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
# for i in range(20):
#     print (findBestScore())

"""
Comments and results:

Briefly mention how this went:
  + what value of k did you decide on for your kNN?
    By runnint findBestScore() 20 times, I found the highest scores mostly
    happen when k = 1 or 3. So I used both values to predict.

  + how smoothly were you able to adapt from the iris dataset to here?
    Very smooth. The only change I made was the way to divide up the dataset.
    Besides, by observing the dataset by each column, I reweighted columns.

  + how high were you able to get the average cross-validation (testing) score?
    (0.98952164009111632, 3)

Then, include the predicted labels of the 12 digits with full data but no label:
Paste those labels (just labels) here:
You'll have 12 lines:

X_test1's predicted outputs for full-data are
['digit 9' 'digit 9' 'digit 5' 'digit 5' 'digit 6' 'digit 5' 'digit 0'
 'digit 3' 'digit 8' 'digit 9' 'digit 8' 'digit 4']

Paste those labels (just labels) here:
You'll have 10 lines:
X_test2's predicted outputs for partial-data are
['digit 0' 'digit 0' 'digit 0' 'digit 1' 'digit 7' 'digit 2' 'digit 3'
 'digit 4' 'digit 0' 'digit 1']
"""
