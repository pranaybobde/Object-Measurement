# # l = []
# # l.append((1,2,3,4))
# # print(l)

import cv2

# webcam = False

# cap = cv2.VideoCapture(0)

# img_path = "output_3.png"

# path = img_path.split(".")
# filename = f"{path[0]}_copy.{path[1]}"

# if webcam:
#     while True:
#         ret, img = cap.read()

#         cv2.imshow("frame", img)

#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# else:
#     img = cv2.imread(img_path)

#     img = cv2.resize(img, (0, 0), None, 0.3, 0.3)

#     cv2.imshow("frame", img)

#     cv2.imwrite(filename, img)

#     cv2.waitKey(0)

file = "1.jpg"

img = cv2.imread(file)

print(img.shape)