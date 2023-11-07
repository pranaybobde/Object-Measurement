import cv2
import numpy as np

def get_contours(img, threshold=[150,150], canny = False, min_area = 1000, filter = 0, draw = False):
# def get_contours(img, threshold=[150,150], canny = False):

    kernel = np.ones([5,5])

    gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur_img = cv2.GaussianBlur(gray_scale_img, (5,5), 1)
    
    canny_img = cv2.Canny(blur_img, threshold[0], threshold[1])

    dial_img = cv2.dilate(canny_img, kernel, iterations=3)

    threshold_img = cv2.erode(dial_img, kernel, iterations=2)

    if canny:
        threshold_img = cv2.resize(threshold_img, (0, 0), None, 0.5, 0.5)
        cv2.imshow("canny", threshold_img)

    contours, hierarchy = cv2.findContours(canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    list_contours = []

    for i in contours:
        area = cv2.contourArea(i)

        if area > min_area:
            perimeter = cv2.arcLength(i, True)
            corner = cv2.approxPolyDP(i, 0.02*perimeter, True)
            bounding_box = cv2.boundingRect(corner)

            if filter > 0:
                if len(corner) == filter:
                    list_contours.append((len(corner), area, corner, bounding_box, i))
            else:
                list_contours.append((len(corner), area, corner, bounding_box, i))

    list_contours = sorted(list_contours, key = lambda x:x[1], reverse=True)

    if draw:
        for cnt in list_contours:
            cv2.drawContours(img, cnt[4], -1, (255, 0, 0), 4)

    return img, list_contours


def reorder(cnt_points):
    print(cnt_points.shape, "-------original shape-------------->")
    new_cnt_points = np.zeros_like(cnt_points)
    cnt_points = cnt_points.reshape(4, 2)
    add = cnt_points.sum(1)
    new_cnt_points[0] = cnt_points[np.argmin(add)]
    new_cnt_points[3] = cnt_points[np.argmax(add)]
    diff = np.diff(cnt_points, axis = 1)
    new_cnt_points[1] = cnt_points[np.argmin(diff)]
    new_cnt_points[2] = cnt_points[np.argmax(diff)]

    return new_cnt_points



def img_warp(img, points, w, h, pad = None):
    # print(points)
    # print("------------------------")
    # print("------------------------")
    # print("------------------------")
    # print(reorder(points))

    points = reorder(points)

    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warp = cv2.warpPerspective(img, matrix, (w, h))

    # for adding paddingto the transformed image
    # warp = warp[pad:warp.shape[0]+pad, pad:warp.shape[1]+pad]

    return warp


def magnitude(pts1, pts2):
    return ((pts2[0] - pts1[0])**2 + (pts2[1] - pts1[1])**2)**0.5


