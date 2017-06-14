#
# read digits data
#


import numpy as np
from sklearn import cross_validation
from sklearn import tree
from sklearn import ensemble
import pandas as pd

print("+++ Start of pandas' datahandling +++\n")
# df here is a "dataframe":
df = pd.read_csv('digits5.csv', header=0)    # read the file w/header row #0
df.head()                                 # first five lines
df.info()                                 # column details


print("\n+++ End of pandas +++\n")

print("+++ Start of numpy/scikit-learn +++\n")

# Data needs to be in numpy arrays - these next two lines convert to numpy arrays
X_data_orig = df.iloc[:,0:64].values        # iloc == "integer locations" of rows/cols
y_data_orig = df[ '64' ].values      # individually addressable columns (by name)
feature_names = df.columns.values
target_names = ['0','1','2','3','4','5','6','7','8','9']

X_data_full = X_data_orig[0:,:]  #
y_data_full = y_data_orig[0:]    #
#
# now, grab and edit pieces from iris5.py in order to try DTs and RFs on the digits dataset!
#

#
# cross-validation and scoring to determine parameters...
# The first ten will be our test set - the rest will be our training set
#
X_test = X_data_full[0:20,0:64]              # the final testing data
X_train = X_data_full[20:,0:64]              # the training data

y_test = y_data_full[0:20]                  # the final testing outputs/labels (unknown)
y_train = y_data_full[20:]                  # the training outputs/labels (known)


#
# we can scramble the data - but only if we know the test set's labels!
#
indices = np.random.permutation(len(X_data_full))  # this scrambles the data each time
X_data_full = X_data_full[indices]
y_data_full = y_data_full[indices]


######################################
##                                  ##
##   Model Decision Tree Graph      ##
##                                  ##
######################################
def decisionTreeGraph(max_depth):
    ''' generate dot file for MDT graph'''
    dtree = tree.DecisionTreeClassifier(max_depth=max_depth)

    # this next line is where the full training data is used for the model
    dtree = dtree.fit(X_data_full, y_data_full)
    dtree.feature_importances_
    print("\nCreated and trained a decision tree classifier")

    #
    # write out the dtree to tree.dot (or another filename of your choosing...)
    tree.export_graphviz(dtree, out_file='tree' + str(max_depth) + '.dot',   # constructed filename!
                            feature_names=feature_names,  filled=True, rotate=False, # LR vs UD
                            class_names=target_names, leaves_parallel=True)
    print ('write out tree.dot')
    # the website to visualize the resulting graph (the tree) is at www.webgraphviz.com

print (decisionTreeGraph(4))

#################################
##                             ##
##    Find max_depth for DT    ##
##                             ##
#################################
#  10-fold cross-validate (use part of the training data for training - and part for testing)
#   first, create cross-validation data (here 9/10 train and 1/10 test)
#   Iterates through the decision tree model parameter, max_depth, in order
#   to determine which one performs best by 10-fold cross-validate.
def findBestScore():
    """ findBestScore iterates through the model parameters, max_depth,
        between 1 and 20 to determine which one performs best by returning
        the maximum testing_avgScore and the corresponding max_depth value.
    """
    resultList = []
    BestScore = 0
    # iterate through different max_depths from 1 to 19
    for max_depth in range(1,20):
        dtree = tree.DecisionTreeClassifier(max_depth=max_depth)
        trainng_score = []
        testing_score = []
        # run 10 different cross-validation
        for index in range(10):
            # split into cross-validation sets.
            cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
                cross_validation.train_test_split(X_train, y_train, test_size=0.1)

            # fit the model using the cross-validation data
            # and tune parameter, such as max_depth here
            dtree = dtree.fit(cv_data_train, cv_target_train)
            dtree.feature_importances_
            trainng_score += [dtree.score(cv_data_train,cv_target_train)]
            testing_score += [dtree.score(cv_data_test,cv_target_test)]

        # Compute the average score for both traning and testing data
        trainng_avgScore = 1.0 * sum(trainng_score)/len(trainng_score)
        testing_avgScore = 1.0 * sum(testing_score)/len(testing_score)

        # find the best score
        if testing_avgScore > BestScore:
            BestScore = testing_avgScore
            best_depth = max_depth
        resultList += [[best_depth, trainng_avgScore, testing_avgScore]]
    print ('The best average score and the corresponding max_depth is: ')
    return BestScore, best_depth

