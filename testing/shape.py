import cv2
import numpy as np

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
          "speed_limit.jpg",
          ]
kernel = np.ones((2, 2), np.uint8)
kernel_2= np.ones((3, 3), np.uint8)

# np.put(kernel,[0,3,12,15],0)
# for img in images:
#     im = cv2.imread(img,0)
#     # dilated = cv2.dilate(im, kernel, iterations=1)
#     # closing = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)
#     # cv2.imshow("Original", closing)
#     # cv2.waitKey()
#     canned = cv2.Canny(im, 150, 200, apertureSize=3, )
#     closed = cv2.morphologyEx(canned, cv2.MORPH_CLOSE, kernel)
#     # cv2.imshow("Original", closing)
#     cv2.waitKey()
#     cv2.imshow("Original", canned)
#     cv2.waitKey()
#     cv2.imshow("Original", closed)
#     cv2.waitKey()
#
#     contours,hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     print(len(contours))
#     # cv2.drawContours(canned, contours, -1, (127), 1)
#     for i,cnt in enumerate(contours):
#         can = closed.copy()
#         contours, hierarchy = cv2.findContours(can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         print(hierarchy[0][i])
#         cv2.drawContours(can, [cnt], 0, (127), 1)
#         cv2.imshow("Original", can)
#         cv2.waitKey()


for im in images:
    # read the image
    img = cv2.imread("stage_1\\"+im, 0)

    # Show the Images
    cv2.imshow("Original", img)
    cv2.waitKey()

    # # Close small gabs before thresholding
    # closed_1 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_2)

    # Apply Canny Edge detection filter
    canned = cv2.Canny(img, 127, 127,apertureSize = 3,)
    cv2.imshow("Original", canned)
    cv2.waitKey()

    # Close the gaps in the image
    closed = cv2.morphologyEx(canned, cv2.MORPH_CLOSE, kernel)

    # Find contours and hierarchy
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get the hierarchy list
    heir = hierarchy[0]

    for i,h in enumerate(heir):
        if h[3] == -1 and h[2] != -1:
            print(h)
            cnt = contours[i]
            # Approximate the contour
            epsilon_1 = 0.025 * cv2.arcLength(cnt, True)
            approx_1 = cv2.approxPolyDP(cnt,epsilon_1,True)
            print(heir[i])
            edges = len(approx_1)
            print(edges)
            if edges == 8:
                epsilon_2 = 0.01 * cv2.arcLength(cnt, True)
                approx_2 = cv2.approxPolyDP(cnt, epsilon_2, True)
                # print(heir[i])
                print(len(approx_2))

            # Draw the contour
            cv2.drawContours(closed, [cnt], 0, (127), 1)
            cv2.imshow("Original", closed)
            cv2.waitKey()
            break

# Differentiate between bumpy road and descendent
#     print(len(contours))
#     for i,h in enumerate(heir):
#         if h[0] == -1 and h[2] == -1:
#             cnt = contours[i]
#             epsilon_tri = 0.04 * cv2.arcLength(cnt, True)
#             approx_tri = cv2.approxPolyDP(cnt, epsilon_tri, True)
#             print(len(approx_tri))



# print(len(cnt))
# for im in images:
#     img = cv2.imread(im,0)
#
#     canned = cv2.Canny(img, 100,127,3)
#     cv2.imshow("Original", canned)
#     cv2.waitKey()
#     contours, heirarchy = cv2.findContours(canned, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cnt = contours[0]
#     epsilon = 0.04*cv2.arcLength(cnt,True)
#     approx = cv2.approxPolyDP(cnt,epsilon,True)
#     print(len(approx))
#     cv2.drawContours(canned, [cnt], 0,(127), 5)
#     cv2.imshow("Original", canned)
#     cv2.waitKey()
