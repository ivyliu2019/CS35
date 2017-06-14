#
# read wine data
#
"""
    In this problem, I analyzed Wine recognition data(Updated Sept 21, 1998)
   The analysis determined the quantities of 13 constituents found in each
   of the three types of wines. The 13 attributes are
    1) Alcohol
 	2) Malic acid
 	3) Ash
	4) Alcalinity of ash
 	5) Magnesium
	6) Total phenols
 	7) Flavanoids
 	8) Nonflavanoid phenols
 	9) Proanthocyanins
	10)Color intensity
 	11)Hue
 	12)OD280/OD315 of diluted wines
 	13)Proline
    So I chose to classify the class of each wine as the first feature. I used
    both Decision Tree and RF model to tune the parameters and fit the dataset.
    More information about the parameters and the average best scores for each
    model is provided after each section.

    For the second feature, I chose to impute the value of first 20 wine's
    alchol value. After tuning the parameters, I used RF model to impute and
    more information is provided below.
"""
import numpy as np
from sklearn import cross_validation
from sklearn import tree
from sklearn import ensemble
import pandas as pd

print("+++ Start of pandas' datahandling +++\n")
# df here is a "dataframe":
df = pd.read_csv('wine.data.csv', header=0)    # read the file w/header row #0

df.head()                                 # first five lines
df.info()                                 # column details
# end of conversion to numeric data...
print("\n+++ End of pandas +++\n")

print("+++ Start of numpy/scikit-learn +++\n")
# Save the data with unknown before we drop them
all_data = df.values

# drop the unknown rows now
df = df.dropna()

# Data needs to be in numpy arrays - these next two lines convert to numpy arrays
X_data_full= df.iloc[:,1:].values       # iloc == "integer locations" of rows/cols
y_data_full = df.iloc[:,0].values      # individually addressable columns

# this scrambles the data each time
indices = np.random.permutation(len(X_data_full))
X_data_full = X_data_full[indices]
y_data_full = y_data_full[indices]

# The first twenty are our test set - the rest are our training
X_test = X_data_full[0:20,:]              # the final testing data
X_train = X_data_full[20:,:]              # the training data

# first feature: class
y_test = y_data_full[0:20]                # the final testing outputs/labels (unknown)
y_train = y_data_full[20:]                 # the training outputs/labels (known)

feature_names = ['Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash',
                'Magnesium', 'Total phenols','Flavanoids',
                'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity',
                'Hue', 'OD280/OD315 of diluted wines', 'Proline'  ]
target_names = ['1','2','3']

##########################################################
##                                                      ##
##   Preliminary Work to determine max_depth value      ##
##                                                      ##
##########################################################
# 10-fold cross-validate (use part of the training data for training - and part for testing)
#   first, create cross-validation data (here 9/10 train and 1/10 test)
#   Iterates through the n_neighbors model parameter, also called k, in order
#   to determine which one performs best by 10-fold cross-validate.
def findBestScoreF1():
    """ FindBestScore iterates through the decisionTree model parameter, max_depth,
        between 1 and 20 to determine which one performs best by returning
        the maximum testing_avgScore and the corresponding k value for the first
        feature, safety.
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
#
# Run multiple trials and determine k value
# for i in range(20):
#     print ('the best average scores is when DT max_depth is', findBestScoreF1())

"""
Comments and results:

Briefly mention how this went:
  + what value of max_depth did you decide on for your decition tree?
    By runnint findBestScore() 20 times, I found the highest scores mostly
    happen when max_depth is 15.

  + The average cross-validated test-set accuracy for your best DT model:
    0.97142857142857153

  + A brief summary of what the first two layers of the DT "ask" about a
    line of data:
    First layer: color intensity;
    second layer: Proline and Flavanoids

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

    # write out the dtree to tree.dot (or another filename of your choosing...)
    tree.export_graphviz(dtree, out_file='tree5' + str(max_depth) + '.dot',   # constructed filename!
                            feature_names=feature_names,  filled=True, rotate=False, # LR vs UD
                            class_names=target_names, leaves_parallel=True)

    print ('write out tree5.dot')
    # the website to visualize the resulting graph (the tree) is at www.webgraphviz.com

# print (decisionTreeGraph(15))

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
        rforest = ensemble.RandomForestClassifier(max_depth=max_depth, n_estimators=10)
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

# # Run multiple trials and determine max_depth value
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
        rforest = ensemble.RandomForestClassifier(max_depth=4, n_estimators=n)
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

# # Run multiple trials and determine n value
# for i in range(20):
#      print (findRFBestN())

# RF model feture importances
rforest = ensemble.RandomForestClassifier(max_depth=4, n_estimators=80)
cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
    cross_validation.train_test_split(X_train, y_train, test_size=0.1) # random_state=0
