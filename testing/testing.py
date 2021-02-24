import cv2
import sys
import numpy as np
import random

# Image names
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


class Color:

    def __init__(self, dom_color=None, clrs=[], clrv=[]):
        self.dominant_color = dom_color
        self.colors = clrs
        self.red = clrv[0]
        self.blue = clrv[1]
        self.green = clrv[2]
        self.yellow = clrv[3]
        self.brown = clrv[4]
        self.white = clrv[5]
        self.black = clrv[6]


class Sign:

    def __init__(self, img):
        self.image = cv2.imread(img)
        self.HSV_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.grey_img = cv2.imread(img, 0)
        self.h = self.image.shape[0]
        self.w = self.image.shape[1]
        self.area = self.h * self.w
        self.findCnts()
        self.findShape()
        self.findColours()
        self.findSign()
        self.category_determined = False
        self.type_determined = False

    def findCnts(self):

        # Apply Canny
        self.canned = cv2.Canny(self.grey_img, 150, 150, apertureSize=3)

        # Closing structuring element
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        # Close the gaps
        self.closed = cv2.morphologyEx(self.canned, cv2.MORPH_CLOSE, kernel)

        # Find Contours
        self.contours, self.hierarchy = cv2.findContours(self.closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        self.removeBorder()

        self.removeText()

    def removeBorder(self):

        # Find the contours from the Canny rather than the closing
        contours, hierarchy = cv2.findContours(self.canned, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize the mask
        no_border = np.zeros(self.grey_img.shape, np.uint8)

        # Find the borders
        for i, h in enumerate(hierarchy[0]):

            cnt = contours[i]

            # Find the area of the contour
            area = cv2.contourArea(cnt)

            if area == 0 :
                # Create a mask with the border
                mask = np.zeros(self.grey_img.shape, np.uint8)
                cv2.drawContours(mask, [cnt], 0, 255, -1)

                # Add the border to the main mask
                no_border = cv2.add(no_border, mask)

        if np.array_equiv(no_border, np.zeros(self.grey_img.shape, np.uint8)):
            pass

        else:
            # Invert thr mask
            no_border_mask = cv2.bitwise_not(no_border)

            # Apply the mask
            no_border_img = cv2.bitwise_and(self.closed, no_border_mask)

            # Change the canned
            self.canned = no_border_img

            # Closing structuring element
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

            # Close the gaps
            self.closed = cv2.morphologyEx(self.canned, cv2.MORPH_CLOSE, kernel)

    def removeText(self):
        # Define the closing structuring element
        kernel_2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # ----Stage 1----


        # Initialize the mask
        no_text = np.zeros(self.grey_img.shape, np.uint8)

        # Close the main image
        closed_2 = cv2.morphologyEx(self.canned, cv2.MORPH_CLOSE, kernel_2)

        # Find external contours and hierarchy
        contours, hierarchy = cv2.findContours(self.closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hier = hierarchy[0]

        # Find the text
        for i, h in enumerate(hier):
            cnt = contours[i]
            if cv2.contourArea(cnt) < 0.15 * self.area:
                # Create a mask with the text
                mask = np.zeros(self.grey_img.shape, np.uint8)
                cv2.drawContours(mask, [cnt], 0, 255, -1)
                # Add to the main mask
                no_text = cv2.add(no_text, mask)
        if np.array_equiv(no_text, np.zeros(self.grey_img.shape, np.uint8)):
            # Use the second closing
            self.closed = closed_2

            # Find the contours for the new closed
            self.contours, self.hierarchy = cv2.findContours(self.closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            # Invert the msak
            no_text_mask = cv2.bitwise_not(no_text)

            # Apply the mask
            no_text_img = cv2.bitwise_and(closed_2, no_text_mask)
            # ----Stage 2----

            # Find contours and hierarchy for the new image
            contours, hierarchy = cv2.findContours(no_text_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hier = hierarchy[0]

            # Initialize the mask
            no_text = np.zeros(self.grey_img.shape, np.uint8)

            # Find the text
            for i, h in enumerate(hier):
                cnt = contours[i]
                if cv2.contourArea(cnt) < 0.03 * self.area:
                    # Create a mask with the text
                    mask = np.zeros(self.grey_img.shape, np.uint8)
                    cv2.drawContours(mask, [cnt], 0, 255, -1)
                    # Add to the main mask
                    no_text = cv2.add(no_text, mask)
                    # pixelpoints = np.transpose(np.nonzero(mask))

            # Invert the mask
            no_text_mask = cv2.bitwise_not(no_text)

            # Apply the mask
            no_text_img = cv2.bitwise_and(no_text_img, no_text_mask)

            # Use the second closing
            self.closed = no_text_img

            # Find the contours for the new closed
            self.contours, self.hierarchy = cv2.findContours(self.closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def findShape(self):
        # Initialise edges value
        self.edges = 0

        for i, h in enumerate(self.hierarchy[0]):
            # Assign the contour
            cnt = self.contours[i]
            # Find the outer contour
            if h[3] == -1 and h[2] != -1:

                # Approximate the contour
                epsilon_1 = 0.025 * cv2.arcLength(cnt, True)
                approx_1 = cv2.approxPolyDP(cnt, epsilon_1, True)
                self.edges = len(approx_1)
                if self.edges == 8:
                    epsilon_2 = 0.01 * cv2.arcLength(cnt, True)
                    approx_2 = cv2.approxPolyDP(cnt, epsilon_2, True)
                    self.edges = len(approx_2)
                break

        if self.edges == 3:
            self.shape = "Triangle"
        elif self.edges == 4:
            self.shape = "Rectangle"
        elif self.edges == 8:
            self.shape = "Octagon"
        elif self.edges > 8:
            self.shape = "Circle"
        else:
            self.shape = "Undetermined"

    def findColours(self):

        red = 0
        yellow = 0
        blue = 0
        brown = 0
        green = 0
        white = 0
        black = 0
        colors = []
        dom_clr = ""
        for i in range(self.h):
            for j in range(self.w):
                point = self.HSV_img[i][j]
                if point[2] < 30:
                    black = black + 1
                elif point[1] < 30:
                    white = white + 1
                elif (5 >= point[0] >= 0) or (180 >= point[0] >= 165):
                    red = red + 1
                elif 15 >= point[0] >= 5:
                    brown = brown + 1
                elif 30 >= point[0] >= 20:
                    yellow = yellow + 1
                elif 85 >= point[0] >= 65:
                    green = green + 1
                elif 100 >= point[0] >= 90:
                    blue = blue + 1

        dominant_color = max(red, brown, yellow, green, blue)

        if dominant_color == red:
            dom_clr = "red"
        elif dominant_color == brown:
            dom_clr = "brown"
        elif dominant_color == yellow:
            dom_clr = "yellow"
        elif dominant_color == green:
            dom_clr = "green"
        elif dominant_color == blue:
            dom_clr = "blue"
        else:
            dom_clr = "not defined"
        if yellow > 0.01 * self.area:
            colors.append("yellow")
        if blue > 0.02 * self.area:
            colors.append("blue")
        if brown > 0.04 * self.area:
            colors.append("brown")
        if green > 0.01 * self.area:
            colors.append("green")
        if red > 0.23 * self.area:
            colors.append("red")
        if 0.4 * self.area > black > 0.015 * self.area:
            colors.append("black")

        clr = Color(dom_clr, colors, [red, blue, green, yellow, brown, white, black])
        self.color = clr

    def findSign(self):
        # Based on colors alone
        if 'brown' in self.color.colors:
            self.category = "Information Sign"
            self.type = "Tourist Destination"
        elif 'yellow' in self.color.colors:
            if 'green' in self.color.colors:
                self.category = "Warning Sign"
                self.type = "Traffic Lights Ahead"
            else:
                self.category = "Information Sign"
                self.type = "Exit"
        elif 'green' in self.color.colors:
            self.category = "Information Sign"
            self.type = "Major Road Sign"
        elif set(['red', 'blue']).issubset(set(self.color.colors)):
            self.category = "Prohibitory Signs"
            self.type = "No Parking"
        elif self.edges == 3:
            if 'yellow' in self.color.colors:
                self.category = "Warning Sign"
                self.type = "Traffic Lights Ahead"
            elif 'black' in self.color.colors:
                self.category = "Warning Sign"
                self.findTri()
            else:
                self.category = "Prohibitory Signs"
                self.type = "Give Way"
        elif self.edges == 4:
            self.category = "Information Sign"

            if 'yellow' in self.color.colors:
                self.type = "Exit"
            elif "blue" in self.color.colors:
                self.type = "Freeway Entry"
            elif "green" in self.color.colors:
                self.type = "Major Road Sign"
            else:
                self.type = "Undetermined"
        elif self.edges == 5:
            self.category = "Information Sign"
            if 'brown' in self.color.colors:
                self.type = "Tourist Destination"
            else:
                self.type = "Local Destination"
        elif self.edges == 8:
            self.category = "Prohibitory Signs"
            self.type = "Stop"
        elif self.edges > 8:
            if 'red' in self.color.colors:
                self.category = "Prohibitory Signs"
                if 'blue' in self.color.colors:
                    self.type = "No Parking"
                else:
                    self.type = "No Entry"
            elif 'blue' in self.color.colors:
                self.category = "Direction Sings"
                self.findOrientation()
            else:
                self.category = "Information Signs"
                self.type = "End Speed Limit"
        else:
            self.category = "Undetermined"
            self.type = "Undetermined"

    def findTri(self):
        # Extract hier
        hier = self.hierarchy[0]

        for i, h in enumerate(hier):
            if h[0] == -1 and h[2] == -1:
                cnt = self.contours[i]
                epsilon_tri = 0.02 * cv2.arcLength(cnt, True)
                approx_tri = cv2.approxPolyDP(cnt, epsilon_tri, True)
                if len(approx_tri) >= 4:
                    self.type = "Bumpy Road"
                elif len(approx_tri) == 4:
                    self.type = "Give way"
                else:
                    self.type = "Dangerous Descendent"

    def findOrientation(self):
        # Extract hier
        hier = self.hierarchy[0]

        # Initialize the count
        count = 0

        # Find the arrow contour and the arrow count
        for i, h in enumerate(hier):
            if h[0] == -1 and h[1] == -1 and h[2] == -1:
                cnt = self.contours[i]
                if cv2.arcLength(cnt, True) > 200:

                    self.arrow_cnt = self.contours[i]
                    count = count+1

        if count > 1:
            self.type = "Circular"
        else :
            # Assigning initial values
            right = 0
            left = 0
            cnt = self.arrow_cnt
            (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)
            print(angle)

            if angle > 120 :
                self.type = "Go Straight"
                return

            # Find the approximation
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # Determine whether the contour is on the left of the right
            for apx in approx:
                if apx[0][0] < ((self.w / 2) - 15):
                    left = left + 1
                elif apx[0][0] > ((self.w / 2) + 15):
                    right = right + 1
            if left  > right:
                self.type = "Go Left"
            else:
                self.type = "Go Right"
            return



def stage1_images(sign = "all",show = True):
    if sign == "all":
        for im in images:
            img = "stage_1\\"+im
            sign = Sign(img)
            if show == True:
                cv2.imshow("original",sign.image)
                cv2.waitKey()
            print(sign.category)
            print(sign.type)
    else:
        img = "stage_1\\" + sign + ".jpg"
        sign = Sign(img)
        if show == True:
            cv2.imshow("original", sign.image)
            cv2.waitKey()
        print(sign.category)
        print(sign.type)

def stage2_images(sign = "all",show = True):
    if sign == "all":
        for im in images:
            img = "stage_2\\"+im
            sign = Sign(img)
            if show == True:
                cv2.imshow("original",sign.image)
                cv2.waitKey()
            print(sign.category)
            print(sign.type)
    else:
        img = "stage_2\\" + sign + ".jpg"
        sign = Sign(img)
        if show == True:
            cv2.imshow("original", sign.image)
            cv2.waitKey()
        print(sign.category)
        print(sign.type)

def stage3_images(sign = "all",show = True):
    if sign == "all":
        for im in stage_3_images:
            img = "stage_3\\"+im
            sign = Sign(img)
            if show == True:
                cv2.imshow("original",sign.image)
                cv2.waitKey()
            print(sign.category)
            print(sign.type)
    else:
        img = "stage_3\\" + sign + ".png"
        sign = Sign(img)
        if show == True:
            cv2.imshow("original", sign.image)
            cv2.waitKey()
        print(sign.category)
        print(sign.type)

def stage4_images(sign = "all",show = True):
    if sign == "all":
        for im in stage_4_images:
            img = "stage_4\\"+im
            sign = Sign(img)
            if show == True:
                cv2.imshow("original",sign.image)
                cv2.waitKey()
            print(sign.category)
            print(sign.type)
    else:
        img = "stage_4\\" + sign + ".png"
        sign = Sign(img)
        if show == True:
            cv2.imshow("original", sign.image)
            cv2.waitKey()
        print(sign.category)
        print(sign.type)



