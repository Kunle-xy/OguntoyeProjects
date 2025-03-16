import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

video_path = 'part4/p4a_video1.mp4'
cap = cv.VideoCapture(video_path)
output_video_path= video_path.split('.')[0] + '_result.mp4'

fourcc = cv.VideoWriter_fourcc(*'MP4V')
frame_rate = cap.get(cv.CAP_PROP_FPS)
frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
out = cv.VideoWriter(output_video_path, fourcc, frame_rate, frame_size)

kernel_erode = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

total = 576045//4
text = 'Hello, World!'
font = cv.FONT_HERSHEY_SIMPLEX  # Font type
org = (400, 410)  # Bottom-left corner of the text string in the image
fontScale = 0.7  # Font scale
color = (0, 0, 255)  # Text color (BGR)
thickness = 2
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    _, thresh = cv.threshold(frame[370:410, 330:460], 127, 255, cv.THRESH_BINARY_INV)
    erode = cv.erode(thresh, kernel_erode, iterations=1 )
    erode = cv.dilate(erode, kernel_erode, iterations=1 )

    number = round(erode.sum()/total)
    # number = erode.sum()
    text = f'chances remaining: {int(number)}'
    cv.putText(frame, text, org, font, fontScale, color, thickness, cv.LINE_AA)



    # plt.imshow(erode)
    # print(number, thresh.sum(), erode.sum())
    # # plt.axis('off')
    # plt.show()

    out.write(frame)

# Release everything when job is finished
cap.release()
out.release()