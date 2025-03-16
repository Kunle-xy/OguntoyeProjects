import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


video_path = 'p3a_video1.mp4'


cap = cv.VideoCapture(video_path)

fourcc = cv.VideoWriter_fourcc(*'mp4v')  # or 'XVID', 'MJPG', 'DIVX', etc.
frame_rate = cap.get(cv.CAP_PROP_FPS)
frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
# print(frame_rate, frame_size)
output_video_path = video_path.split('.')[0] + '_test.mp4'
out = cv.VideoWriter(output_video_path, fourcc, frame_rate, frame_size, False)


window_name = 'image'
if not cap.isOpened():
  exit()


while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(frame)

    if not ret:
        break

    # rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Apply a binary threshold to the grayscale frame
    ret, image = cv.threshold(image, 230, 255, cv.THRESH_BINARY_INV)


    kernel_erode2 = cv.getStructuringElement(cv.MORPH_RECT,(8, 8))
    image = cv.erode(image, kernel_erode2, iterations=1 )
    image = ~image

    frame[:410, :][image[:410, :]==0]=[255, 0, 0]

    # plt.show()
    out.write(frame)
    cv.imshow("AI",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
out.release()
cv.destroyAllWindows()
