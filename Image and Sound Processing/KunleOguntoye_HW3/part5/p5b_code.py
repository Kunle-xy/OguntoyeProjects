import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"


video_path = ['part5/p5b_video1.mp4']
for vid in video_path:
    cap = cv.VideoCapture(vid)
    output_video_path= vid.split('.')[0] + '_result.mp4'

    fourcc = cv.VideoWriter_fourcc(*'MP4V')
    frame_rate = cap.get(cv.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    out = cv.VideoWriter(output_video_path, fourcc, frame_rate, frame_size)


    window_name = 'image'
    if not cap.isOpened():
        exit()

    color_dict = {}
    data = {}


    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        # print(frame)

        if not ret:
            break

        # rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        image_GRAY = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Apply a binary threshold to the grayscale frame
        ret, image = cv.threshold(image_GRAY, 230, 255, cv.THRESH_BINARY_INV)


        kernel_erode2 = cv.getStructuringElement(cv.MORPH_RECT,(8, 8))
        kernel = cv.getStructuringElement(cv.MORPH_RECT,(25, 25))
        image = cv.erode(image, kernel_erode2, iterations=1 )
        image = ~image

        # image = cv.erode(image, kernel, iterations=1 )
        # Find contours

        contours, _ = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Draw rectangles around each contour

        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            if w*h >= 10000 and w*h <= 80000 :  # hardcoded values
                center_x, center_y = x + w//2, y + h//2
                text_img = ~image_GRAY[y:y+h, x:x+w]
                text = pytesseract.image_to_string(text_img, lang='eng', config='--psm 6')
                # print(text)
                if text not in data:
                    data[text] = []
                    data[text].append((center_x, center_y))
                else:
                    data[text].append((center_x, center_y))

                if text not in color_dict:
                    color_dict[text] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                # else:
                #     pass

                # plt.imshow(text_img, 'gray')
                # plt.show()
                    # try:
                    #     color_dict[text] = colors.pop(0)
                    # except:
                    #     color_dict[text] = (255, 255, 0)

                # print(text)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # print(data)
        for item in data:
            for ix in range(len(data[item])):
                curr = data[item][ix]
                cv.circle(frame, curr, 3, color_dict[item], -1)
                try:
                    next = data[item][ix+1]
                    cv.line(frame, curr, next,  color_dict[item], 2)
                except:
                    pass

                # cv.putText(frame, item, (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)


        # plt.imshow(frame, 'gray')
        # plt.show()

        # frame[:410, :][image[:410, :]==0]=[255, 0, 0]

        # plt.show()
        out.write(frame)
        cv.imshow("AI",frame)
        if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()
    out.release()
    cv.destroyAllWindows()