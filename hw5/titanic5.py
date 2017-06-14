#
# read Titanic data
#
import numpy as np
from sklearn import cross_validation
from sklearn import tree
from sklearn import ensemble
import pandas as pd

print("+++ Start of pandas' datahandling +++\n")
# df here is a "dataframe":
df = pd.read_csv('titanic5.csv', header=0)    # read the file w/header row #0

# drop columns here
df = df.drop(['name', 'ticket', 'fare', 'cabin', 'home.dest','embarked'], axis=1)

# One important one is the conversion from string to numeric datatypes!
# You need to define a function, to help out...
def tr_mf(s):
    """ from string to number
    """
    d = { 'male':0, 'female':1 }
    return d[s]

df['sex'] = df['sex'].map(tr_mf)  # apply the function to the column
df.head()                                 # first five lines
df.info()                                 # column details
#
# end of conversion to numeric data...
print("\n+++ End of pandas +++\n")

print("+++ Start of numpy/scikit-learn +++\n")
# Save the rows with age unknown before we drop them
all_data = df.values

# drop the unknown rows now
df = df.dropna()

# Data needs to be in numpy arrays - these next two lines convert to numpy arrays
X_data_full = df.drop('survived', axis=1).values
y_data_full = df[ 'survived' ].values

# The first twenty are our test set - the rest are our training
X_test = X_data_full[0:20,:]              # the final testing data
X_train = X_data_full[20:,:]              # the training data

y_test = y_data_full[0:20]                # the final testing outputs/labels (unknown)
y_train = y_data_full[20:]                 # the training outputs/labels (known)
feature_names = df.drop('survived', axis=1).columns.values
target_names = ['0','1']

##########################################################
##                                                      ##
##   Preliminary Work to determine max_depth value      ##
##                                                      ##
##########################################################
# 10-fold cross-validate (use part of the training data for training - and part for testing)
#   first, create cross-validation data (here 9/10 train and 1/10 test)
#   Iterates through the n_neighbors model parameter, also called k, in order
#   to determine which one performs best by 10-fold cross-validate.
def findBestScore():
    """ FindBestScore iterates through the n_neighbors model parameter,
        between 1 and 20 to determine which one performs best by returning
        the maximum testing_avgScore and the corresponding k value.
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

# Run multiple trials and determine k value
# for i in range(20):
#     print (findBestScore())

"""
Comments and results:

Briefly mention how this went:
  + what value of max_depth did you decide on for your decition tree?
    By runnint findBestScore() 20 times, I found the highest scores mostly
    happen when max_depth is 3.

  + The average cross-validated test-set accuracy for your best DT model:
    （0.83900000000000008，3)

  + A brief summary of what the first two layers of the DT "ask" about a
    line of data:
    First layer: sex; second layer: pclass and age
"""

######################################
##                                  ##
##   Model Decision Tree Graph      ##
##                                  ##
######################################
def decisionTreeGraph(max_depth):
    """ generate dot file for MDT graph """
    dtree = tree.DecisionTreeClassifier(max_depth=max_depth)

    # this next line is where the full training data is used for the model
    dtree = dtree.fit(X_data_full, y_data_full)
    print("\nCreated and trained a decision tree classifier")

    #
    # write out the dtree to tree.dot (or another filename of your choosing...)
    tree.export_graphviz(dtree, out_file='tree' + str(max_depth) + '.dot',   # constructed filename!
                            feature_names=feature_names,  filled=True, rotate=False, # LR vs UD
                            class_names=target_names, leaves_parallel=True)
    print ('write out tree.dot')
    # the website to visualize the resulting graph (the tree) is at www.webgraphviz.com

# print (decisionTreeGraph(3))

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
# for i in range(20):
#     print (findRFBestDepth())

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
        rforest = ensemble.RandomForestClassifier(max_depth=5, n_estimators=n)
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

# Run multiple trials and determine n value
# for i in range(20):
#      print (findRFBestN())

# RF model feture importances
rforest = ensemble.RandomForestClassifier(max_depth=5, n_estimators=110)
cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
    cross_validation.train_test_split(X_train, y_train, test_size=0.1) # random_state=0
# fit the model using the cross-validation data
rforest = rforest.fit(X_train, y_train)
# print("feature importances from RF model are:", rforest.feature_importances_)

"""
what value of max_depth did you decide on for your decition tree?
    By running findRFBestDepth() 20 times, I found the highest scores mostly
    happen when max_depth is 5 and n_estimator is 110.

The average cross-validated test-set accuracy for your best RF model:
    0.83600000000000008

Feature importances:
    [ 0.20447085  0.532224    0.14179381  0.0545039   0.06700745]

"""

#####################################
##                                 ##
##   Impute the missing ages       ##
##                                 ##
#####################################
# Imputing
from impute import ImputeLearn
from sklearn import neighbors
#
# impute with RFs
#
all_data_imp = ImputeLearn( all_data ).impute(learner = ensemble.RandomForestRegressor(n_estimators = 110,max_depth=5))
# print("RF imputed outputs are")
# print(all_data_imp[:30,3])

"""
RF imputed outputs are
[ 28.61872875  28.63456658  28.65385468  28.7512153   28.51688421
  28.61481153  26.55535028  28.67823843  28.67123124  28.60948563
  33.99177592  34.14306998  30.3744952   33.17889396  30.29148392
  29.89082837  30.08769026  34.28713337  29.22173117  14.03788659
  36.51798391  17.54575112  44.39754546  43.0770746   42.30811932
  38.29996219  38.00541655  43.07320461  51.04449032  43.05613767]
 Compared to the google sheet, we could see that the imputed outputs are not
 accurate at all.
"""

# Extra credit: compute using KN 
all_data_imp1 = ImputeLearn( all_data ).impute(learner = neighbors.KNeighborsRegressor(n_neighbors=5))
print("KN imputed outputs are")
print(all_data_imp1[:30,3])
"""

KN imputed outputs are
[ 25.2      25.2      25.2      25.2      25.2      25.2      24.2      25.2
  25.2      25.2      34.3      34.3      31.6      30.8      31.6      31.6
  31.6      34.3      28.       3.36666   32.4      41.       36.8      43.6
  36.8      46.2      53.       36.1      51.4      36.1    ]
Compared to RF algorithm, KN is slightly more accurate.
"""
