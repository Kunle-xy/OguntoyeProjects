import cv2 as cv
import numpy as np

import matplotlib.pyplot as plt

import random
# !apt-get install tesseract-ocr -y
# !pip install pytesseract opencv-python
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

image = cv.imread('p1_image2.png',  cv.IMREAD_GRAYSCALE)
ret, thresh = cv.threshold(image, 150, 255, cv.THRESH_BINARY)

imageX  = cv.imread('p1_image2.png')
image_rgb = cv.cvtColor(imageX, cv.COLOR_BGR2RGB)

# ret, image = cv.threshold(image, 230, 255, cv.THRESH_BINARY_INV)

boundingBox = image.shape[0]//4, image.shape[1]//4

result = np.zeros((4,4)).astype('object')

for i in range(1,5):
  for j in range(1,5):
      # print(data)
      try:
        img = image_rgb[boundingBox[0]*(i-1) : boundingBox[0]*(i-1) + boundingBox[0] ,
                  boundingBox[1]*(j-1) :  boundingBox[1]*(j-1) + boundingBox[1]]
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        (x, y, w, h) = (data['left'][1] + boundingBox[1]*(j-1), data['top'][1] + boundingBox[0]*(i-1),
                        data['width'][1], data['height'][1])
        # print(x,y,w,h)
      except:
        img = image[boundingBox[0]*(i-1) : boundingBox[0]*(i-1) + boundingBox[0] ,
                  boundingBox[1]*(j-1) :  boundingBox[1]*(j-1) + boundingBox[1]]
        img = cv.equalizeHist(img)
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        (x, y, w, h) = (data['left'][1] + boundingBox[1]*(j-1), data['top'][1] + boundingBox[0]*(i-1),
                        data['width'][1], data['height'][1])
        # pass
      cv.rectangle(image_rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)

plt.imshow(image_rgb, cmap='gray')
plt.axis('off')
plt.savefig("p1_image2_with_boxes.png", bbox_inches='tight')
