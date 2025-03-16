import cv2 as cv
import numpy as np
from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt


# Part 1a

img = cv.imread('image_part1a.png', cv.IMREAD_GRAYSCALE) # read image

kernel_erode = cv.getStructuringElement(cv.MORPH_RECT,(50, 1)) # create a kernel for erosion
kernel_dilate = cv.getStructuringElement(cv.MORPH_RECT,(90, 1)) # create a kernel for dilation

img2 = (img == 255).astype(np.uint8)    # 1 is the foreground (lines) and 0 is the background

erosion = cv.erode(img2,kernel_erode,iterations = 1) # apply erosion
dilate = cv.dilate(erosion, kernel_dilate, iterations=1, borderValue=0) # apply dilation

imgb = cv.imread('image_part1b.png', cv.IMREAD_GRAYSCALE) # read image
ret, img2b = cv.threshold(imgb, 200, 255, cv.THRESH_BINARY) # threshold the image

partb = (img2b == 0).astype(np.uint8) # 0 is the background
result_horizontal = partb + dilate # add the two images

plt.imshow(result_horizontal, cmap='gray') # show the result

# Part 1b

img = cv.imread('image_part1a.png', cv.IMREAD_GRAYSCALE)

kernel_dilate = cv.getStructuringElement(cv.MORPH_RECT,(1, 50))
kernel_erode = cv.getStructuringElement(cv.MORPH_RECT,(1, 90))

img2 = (img == 255).astype(np.uint8)

dilate = cv.dilate(img2, kernel_dilate, iterations=1 )
erosion = cv.erode(dilate,kernel_erode,iterations = 1, borderValue=1)

result_vertical = partb + erosion
plt.imshow(result_vertical, cmap='gray')