# # Run multiple trials and determine max_depth value
# for i in range(20):
#     print (findBestScore())


"""
Comments and results:

Briefly mention how this went:
  + what value of max_depth did you decide on for your decition tree?
    By runnint findBestScore() 20 times, I found the highest scores mostly
    happen when max_depth is 16.

  + how smoothly were you able to adapt from the iris dataset to here?
    Very smooth. The only change I made was the way to divide up the dataset.

  + how high were you able to get the average cross-validation (testing) score?
    (0.87752808988764053, 16)
"""


##########################################################
##                                                      ##
##    Find max_depth and n_estimators for RF model      ##
##                                                      ##
##########################################################
#
# The data is already in good shape -- a couple of things to define again...
#
def findRFBestDepth():
    """ findRFBestDepth iterates through the model parameter, max_depth
        between 1 and 20 to determine which one performs best by returning
        the maximum testing_avgScore and the corresponding max_depth value
        when n_estimators is 100.
    """
    resultList = []
    BestScore = 0
    # iterate through different max_depths from 1 to 19
    for max_depth in range(1,20):
        rforest = ensemble.RandomForestClassifier(max_depth=max_depth, n_estimators=100)
        trainng_score = []
        testing_score = []
        # run 10 different cross-validation
        for index in range(10):
            # split into cross-validation sets.
            cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
                cross_validation.train_test_split(X_train, y_train, test_size=0.1)

            # fit the model using the cross-validation data
            # and tune parameter, such as max_depth here
            rforest = rforest.fit(cv_data_train, cv_target_train)
            trainng_score += [rforest.score(cv_data_train,cv_target_train)]
            testing_score += [rforest.score(cv_data_test,cv_target_test)]

        # Compute the average score for both traning and testing data
        trainng_avgScore = 1.0 * sum(trainng_score)/len(trainng_score)
        testing_avgScore = 1.0 * sum(testing_score)/len(testing_score)

        # find the best score
        if testing_avgScore > BestScore:
            BestScore = testing_avgScore
            best_depth = max_depth
        resultList += [[best_depth, trainng_avgScore, testing_avgScore]]
    print ('The best average score and the corresponding max_depth is: ')
    return BestScore, best_depth

# Run multiple trials and determine max_depth value
for i in range(20):
    print (findRFBestDepth())


def findRFBestN():
    """ findRFBestN iterates through the model parameter, n_estimators
        between 1 and 200 that is the mutiple of 10 to determine which one
        performs best by returning the maximum testing_avgScore and the
        corresponding max_depth value when max_depth is 16.
    """
    resultList = []
    BestScore = 0
    nList = [ n for n in range(1,200) if n%10 == 0]
    for n in nList:
        rforest = ensemble.RandomForestClassifier(max_depth=16, n_estimators=n)
        trainng_score = []
        testing_score = []
        # run 10 different cross-validation
        for index in range(10):
            # split into cross-validation sets.
            cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
                cross_validation.train_test_split(X_train, y_train, test_size=0.1)

            # fit the model using the cross-validation data
            # and tune parameter, such as max_depth here
            rforest = rforest.fit(cv_data_train, cv_target_train)
            trainng_score += [rforest.score(cv_data_train,cv_target_train)]
            testing_score += [rforest.score(cv_data_test,cv_target_test)]

        # Compute the average score for both traning and testing data
        trainng_avgScore = 1.0 * sum(trainng_score)/len(trainng_score)
        testing_avgScore = 1.0 * sum(testing_score)/len(testing_score)

        # find the best score
        if testing_avgScore > BestScore:
            BestScore = testing_avgScore
            best_n = n
        resultList += [[n, trainng_avgScore, testing_avgScore]]
    print ('The best average score and the corresponding n_estimator is: ')
    return BestScore, best_n

