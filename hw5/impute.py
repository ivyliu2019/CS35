import numpy as np
from sklearn import datasets
from sklearn import neighbors

#
# Imputer supporting arbitrary classifiers
#   not optimized: runs one nan at a time...
#
# from https://github.com/scikit-learn/scikit-learn/issues/2989
#
class ImputeLearn(object):
    def __init__(self, mat):
        self.mat = np.array(mat)
        self.mat_isnan = np.isnan(self.mat)
        self.w = np.where(np.isnan(self.mat))

    def impute(self, learner):
        ximp = self.mat.copy()
        for i in np.arange(0, len(self.w[0])):
            n = self.w[0][i] # row where the nan is
            p = self.w[1][i] # column where the nan is
            col_isnan = self.mat_isnan[n, :] # empty columns in row n
            train = np.delete(self.mat, n, axis = 0) # remove row n to obtain a training set
            train_nonan = train[~np.apply_along_axis(np.any, 1, np.isnan(train)), :] # remove rows where there is a nan in the training set
            target = train_nonan[:, p] # vector to be predicted
            feature = train_nonan[:, ~col_isnan] # matrix of predictors
            learn = learner.fit(feature, target) # learner
            ximp[n, p] = learn.predict(self.mat[n, ~col_isnan].reshape(1, -1)) # predict and replace
        
        return(ximp)

if __name__ == "__main__":
    # Impute with learner in the iris data set
    iris = datasets.load_iris()
    mat = iris.data.copy()

    print("mat[0,2] =",mat[0,2])
    print("mat[0,3] =",mat[0,3])
    print("mat[11,1] =",mat[11,1])

    ## throw some nans
    mat[0,2] = np.NaN
    mat[0,3] = np.NaN
    mat[11,1] = np.NaN

    print("mat[0,2] =",mat[0,2])
    print("mat[0,3] =",mat[0,3])
    print("mat[11,1] =",mat[11,1])

    ## impute
    mat = ImputeLearn(mat).impute(learner = neighbors.KNeighborsRegressor(n_neighbors = 5))

    print("mat[0,2] =",mat[0,2])
    print("mat[0,3] =",mat[0,3])
    print("mat[11,1] =",mat[11,1])