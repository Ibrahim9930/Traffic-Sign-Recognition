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
stage_3_images = ["bumpy_road.png",
                  "give_way.png",
                  "no_parking.png",
                  "stop.png",
                  "tourist_destination.png",
                  "traffic_lights_ahead.png",
                  ]
stage_4_images = ["bumpy_road.png",
                  "circular.png",
                  "sign.png",
                  "traffic.png",
                  ]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
kernel_2 = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

for im in stage_3_images:

    # Read the image
    img = cv2.imread("stage_3\\"+im ,0)

    # Initialize the mask
    no_text = np.zeros(img.shape, np.uint8)

    # Apply Canny
    canned = cv2.Canny(img, 150, 150,apertureSize=3)

    # Close the image used to extract the text
    closed = cv2.morphologyEx(canned, cv2.MORPH_CLOSE, kernel)
    closed_2 = cv2.morphologyEx(canned, cv2.MORPH_CLOSE, kernel_2)

    # Find contours and hierarchy
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hier = hierarchy[0]



    for i, h in enumerate(hier):
        cnt = contours[i]
        if cv2.contourArea(cnt) < 5000:
            mask = np.zeros(img.shape, np.uint8)
            cv2.drawContours(mask, [cnt], 0, 255, -1)
            no_text = cv2.add(no_text,mask)
            # pixelpoints = np.transpose(np.nonzero(mask))

    # Invert the msak
    no_text_mask = cv2.bitwise_not(no_text)

    # Apply the mask
    no_text_img = cv2.bitwise_and(closed_2, no_text_mask)

    # Find contours and hierarchy
    contours, hierarchy = cv2.findContours(no_text_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hier = hierarchy[0]

    no_text = np.zeros(img.shape, np.uint8)

    # Find the text
    for i, h in enumerate(hier):
        cnt = contours[i]
        if cv2.contourArea(cnt) < 600:
            mask = np.zeros(img.shape, np.uint8)
            cv2.drawContours(mask, [cnt], 0, 255, -1)
            no_text = cv2.add(no_text, mask)
            # pixelpoints = np.transpose(np.nonzero(mask))

    # Invert the msak
    no_text_mask = cv2.bitwise_not(no_text)

    # Apply the mask
    no_text_img = cv2.bitwise_and(no_text_img, no_text_mask)

    # Find all the hierarchies
    contours, hierarchy = cv2.findContours(no_text_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hier = hierarchy[0]

    for i, h in enumerate(hier):
        cnt = contours[i]
        # print(h)
        # t=no_text_img.copy()
        # cv2.drawContours(t,[cnt],0,(127),3)
        # cv2.imshow("original",t)
        # cv2.waitKey()
        if h[3] == -1 and h[2] != -1:
            cv2.drawContours(no_text_img, [cnt], 0, (127), 2)
            cv2.imshow("original",no_text_img)
            cv2.waitKey()
            # Approximate the contour
            epsilon_1 = 0.025 * cv2.arcLength(cnt, True)
            # epsilon_1 = 0.045 * cv2.arcLength(cnt, True)
            approx_1 = cv2.approxPolyDP(cnt, epsilon_1, True)
            edges = len(approx_1)
            if edges == 8:
                epsilon_2 = 0.01 * cv2.arcLength(cnt, True)
                approx_2 = cv2.approxPolyDP(cnt, epsilon_2, True)
                edges = len(approx_2)
            print(edges)
            break
    # --------------Helper functions--------------
    # Find the text
    # for i, h in enumerate(hier):
    #     cnt = contours[i]
    #     if cv2.contourArea(cnt) < 600:
    #         mask = np.zeros(img.shape, np.uint8)
    #         cv2.drawContours(mask, [cnt], 0, 255, -1)
    #         no_text = cv2.add(no_text,mask)
    #         # pixelpoints = np.transpose(np.nonzero(mask))


    # # Find contours and hierarchy
    # contours, hierarchy = cv2.findContours(no_text_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    # # Get the hierarchy list
    # heir = hierarchy[0]
    #
    # for i, h in enumerate(heir):
    #     if h[3] == -1 and h[2] != -1:
    #         print(h)
    #         cnt = contours[i]
    #         # Approximate the contour
    #         epsilon_1 = 0.025 * cv2.arcLength(cnt,  True)
    #         approx_1 = cv2.approxPolyDP(cnt, epsilon_1, True)
    #         print(heir[i])
    #         edges = len(approx_1)
    #         print(edges)
    #         if edges == 8:
    #             epsilon_2 = 0.01 * cv2.arcLength(cnt, True)
    #             approx_2 = cv2.approxPolyDP(cnt, epsilon_2, True)
    #             # print(heir[i])
    #             print(len(approx_2))
    #
    #         # Draw the contour
    #         cv2.drawContours(closed, [cnt], 0, (127), 1)
    #         cv2.imshow("original", closed)
    #         cv2.waitKey()
    #         break


    # cv2.imshow("original", cv2.bitwise_not(no_text))
    # cv2.waitKey()

# np.put(kernel,[0,1,3,4,5,6,8,15,16,18,19,20,21,23,24],0)

# for im in images:
#
#     # Read Image
#     img = cv2.imread("stage_2\\"+im,0)
#
#     # Apply Canny
#     canned = cv2.Canny(img, 150, 150, apertureSize=3)
#
#     # Close the gaps
#     closed = cv2.morphologyEx(canned, cv2.MORPH_CLOSE, kernel)
#
#     # Find Contours and Hierarchy
#     contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     # Get the external hierarchy
#     hier = hierarchy[0]
#
#     for i,h in enumerate(hier):
#         if h[0] == -1 :
#             cnt = contours[i]
#             print(h)
#             # Approximate the contour
#             epsilon_1 = 0.025 * cv2.arcLength(cnt, True)
#             approx_1 = cv2.approxPolyDP(cnt, epsilon_1, True)
#             print(h)
#             edges = len(approx_1)
#             print(edges)
#             if edges == 8:
#                 epsilon_2 = 0.01 * cv2.arcLength(cnt, True)
#                 approx_2 = cv2.approxPolyDP(cnt, epsilon_2, True)
#                 # print(heir[i])
#                 print(len(approx_2))
#
#             # Draw the contour
#             cv2.drawContours(closed, [cnt], 0, (127), 3)
#             cv2.imshow("Original", closed)
#             cv2.waitKey()
#             # break
