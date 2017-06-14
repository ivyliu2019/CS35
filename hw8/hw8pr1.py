#
# coding: utf-8
#
# hw8pr1.py - the k-means algorithm -- with pixels...
#

# import everything we need...
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import utils
import cv2
from math import pow, sqrt

# choose an image...
IMAGE_NAME = "./jp.png"  # Jurassic Park
IMAGE_NAME = "./batman.png"
IMAGE_NAME = "./hmc.png"
IMAGE_NAME = "./thematrix.png"
IMAGE_NAME = "./fox.jpg"
IMAGE_NAME = "./1.jpg"
IMAGE_NAME = "./2.jpg"
image = cv2.imread(IMAGE_NAME, cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# reshape the image to be a list of pixels
image_pixels = image.reshape((image.shape[0] * image.shape[1], 3))

# choose k (the number of means) in  NUM_MEANS
# and cluster the pixel intensities
barList = []
for i in range(2,6):
    NUM_MEANS = i
    clusters = KMeans(n_clusters = NUM_MEANS)
    clusters.fit(image_pixels)

    # After the call to fit, the key information is contained
    # in  clusters.cluster_centers_ :
    count = 0
    print ("When K = ", NUM_MEANS)
    for center in clusters.cluster_centers_:
        print("Center #", count, " == ", center)
        # note that the center's values are floats, not ints!
        center_integers = [int(p) for p in center]
        print("   and as ints:", center_integers)
        count += 1

    # build a histogram of clusters and then create a figure
    # representing the number of pixels labeled to each color
    hist = utils.centroid_histogram(clusters)
    bar = utils.plot_colors(hist, clusters.cluster_centers_)
    barList += [bar]


# in the first figure window, show our image
plt.figure()
plt.axis("off")
plt.imshow(image)

# in the second figure window, show the pixel histograms
#   this starter code has a single value of k for each
#   your task is to vary k and show the resulting histograms
# this also illustrates one way to display multiple images
# in a 2d layout (fig == figure, ax == axes)
#
fig, ax = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False)
titleList = []
for i in range(2,6):
    titleList += [str(i)+" means"]
ax[0,0].imshow(barList[0]);    ax[0,0].set_title(titleList[0])
ax[0,1].imshow(barList[1]);    ax[0,1].set_title(titleList[1])
ax[1,0].imshow(barList[2]);    ax[1,0].set_title(titleList[2])
ax[1,1].imshow(barList[3]);    ax[1,1].set_title(titleList[3])
for row in range(2):
    for col in range(2):
        ax[row,col].axis('off')
# plt.show(fig)


# Helper function
def getDistance( pixel1, pixel2 ):
    """ getDistance takes in two inputs: pixel1, pixel2, and
        calculates the "Pythagorean-style" distance and returns
        the distance
    """
    r1, g1, b1 = pixel1
    r2, g2, b2 = pixel2
    sum = pow(r1-r2, 2) + pow(g1-g2, 2) + pow(b1-b2, 2)
    distance = sqrt(sum)
    return distance

def clusterPixels( image_pixels, NUM_MEANS ):
    """ clustersPixels takes in an input image_pixels and
        NUM_MEANS and returns a list of key information cotained
        in clusters.cluster_centers_.
    """
    clusters = KMeans(n_clusters = NUM_MEANS)
    clusters.fit(image_pixels)

    # After the call to fit, the key information is contained
    # in  clusters.cluster_centers_ :
    count = 0
    centerList = []
    for center in clusters.cluster_centers_:
        # note that the center's values are floats, not ints!
        center_integers = [int(p) for p in center]
        centerList.append(center_integers)
    return centerList

def getClosestK( centerVal, pixel ):
    """ getClosestK takes in a list of centers' values and input pixel,
        finds the mean (from k-means) that input pixel is closest to
        and returns the cloest center value.
    """
    distanceDict = {}
    minDistance = 99999999
    minDistanceIndex = 0
    for i in range(len(centerVal)):
        distanceDict[i] = getDistance( centerVal[i], pixel )
        if minDistance > distanceDict[i]:
            minDistance = distanceDict[i]
            minDistanceIndex = i
    closestK = centerVal[minDistanceIndex]
    return closestK

NUM_MEANS = 5
def posterizing(imageName):
    """ posterizing takes in an input image and creates a new image
        from the original one. The new images is simplified in the
        color content.
    """
    new_image = image.copy()
    new_image = cv2.imread(imageName,cv2.IMREAD_COLOR)
    # new_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    new_image_pixels = image.reshape((image.shape[0] * image.shape[1], 3))
    centerList = clusterPixels( new_image_pixels, NUM_MEANS )

    pixelsList = []
    num_rows, num_cols, num_chans = new_image.shape
    for row in range(num_rows):
        for col in range(num_cols):
            pixel = new_image[row, col]
            new_image[row, col] = getClosestK( centerList, pixel)
    return new_image

#
# comments and reflections on hw8pr1, k-means and pixels
"""
 + Which of the paths did you take:
    + posterizing or
    + algorithm-implementation
    I chose posterizing path.

 + How did it go?  Which file(s) should we look at?
    For image '1.jpg', I used k = 2 and the generated image is called '1_posterized'
    For image '2.jpg', I used k = 5 and the generated image is called '2_posterized'

 + Which function(s) should we try.
    posterizing(imageName) will generate the posterized image pixels.
"""
#
#
