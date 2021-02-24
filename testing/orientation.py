import cv2
import numpy as np
# from main import Color
images = ["bumpy_road.jpg",
          "dangerous_descendent.jpg",
          "exit.jpg",
          "freeway_entry.jpg",
          "give_way.jpg",
          "go_left.jpg",
          "go_right.jpg",
          "go_straight.jpg",
          "local_destination.jpg",
          "major_road_sign.jpg",
          "no_entry.jpg",
          "no_parking.jpg",
          "stop_sign.jpg",
          "tourist_destination.jpg",
          "traffic_light_ahead.jpg",
          ]
kernel = np.ones((2, 2), np.uint8)
kernel_2= np.ones((3, 3), np.uint8)


# Read the image
img = cv2.imread("stage_1\\"+images[1],0)
cv2.imshow("Original",img)
cv2.waitKey()

# Find and print image size
h = img.shape[0]
w = img.shape[1]
print(h)
print(w)

# Close small gabs before thresholding
# closed_1 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_2)



# Apply Canny
canned = cv2.Canny(img, 150, 150,apertureSize = 3,)
cv2.imshow("Original", canned)
cv2.waitKey()

# Close
closed = cv2.morphologyEx(canned, cv2.MORPH_CLOSE, kernel)

# Find the contours
contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hier = hierarchy[0]

print(len(contours))

# Draw and print all the contours
# for i,h in enumerate(hier):
#     cnt = contours[i]
#     cv2.drawContours(closed, [cnt], 0, (127), 1)
#     print(h)
#     cv2.imshow("Original", closed)
#     cv2.waitKey()
#     if h[0] == -1 and h[2] == -1:
#         epsilon_tri = 0.02 * cv2.arcLength(cnt, True)
#         approx_tri = cv2.approxPolyDP(cnt, epsilon_tri, True)
#         print(len(approx_tri))
#
# for i,h in enumerate(hier):
#     if h[0] == -1 and h[1] ==-1 and h[2] == -1:
#         print(h)
#         right = 0
#         left = 0
#         cnt = contours[i]
#         if cv2.arcLength(cnt,True) > 200:
#             cv2.drawContours(closed, [cnt], 0, (127), 3)
#             cv2.imshow("Original", closed)
#             cv2.waitKey()
#             epsilon = 0.02 * cv2.arcLength(cnt, True)
#             approx = cv2.approxPolyDP(cnt, epsilon, True)
#             # print(approx)
#             print(len(approx))
#             for apx in approx:
#                 print(apx)
#                 if apx[0][0] < (w/2 - 20):
#                     left = left +1
#                 elif apx[0][0] > (w/2 + 20):
#                     right = right+1
#             print(left)
#             print(right)
#             break




# --------Helper Codes-------- #

# Draw and print all the contours
# for i,h in enumerate(heir):
#     cnt = contours[i]
#     cv2.drawContours(canned, [cnt], 0, (127), 1)
#     print(i)
#     cv2.imshow("Original", canned)
#     cv2.waitKey()


# Find and print image size
# h = new_img.shape[0]
# w = new_img.shape[1]
# print(h)
# print(w)

# Find topmost and bottommost in the contour
# topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
# bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
# Beta = 0.0001 * self.area
# if topmost[0] < 2 or topmost[1] < 2 or bottommost[0] > (self.w) or bottommost[1] > ( self.h):
#     h = self.hierarchy[0][i+1]
#     cnt  = self.contours[i+1]
#     # topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
#     # bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
#     # print("topmost is {}".format(topmost))
#     # print("bottommost is {}".format(bottommost))
# cv2.drawContours(self.closed,[cnt],0,(127),2)
# cv2.imshow("original",self.closed)
# cv2.waitKey()
# --------------

# Rotate the image
# rows,cols = OG_img.shape
# M = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
# img = cv2.warpAffine(OG_img,M,(cols,rows))
# cv2.imshow("Original", img)
# cv2.waitKey()
# for i,h in enumerate(hier):
#     if h[0] == -1 and h[1] ==-1 and h[2] == -1:
#
#         cnt = contours[i]
#         print(cv2.arcLength(cnt,True))
#         cv2.drawContours(closed, [cnt], 0, (127), 3)
#         cv2.imshow("Original", closed)
#         cv2.waitKey()
#         rect = cv2.minAreaRect(cnt)
#         print(rect)


#Convert color
# new_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# Splitting technique based on color
# left = 0
#     right = 0
#     rimg = new_img[0:rows,0:int(cols/2)]
#     limg = new_img[0:rows,int(cols/2):]
#     for i in range(limg.shape[0]):
#         for j in range(limg.shape[1]):
#             point = limg[i][j]
#             if point[1] > 30 and 100 >= point[0] >= 90:
#                 left = left+1
#     for i in range(rimg.shape[0]):
#         for j in range(rimg.shape[1]):
#             point = rimg[i][j]
#             if point[1] > 30 and 100 >= point[0] >= 90:
#                 right = right + 1
#     print(right)
#     print(left)
#     print(right - left)


# Splitting technique based on something
# rimg = new_img[0:rows,0:int(cols/2)]
# limg = new_img[0:rows,int(cols/2):]
#
# left_contours,left_hierarchy = cv2.findContours(limg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# left_canned = cv2.Canny(limg, 127, 127, apertureSize=3, )
# cv2.imshow("Original", left_canned)
# cv2.waitKey()
# right_contours,right_hierarchy = cv2.findContours(rimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# right_canned = cv2.Canny(rimg, 127, 127, apertureSize=3, )
# cv2.imshow("Original", right_canned)
# cv2.waitKey()
# print(len(left_contours))
# for i,cnt in enumerate(left_contours):
#     print(left_hierarchy[0][i])
#     cv2.drawContours(left_canned, [cnt], 0, (127), 1)
#     cv2.imshow("Original", left_canned)
#     cv2.waitKey()
# for i,cnt in enumerate(right_contours):
#     print(right_hierarchy[0][i])
#     cv2.drawContours(right_canned, [cnt], 0, (127), 1)
#     cv2.imshow("Original", right_canned)
# cv2.waitKey()


# Find the Centroid
# M = cv2.moments(cnt)
# cx = int(M['m10'] / M['m00'])
# cy = int(M['m01'] / M['m00'])
# print(cx)
# print(cy)