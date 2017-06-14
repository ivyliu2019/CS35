# ## Problem 3:  green-screening!
#
# This question asks you to write one function that takes in two images:
#  + orig_image  (the green-screened image)
#  + new_bg_image (the new background image)
#
# It also takes in a 2-tuple (corner = (0,0)) to indicate where to place the upper-left
#   corner of orig_image relative to new_bg_image
#
# The challenge is to overlay the images -- but only the non-green pixels of
#   orig_image...
#

#
# Again, you'll want to borrow from hw7pr1 for
#  + opening the files
#  + reading the pixels
#  + create some helper functions
#    + defining whether a pixel is green is the key helper function to write!
#  + then, creating an output image (start with a copy of new_bg_image!)
#
# Happy green-screening, everyone! Include at least TWO examples of a background!
#


import cv2
import numpy as np

# Helper Functions
def isGreen( pixel ):
    """ isGreen takes in a pixel and evaluates whether it is a green pixel.
    """
    r, g, b = pixel
    if g>= 220 and r <= 125 and b <= 125:
        return True
    return False

def nonGreen( image, corner ):
    """ nonGreen takes in an input image and the coordinates of corner
        we need to match, returns a dictionary for non-green pixels,
        where the keys are the coordinates and values are the rgb values.
    """
    num_rows, num_cols, num_chans = image.shape
    pixelsDict = {}
    matchingRow, matchingCol = corner

    for row in range(num_rows):
        for col in range(num_cols):
            pixel = image[row, col]
            if isGreen(pixel) == True:
                continue
            # update the col and row
            newRow = matchingRow + row
            newCol = matchingCol + col
            # update the dictionary
            pixelsDict[(newRow, newCol)] = pixel
    return pixelsDict

def writeOutImage(image_name, image_object_to_write):
    """ writeOutImage saves the message-encoded images with
        with _out appended to the end of the filename
    """
    name = 'green_screen' + image_name[:-4] + '_out.png'
    cv2.imwrite( name, image_object_to_write )


# Here is a signature for the green-screening...
# remember - you will want helper functions!
def green_screen( orig_image, new_bg_image, corner=(0,0) ):
    """ green_screen takes in two images orig_image and new_bg_image
        and ignores the "green" from the orig_image and places all of
        the pixels in orig_image that are NOT green on top of new_bg_image.
        The input corner=(0,0) indicates where the upper-left corner of
        orig_image should go within new_bg_image.
    """
    # read the input images
    origImage = cv2.imread(orig_image, cv2.IMREAD_COLOR)
    bgImage = cv2.imread(new_bg_image, cv2.IMREAD_COLOR).copy()

    num_rows, num_cols, num_chans = bgImage.shape
    nonGreenPixels = nonGreen(origImage, corner)
    keysList = nonGreenPixels.keys()

    for row in range(num_rows):
        for col in range(num_cols):
            if (row,col) not in keysList:
                continue
            bgImage[(row, col)] = nonGreenPixels[(row, col)]

    writeOutImage(bgImage, bgImage)

    return bgImage

image1 = green_screen('orig_image.jpg', '2.jpg', corner=(50,50))
image2 = green_screen('orig_image.jpg', '3.jpg', corner=(50,50))
