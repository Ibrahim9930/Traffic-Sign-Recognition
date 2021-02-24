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
          'speed_limit.jpg',
          ]
kernel = np.ones((5, 5), np.uint8)
kernel_2= np.ones((3, 3), np.uint8)

np.put(kernel,[0,1,3,4,5,6,8,15,16,18,19,20,21,23,24],0)
# dilated = cv2.dilate(canned, kernel_2, iterations=1)
# eroded = cv2.erode(dilated, kernel, iterations=1)
# eroded = cv2.erode(closed, kernel, iterations=1)

for im in images:
    # Read the image
    img = cv2.imread("stage_2\\"+im,0)

    # Close small gaps
    closed_1 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_2)

    # Apply Canny
    canned = cv2.Canny(closed_1, 127, 127, apertureSize=3, )

    # Apply canny for the no_text image
    canned_2 = cv2.Canny(img, 127, 127, apertureSize=3, )

    # Closing
    closed = cv2.morphologyEx(canned, cv2.MORPH_CLOSE, kernel)

    # closing the second canny
    closed_2 = cv2.morphologyEx(canned_2, cv2.MORPH_CLOSE, kernel_2)

    cv2.imshow("Canned",closed_2)
    cv2.waitKey()
    # Find contours and hierarchy
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get the hierarchy list
    heir = hierarchy[0]


    for i, h in enumerate(heir):
        if h[3] == -1 and h[2] != -1:
            # Print the hierarchy
            print(h)

            # Assign the contour
            cnt = contours[i]

            # Draw the contour
            cv2.drawContours(closed, [cnt], 0, (127), 1)
            cv2.imshow("Original", closed)
            cv2.waitKey()

            # Make the mask
            mask = np.zeros(img.shape, np.uint8)
            cv2.drawContours(mask, [cnt], 0, 255, -1)
            pixelpoints = np.transpose(np.nonzero(mask))

            # Draw the mask
            cv2.imshow("Original", mask)
            cv2.waitKey()
            # Remove text from canned
            no_text = cv2.bitwise_and(closed_2,mask)
            cv2.imshow("Original", no_text)
            cv2.waitKey()
            break
