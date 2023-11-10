import cv2
import numpy as np
from utils import *

webcam = True
img_dir = "demo.jpg"

cap = cv2.VideoCapture(0)

cap.set(10, 160)
cap.set(3, 1920)
cap.set(4, 1080)

paper_w = 210
paper_h = 297

scale = 2

# for videos 
if webcam:
    while True:
        ret, img = cap.read()
    
        # img_cnt, list_contours = get_contours(img, canny=True, draw = True)

        img_cnt, list_contours = get_contours(img, canny=True, min_area=50000)

        if len(list_contours) != 0:
            biggest = list_contours[0][2]
            # print(biggest)

            warp = img_warp(img, biggest, paper_w*scale, paper_h*scale)

            img_cnt2, list_contours2 = get_contours(warp, min_area=1000, threshold=[200, 200])

            if len(list_contours2) != 0:
                for obj in list_contours2:
                    cv2.polylines(img_cnt2, [obj[2]], True, (255,0,255), 2)

                    new_points = reorder(obj[2])
                    new_width = round((magnitude(new_points[0][0]//scale, new_points[1][0]//scale)/10),1)
                    new_height = round((magnitude(new_points[0][0]//scale, new_points[2][0]//scale)/10),1)
                    
                    # cv2.arrowedLine(img_cnt2, (new_points[0][0][0], new_points[0][0][1]), (new_points[1][0][0], new_points[1][0][1]),
                                    # (255, 0, 255), 3, 8, 0, 0.05)
                    # cv2.arrowedLine(img_cnt2, (new_points[0][0][0], new_points[0][0][1]), (new_points[2][0][0], new_points[2][0][1]),
                                    # (255, 0, 255), 3, 8, 0, 0.05)

                    x, y, w, h = obj[3]
                    cv2.putText(img_cnt2, '{}cm'.format(new_width), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (25, 0, 255), 2)
                    cv2.putText(img_cnt2, '{}cm'.format(new_height), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (25, 0, 255), 2)

        
        img = cv2.resize(img, (0,0), None, 0.5, 0.5)

        cv2.imshow("Frame", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release() 
    cv2.destroyAllWindows()

# for images
else:
    img = cv2.imread(img_dir)

    img_cnt, list_contours = get_contours(img, canny=True, min_area=50000)

    if len(list_contours) != 0:
        biggest = list_contours[0][2]
        # print(biggest)

        warp = img_warp(img, biggest, paper_w*scale, paper_h*scale)

        img_cnt2, list_contours2 = get_contours(warp, min_area=1000, threshold=[200, 200])

        if len(list_contours2) != 0:
            for obj in list_contours2:
                cv2.polylines(img_cnt2, [obj[2]], True, (255,0,255), 2)

                new_points = reorder(obj[2])
                new_width = round((magnitude(new_points[0][0]//scale, new_points[1][0]//scale)/10),1)
                new_height = round((magnitude(new_points[0][0]//scale, new_points[2][0]//scale)/10),1)
                
                # cv2.arrowedLine(img_cnt2, (new_points[0][0][0], new_points[0][0][1]), (new_points[1][0][0], new_points[1][0][1]),
                                # (255, 0, 255), 3, 8, 0, 0.05)
                # cv2.arrowedLine(img_cnt2, (new_points[0][0][0], new_points[0][0][1]), (new_points[2][0][0], new_points[2][0][1]),
                                # (255, 0, 255), 3, 8, 0, 0.05)

                x, y, w, h = obj[3]
                cv2.putText(img_cnt2, '{}cm'.format(new_width), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (25, 0, 255), 2)
                cv2.putText(img_cnt2, '{}cm'.format(new_height), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (25, 0, 255), 2)

        cv2.imshow("Transformed Image", img_cnt2)
    else:
        print("-----------------empty------------------>")
        
    img = cv2.resize(img, (0,0), None, 0.5, 0.5)

    cv2.imshow("Frame", img)

    cv2.waitKey(0)









