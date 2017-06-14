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

"""
Comments/Analysis:

(1) The spam_out.png contains a hidden message that I wrote. You could find it
    by using the decode function above

(2) CHANLLENGE: The harrypotter_out.png contains a huge amount of text, see
    if you can find out what it is!

All images and codes are included in GitHub:
https://github.com/maggieli96/CS35_Midway_Projects/tree/master/pixel
"""

import cv2
import numpy as np

#################################
#           Part A              #
#################################


# Part A: here is a signature for the decoding
# remember - you will want helper functions!

def read_all_bit( image ):
    """ This function takes in an input image (already read using cv2)

        This function loop though all pixels, transform the rgb value following
        r->g->b order to binary bits, and read the lowest-order bits add to the
        output string.

        This function retuns a string of bits that contains the last bit of
        all rgb value in binary form.
    """
    # get the numrow and num col
    num_rows, num_cols, num_chans = image.shape
    out_string = ""

    # loop though all pixel
    for row in range(num_rows):
        for col in range(num_cols):
            # loop through the pixel rgb value of the original picture
            for i in range(3):
                # get the value -> to binary string -> get last bit
                val = image[row,col][i]
                bit = bin(val)
                out_string += bit[-1]

    return out_string



def output_message(bit_string):
    """ This function takes in a list of bits.

        This function loop through the block of 8 bits. Check if it is end
        mark "00000000", if yes then stopping reading. If not, then get the
        integer value of the binary string, and then get the ascii char with
        this specific value. Add to the output string

        This function returns the message contains in the bit string
    """
    # Get the largest num possible of blocks, initiate output string
    num = int(len(bit_string) / 8)
    message = ""

    # loop though all blocks
    for i in range(num):

        # get the block of 8 digits binary string
        beg = 8*i
        end = 8*(i+1)
        block = bit_string[beg:end]

        # if end mark, break
        if block == "00000000":
            break

        # if not, convert to ascii char and add to message string
        val = int(block, 2)
        char = chr(val)
        message += char

    return message



def desteg_string( image ):
    """ This function takes in an image already read by cv2, then it returns
        the coded message in this image.
    """
    # read the bit_string
    out_string = read_all_bit(image)

    # get the message
    message = output_message(out_string)
    return message





#################################
#           Part B              #
#################################

def read_image( image_name ):
    """ This function takes in an image name, and output and
        image (numpy array) read by cv2
    """
    raw_image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    return raw_image


def char_to_block(char):
    """ This function takes in a character.

        This function gets the ascii value of the char, get the corresponding
        binary string and standardized it to 8 digits

        This function return the 8 digits binary string corresponded to the
        input char
    """
    # get ascii value
    val = ord(char)

    # get binary string
    binary = bin(val)[2:]

    # standardized to 8 dgits
    output = (8-len(binary))*'0'+binary
    return output



def bit_string(message):
    """ This function takes in a string of message.

        This function loops though all char, and converts to 8 digits binary
        string. At the end of the bit message return, add 8 zeros.

        This funtion returns the corresponded bit string of the message with
        the end mark.
    """
    bit_string = ''
    for char in message:
        block = char_to_block(char)
        bit_string += block
    bit_string += "00000000"
    return bit_string



def modify_rgb(rgb_val, bit):
    """ This function takes in a rgb value and a bit

        This function modify the rgb value in order to let it contain the
        information we want (the input bit). If the current bit of rbg val is
        the same, do nothing. It not the same, change the last bit to input
        bit and return the corresponded integer.

        This function return the modified rgb value that conatains the bit
        we want it to contain
    """
    # get the bit of rgb_val
    binary = bin(rgb_val)[2:]
    rgb_bit = bin(rgb_val)[-1]

    # if same, do nothin
    if rgb_bit == bit:
        return rgb_val

    # otherwise, change the bit
    else:
        new_bin = binary[:-1]+bit
        output = int(new_bin,2)
        return output



# Part B: here is a signature for the encoding/embedding
# remember - you will want helper functions!
def steganographize( image_name, message ):
    """ This function takes in a image_name(string), and a message(string)
        The message consists of printable ascii characters.

        This function modifies the rgb_val of the input image and creates a
        new copy of the input image to let it contain the message input.

        This function does not return anything, it writes out the image
        with the name image_name_out.png, and this is the transformed image
        with image contained in it.

        This written image looks identicle to the original one since only
        the least important bits are modifed.
    """
    # read the image and copy for output image
    image = read_image(image_name)
    new_image = image.copy()
    num_rows, num_cols, num_chans = image.shape

    # get the bit string of message
    all_bits = bit_string(message)
    length = len(all_bits)

    # loop though all
    index = 0
    for row in range(num_rows):
        for col in range(num_cols):
            for i in range(3):

                # if already add all message, break
                if index == length:
                    break

                # if not, get original rgb_val and get the new rgb value we
                # want
                rgb_val = image[row,col][i]
                bit = all_bits[index]
                rgb = modify_rgb(rgb_val, bit)

                # set the rgb_val of the copied image to be new rgb val
                new_image[row,col][i] = rgb

                # add index to show that we contain one more bit of message
                index += 1

    # transform the dtype to be np.uint
    new_image = np.uint8(new_image)

    # get the name of the outputfile
    name = image_name[:-4] + "_out.png"

    # write out the image
    cv2.imwrite( name, new_image )