# fit the model using the cross-validation data
rforest = rforest.fit(X_train, y_train)  #already computed
# print("feature importances from RF model are:", rforest.feature_importances_)

"""
what value of max_depth did you decide on for your decition tree?
    By running findRFBestDepth() and findRFBestN() 20 times each,
    I found the highest scores mostly happen when max_depth is 4
    and n_estimator is 80.

The average cross-validated test-set accuracy for your best RF model:
    0.99285714285714288

Feature importances:
[ 0.11870989  0.03622084  0.01187078  0.01112454  0.02495174  0.03957577
  0.11446432  0.00534817  0.02657736  0.16419621  0.11929003  0.15073204
  0.17693832]
"""

##############################################
##                                          ##
##      Second feature: alcohol value       ##
##                                          ##
##############################################
# First we need to tune the parameters:the max_depth and n_estimator
# before we actually impute the alcohol feature

# Divide up the data for second feature: alcohol
# Data needs to be in numpy arrays - these next two lines convert to numpy arrays
X1_data_full= df.iloc[:,2:].values      # iloc == "integer locations" of rows/cols
y1_data_full = df.iloc[:,1].values      # individually addressable columns

# this scrambles the data each time
indices = np.random.permutation(len(X_data_full))
X1_data_full = X1_data_full[indices]
y1_data_full = y1_data_full[indices]

# The first twenty are our test set - the rest are our training
X1_test = X1_data_full[0:20,:]              # the final testing data
X1_train = X1_data_full[20:,:]              # the training data

y1_test = y1_data_full[0:20]                # the final testing outputs/labels (unknown)
y1_train = y1_data_full[20:]                 # the training outputs/labels (known)
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
        rforest = ensemble.RandomForestRegressor(max_depth=max_depth, n_estimators=10)
        trainng_score = []
        testing_score = []
        # run 10 different cross-validation
        for index in range(10):
            # split into cross-validation sets.
            cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
                cross_validation.train_test_split(X1_train, y1_train, test_size=0.1)

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

# # Run multiple trials and determine max_depth value
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
        rforest = ensemble.RandomForestRegressor(max_depth=6, n_estimators=n)
        trainng_score = []
        testing_score = []
        # run 10 different cross-validation
        for index in range(10):
            # split into cross-validation sets.
            cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
                cross_validation.train_test_split(X1_train, y1_train, test_size=0.1)

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

# # Run multiple trials and determine n value
# for i in range(20):
#      print (findRFBestN())

# RF model feture importances
rforest = ensemble.RandomForestRegressor(max_depth=6, n_estimators=20)
cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
    cross_validation.train_test_split(X1_train, y1_train, test_size=0.1) # random_state=0
# fit the model using the cross-validation data
rforest = rforest.fit(X1_train, y1_train)  #already computed
print("feature importances from RF model are:", rforest.feature_importances_)

"""
what value of max_depth did you decide on for your decition tree?
    By running findRFBestDepth() and findRFBestN() 20 times each,
    I found the highest scores mostly happen when max_depth is 6
    and n_estimator is 20.

The average cross-validated test-set accuracy for your best RF model:
    0.58633039461398773

Feature importances:
[ 0.03289736  0.04893755  0.03059275  0.02476788  0.05081728  0.03030378
  0.0354157   0.01351175  0.55476175  0.02817367  0.02586368  0.12395685]
"""


##############################################
##                                          ##
##      Imputing Second feature             ##
##                                          ##
##############################################
from impute import ImputeLearn
from sklearn import neighbors
#
# impute the alcohol feature of first twenty rows with RFs
#
all_data_imp = ImputeLearn( all_data ).impute(learner = ensemble.RandomForestRegressor(n_estimators=20,max_depth=6))
# print("RF imputed outputs are")
# print(all_data_imp[:20,1])

# Extra credit: compute using KN
all_data_imp1 = ImputeLearn( all_data ).impute(learner = neighbors.KNeighborsRegressor(n_neighbors=5))
# print("KN imputed outputs are")
# print(all_data_imp1[:20,1])

"""
RF imputed outputs are:
[ 13.4822506   13.6821056   13.7380744   13.72173724  13.68053709
  13.60023087  13.59772649  13.68146765  13.8365395   13.7763987
  13.15721057  13.46684801  13.58856667  13.78244665  13.6974861
  13.72023545  13.52421786  13.64444116  13.61804051  14.06      ]

KN imputed outputs are
[ 13.924  13.516  13.62   13.272  13.62   13.574  13.596  13.924  13.924
  13.62   13.574  13.574  13.374  13.62   13.574  13.596  13.41   13.62
  13.048  14.06 ]

The original values are:
[ 13.2   13.16  14.37  13.24  14.2   14.39  14.06  14.83  13.86  14.1
  14.12  13.75  14.75  14.38  13.63  14.3   13.83  14.19  13.64  14.06]
"""
