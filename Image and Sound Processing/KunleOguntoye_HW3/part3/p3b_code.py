import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

video_path = 'part3/p3b_video2.mp4'

output_video_path = video_path.split('.')[0] + '_result.mp4'

purple_lower = np.array([130, 50, 50])
purple_upper = np.array([160, 255, 255])

# brown_lower = np.array([150, 190, 210])
# brown_upper = np.array([195, 235, 255])

# Light brown in BGR
light_brown = [100, 42, 200]

# Open the video
cap = cv.VideoCapture(video_path)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'MP4V')
frame_rate = cap.get(cv.CAP_PROP_FPS)
frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
out = cv.VideoWriter(output_video_path, fourcc, frame_rate, frame_size)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # for purple
    # hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # for light blue

    # Create a mask for the purple/light blue color
    mask = cv.inRange(hsv_frame, purple_lower, purple_upper)

    # Change pixels with the target color to light brown
    frame[mask != 0] = light_brown

    # Write the frame to the new video
    out.write(frame)

# Release everything when job is finished
cap.release()
out.release()