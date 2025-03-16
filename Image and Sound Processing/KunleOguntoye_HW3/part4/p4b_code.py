import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

video_path = 'part4/p4b_video2.mp4'
cap = cv.VideoCapture(video_path)
output_video_path= video_path.split('.')[0] + '_result.mp4'

fourcc = cv.VideoWriter_fourcc(*'MP4V')
frame_rate = cap.get(cv.CAP_PROP_FPS)
frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
out = cv.VideoWriter(output_video_path, fourcc, frame_rate, frame_size)
color_ranges = {
    'Blue': np.array([176.0, 193.06, 236.0]),
    'Green': np.array([156.41, 193.73, 86.6]),
    'Purple': np.array([185.06, 125.6, 192.8]),
    'Yellow': np.array([246.0, 221.0, 107.0])
}

midLine = [60, 147, 237, 327]
def test(img):
    res = []
    gray = cv.cvtColor(img[:, :100], cv.COLOR_RGB2GRAY)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        # Approximate the contour to a polygon
        epsilon = 0.05 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        for vertex in approx:
            x, y = vertex[0]
            if x < 10:
                if y <= 99:
                    mid_score = midLine[0]
                elif 100 <= y and y <= 191:
                    mid_score = midLine[1]
                elif 191 <= y and y <= 280:
                    mid_score = midLine[2]
                else:
                    mid_score = midLine[3]

                # score = np.argmin([abs(y - i) for i in midLine])
                # mid_score = midLine[score]
                if y < mid_score:
                    res.append((y + 10, x + 10 ))
                else:
                    res.append((y - 10 , x + 10))

                return (True, (y, x), (res[0][1], res[0][0]), res, score)

tmp_l = ['Colors:']
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    ret = test(frame)
    text = " ".join(tmp_l)

    if ret:
        score = []
        color = frame[ret[2][1], ret[2][0]]
        for key, value in color_ranges.items():
            score.append(np.linalg.norm(color - value))
        if list(color_ranges.keys())[np.argmin(score)] + " ->" != tmp_l[-1]:
            tmp_l.append(list(color_ranges.keys())[np.argmin(score)] + " ->")
            text = " ".join(tmp_l)

        # print(text)


        # print(ret[1],  ret[4], tmp_l)
        # cv.circle(frame, (ret[1][1], ret[1][0]), 3, (255, 0, 0), -1)
        # plt.imshow(frame)
        # plt.show()
        # plt.axis("off")
    cv.putText(frame, text, (10, 350) , cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    out.write(cv.cvtColor(frame, cv.COLOR_RGB2BGR))

# Release everything when job is finished
cap.release()
out.release()