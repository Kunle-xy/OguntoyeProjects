import random
import cv2 as cv
# !apt-get install tesseract-ocr -y
# !pip install pytesseract opencv-python
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

image = cv.imread('p2_image1.png',  cv.IMREAD_GRAYSCALE)
ret, thresh = cv.threshold(image, 150, 255, cv.THRESH_BINARY)

imageX  = cv.imread('p2_image1.png')
image_rgb = cv.cvtColor(imageX, cv.COLOR_BGR2RGB)

ret, image = cv.threshold(image, 230, 255, cv.THRESH_BINARY_INV)

boundingBox = image.shape[0]//4, image.shape[1]//4

result = np.zeros((4,4)).astype('object')


boundingBox = image.shape[0]//4, image.shape[1]//4
text_to_put = ""
result = np.zeros((4,4)).astype('object')
for i in range(1,5):
  for j in range(1,5):
      img = image[boundingBox[0]*(i-1) : boundingBox[0]*(i-1) + boundingBox[0] ,
                  boundingBox[1]*(j-1) :  boundingBox[1]*(j-1) + boundingBox[1]]
      if np.sum(img) > 1e6:

        text = pytesseract.image_to_string(img)
        print(f"Detected text at ({i},{j}): {text} ")
        text_to_put = f" ({i},{j})"
               # Specify the bottom-left corner of the text start (x, y coordinates)
        text_org = (25 , 25)

        # Choose the font type
        font = cv.FONT_HERSHEY_SIMPLEX

        # Font scale (font size)
        font_scale = 0.7

        # Font color in BGR (Blue, Green, Red)
        font_color = (255, 0, 0)

        # Font thickness
        thickness = 2
        cv.putText(image_rgb, text_to_put, (boundingBox[1]*(j-1)  , boundingBox[0]*(i-1) + boundingBox[0]), font, font_scale, font_color, thickness)

        # Using cv2.putText() method