#
# # Run multiple trials and determine n value
# for i in range(20):
#      print (findRFBestN())

"""
Comments and results:

Briefly mention how this went:
  + what value of max_depth did you decide on for your decition tree?
    By runnint findRFBestDepth() 20 times, I found the highest scores mostly
    happen when max_depth is 16.

  + what value of n_estimator did you decide on for your decition tree?
    By runnint findRFBestN() 20 times, I found the highest scores mostly
    happen when n_estimator is 140.

  + how smoothly were you able to adapt from the iris dataset to here?
    Very smooth except that it takes much longer time to run with n_estimator.

  + how high were you able to get the average cross-validation (testing) score?
    (0.98651685393258437, 16, 100)
"""

#################################
##                             ##
##    Feature Importances      ##
##                             ##
#################################
# DT model
dtree = tree.DecisionTreeClassifier(max_depth=16)
cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
        cross_validation.train_test_split(X_train, y_train, test_size=0.1) # random_state=0
# fit the model using the cross-validation data
dtree = dtree.fit(cv_data_train, cv_target_train)
print ('feature importances from DT model are:', dtree.feature_importances_)

# RF model
rforest = ensemble.RandomForestClassifier(max_depth=16, n_estimators=140)
cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
    cross_validation.train_test_split(X_train, y_train, test_size=0.1) # random_state=0
# fit the model using the cross-validation data
rforest = rforest.fit(X_train, y_train)
print("feature importances from RF model are:", rforest.feature_importances_)

'''
feature importances from DT model are:
[ 0.          0.          0.0132354   0.0069676   0.01064929  0.04944418
  0.00257861  0.          0.          0.00413532  0.01739187  0.00208349
  0.0050296   0.00968679  0.00243074  0.          0.          0.00333359
  0.01152157  0.01603394  0.03670882  0.09435273  0.00300949  0.
  0.00137797  0.00598697  0.06863125  0.07019612  0.04684652  0.00309408
  0.01245666  0.          0.          0.06201758  0.00835238  0.00641358
  0.08116455  0.01664386  0.00439885  0.          0.          0.01327392
  0.07551539  0.05490232  0.00104175  0.01048294  0.01076259  0.
  0.          0.          0.00408859  0.00511558  0.0021465   0.0042228
  0.028481    0.002722    0.          0.          0.00645974  0.00226355
  0.06824407    0.02690215  0.0006945   0.00650722]
feature importances from RF model are:
[  0.00000000e+00   2.11088947e-03   2.19266679e-02   1.06135651e-02
   9.36413481e-03   2.10295749e-02   8.31125450e-03   5.34774982e-04
   3.28298082e-05   9.16584396e-03   2.47422402e-02   7.36968185e-03
   1.55329903e-02   2.69762129e-02   6.07073127e-03   6.16382337e-04
   4.63213032e-05   7.79225358e-03   1.99779638e-02   2.40288556e-02
   3.11046750e-02   4.74165367e-02   9.21440904e-03   3.41342932e-04
   9.86573637e-05   1.48083262e-02   4.09770907e-02   2.55668676e-02
   2.82280710e-02   2.37354753e-02   3.27108908e-02   9.73558206e-05
   0.00000000e+00   3.21873276e-02   2.61843669e-02   1.90451365e-02
   4.33946945e-02   1.81024099e-02   2.37338905e-02   0.00000000e+00
   8.41434575e-06   1.02430828e-02   3.65384734e-02   4.75528375e-02
   2.02158359e-02   1.84681929e-02   2.01941223e-02   1.32482886e-04
   4.92859080e-05   1.97466729e-03   1.80886903e-02   2.14050978e-02
   1.21533397e-02   2.10023299e-02   2.58638991e-02   1.83083128e-03
   8.24673852e-06   1.73034834e-03   2.17922903e-02   1.03937055e-02
   2.50507061e-02   3.02952200e-02   1.79290848e-02   3.88812187e-03]
[Finished in 7.607s]
The best average score and the corresponding n_estimator is:
(0.98426966292134832, 180)

'''
