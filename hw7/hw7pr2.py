# ## Problem 2:  steganography
#
# This question asks you to write two functions, likely with some helper functions, that will enable you
# to embed arbitrary text (string) messages into an image (if there is enough room!)

# For extra credit, the challenge is to be
# able to extract/embed an image into another image...

#
# You'll want to borrow from hw7pr1 for
#  + opening the file
#  + reading the pixels
#  + create some helper functions!
#  + also, check out the slides :-)
#
# Happy steganographizing, everyone!
#

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Part A: here is a signature for the decoding
# remember - you will want helper functions!
def desteg_string( image ):
    """
        desteg_string takes in a steganographized image,
        goes through each pixel, one-by-one and extracts the lowest-order
        bit from its channels.
    """
    bitString = readImage(image)
    message = convertToMessage(bitString)
    return (message)

# HelperFunction1
def readImage( image ):
    """
        readImage takes in the image and returns the corresponding
        binary string
    """
    num_rows, num_cols, num_chans = image.shape
    string = ""
    for row in range(num_rows):
        for col in range(num_cols):
            # obtain the rgb value from each pixel
            for i in range(3):
                val = image[row, col][i]
                bit = bin(val)
                string += bit[-1]
    return string

# HelperFunction2
def convertToMessage(string):
    """
    convertToMessage obtains the output message from the binary string
    """
    index = int(string.find('00000000')/8)
    message = ""
    for i in range(index):
        block = string[i*8: (i+1)*8]
        value = int(block, 2)
        message += chr(value)
    return (message)

# test with the first image (no need to convert)
im_rgb2 = cv2.imread('small_flag_with_message_rgb.png',cv2.IMREAD_COLOR)
desteg_string( im_rgb2 )
message = desteg_string( im_rgb2 )
print("message is ", message)

# test with the second image
im_bgr = cv2.imread('small_flag_with_message_bgr.png',cv2.IMREAD_COLOR)
im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
message = desteg_string( im_rgb )
print("message is ", message)


# Part B: here is a signature for the encoding/embedding
# remember - you will want helper functions!
def steganographize( image_name, message ):
    """ steganographize takes in an image and a message (a string) and
        return a copy of the image, but with the least-significant bits
        of some/all of its pixels changed to hold the message, one bit
        at a time!
    """
    image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    newImage = image.copy()
    num_rows, num_cols, num_chans = image.shape

    bitsString = convertToBitString( message )
    index = 0
    for row in range(num_rows):
        for col in range(num_cols):
            # obtain the rgb value from each pixel
            for i in range(3):
                if index == len(bitsString):
                    break

                rgbVal = image[row, col][i]
                bit = bitsString[index]
                rgbVal = modifyPixels( rgbVal, bit )

                newImage[row, col][i] = rgbVal
                index += 1

    writeOutImage(image_name, newImage)
    return

# Helper Functions
def convertToBitString( message ):
    """ convertToBitString takes in a string message and converts it
        to a standardized binary string and end with '00000000'.
    """
    bitsString = ''
    for char in message:
        num = ord(char)
        binary = bin(num)[2:]
        string = (8 - len(binary))*'0' + binary
        bitsString += string
    bitsString += '00000000'
    return bitsString

def writeOutImage(image_name, image_object_to_write):
    """ writeOutImage saves the message-encoded images with
        with _out appended to the end of the filename
    """
    name = image_name[:-4] + '_out.png'
    cv2.imwrite( name, image_object_to_write )

def modifyPixels( rgbVal, bit ):
    """ modifyPixels takes in a rgb value and modify the
        last digit for rgb value if it's different from
        the imput bit
    """
    binary = bin(rgbVal)[2:]
    rgbBit = bin(rgbVal)[-1]

    if rgbBit == bit:
        return rgbVal
    else:
        newBit = binary[:-1]+bit
        value = int(newBit,2)
        return value
