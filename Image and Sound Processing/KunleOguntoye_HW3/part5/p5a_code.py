import cv2
import numpy as np

# Open the video
# video_path = 'backgammon.m4v'  # Change to your video path
video_path = 'part5/p5a_video3.mp4'
cap = cv.VideoCapture(video_path)
output_video_path= video_path.split('.')[0] + '_result.mp4'

fourcc = cv.VideoWriter_fourcc(*'MP4V')
frame_rate = cap.get(cv.CAP_PROP_FPS)
frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
out = cv.VideoWriter(output_video_path, fourcc, frame_rate, frame_size)

# Check if video opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Initialize the motion history image
ret, frame = cap.read()
if not ret:
    print("Failed to read the video")
    cap.release()
    exit()

frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mhist = np.zeros_like(frame_gray, dtype=np.uint8)  # Motion history image

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate difference
    diff = cv2.absdiff(current_frame_gray, frame_gray)
    # plt.imshow(diff, 'gray')
    # plt.show()
    change = diff > 50
    mhist[change] = 255

    # Display the motion history
    # plt.imshow(mhist, 'gray')
    # plt.show()
    # Decay the motion history


    if cv2.waitKey(int(1000 / cap.get(cv2.CAP_PROP_FPS))) & 0xFF == ord('q'):
        break

    # Update the previous frame
    frame_gray = current_frame_gray
    out.write(cv.cvtColor(mhist, cv.COLOR_GRAY2BGR))
    mhist = cv2.subtract(mhist, 5)

# Release everything when job is finished
cap.release()
out.release()
