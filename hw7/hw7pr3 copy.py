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
from matplotlib import pyplot as plt


#################################
#       Helper Function         #
#################################

def read_image( image_name ):
    """ This function takes in an image name, and output and
        image (numpy array) read by cv2
    """
    raw_image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    return raw_image


def is_green(pixel):
    """ This function takes in a pixel: a list of rgb values in the format:
        [r, g, b]

        This function returns True, if it is a green pixels, which we should
        ignore when transfer the pixel to background. The function returns
        False if it is not a green pixel.
    """
    # Get the r,g,b value
    r, g, b = pixel

    # Check whether pixel is green by setting thresholded for all three
    # values
    if g >= 100 and r <= 140 and b <= 140:
        return True

    return False

def get_not_green_pixels( image, corner):
    """ This function takes in an read image, and a corner that we want to
        match the current image to background image.

        This function returns a dictionary of all non-green pixels of the
        input image. The keys are the coordinates of the pixel, the values are
        the list of rgb value [r,g,b] of that pixel.

        Note the keys are coordinates already transformed to the coordinates
        corresponded to the background image using corner.
    """
    # get the shape and tranlation value, also set up the empty dictionary
    num_rows, num_cols, num_chans = image.shape
    all_green_pixels = {}
    add_row, add_col = corner

    # loop though all pixels
    for row in range(num_rows):
        for col in range(num_cols):

            # get pixel
            pixel = image[row,col]

            # if it is green pixel, ignore
            if is_green(pixel):
                continue

            # if not, get the transformed coordinates
            new_row = row + add_row
            new_col = col + add_col

            # add the (key,value) pair to dictionary
            co_or = (new_row, new_col)
            all_green_pixels[co_or] = pixel

    return all_green_pixels


#################################
#         Main Function         #
#################################

# Here is a signature for the green-screening...
# remember - you will want helper functions!
def green_screen( orig_image, new_bg_image, corner=(0,0) ):
    """ This function takes in two image names and a corner coordinates:
            orig_image: The image name of green_background images with
                        figures in the front
            new_bg_image: The image name of the new background image that
                          we want to transfer the figure to
            corner: The coordinates of new_bg_image that we want the
                    orig_image to overlap its corner to

        This function writes out the image with figure from orig_image
        transform to the new_bg_image.

        This function also retuns this green_screened image as a numpy array
    """
    # Read both image
    green_image = read_image(orig_image)
    bg_image = read_image(new_bg_image).copy()

    # get the shape, get all pixels not green from orig_image, get their
    # coordinates
    num_rows, num_cols, num_chans = bg_image.shape
    all_not_green_pixels = get_not_green_pixels(green_image, corner)
    all_keys = all_not_green_pixels.keys()

    # loop though all pixles of bg_image
    for row in range(num_rows):
        for col in range(num_cols):

            # if not a pixel we want to transfer, ignore
            if (row, col) not in all_keys:
                continue

            # else set the pixel from orig_image to bg_image
            bg_image[row,col] = all_not_green_pixels[(row, col)]

    # write out the file
    outputname = 'green_screen_' + new_bg_image[:-4] + '.png'
    cv2.imwrite(outputname, bg_image)

    # convert the color
    bg_image = cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB)


    # return the image
    return bg_image


# image1 = green_screen('orig_image.jpg', '2.jpg', corner=(-200,-50))
# image2 = green_screen('orig_image.jpg', '3.jpg', corner=(200,-100))

image = green_screen('orig_image.jpg', '4.jpg', corner=(700,1000))

"""
Comment and Analysis:

We implemented the green_screen function using three helper function, one to
read the image, one to define what "green" is and one to get all non-green
pixels from an input image, and align the coordinates with the corner given.
Then using these three funtions, we can read two images, get the pixels we
want to trasfer from orig_image and tranform the pixle rgb value in
new_bg_image with aligned coordinates.

we included twoe examples:
green_screen_harrypotter.png
green_screen_new_pic2.png

We can see that there are still green dots around the figure transfered, so
there are still things we can improve: ways of defining green.

All images and code include on GitHub:
https://github.com/maggieli96/CS35_Midway_Projects/tree/master/pixel

"""
