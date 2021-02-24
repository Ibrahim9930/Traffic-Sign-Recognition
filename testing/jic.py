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

# Morphological Kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))

class Color:

    def __init__(self, dom_color = None, clrs = [],clrv=[]):

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

    def __init__(self,img):
        self.image = cv2.imread(img)
        self.HSV_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.grey_img = cv2.imread(img,0)
        self.h = self.image.shape[0]
        self.w = self.image.shape[1]
        self.area = self.h*self.w
        self.findCnts()
        self.findShape()
        self.findColours()
        self.findSign()
        # self.shape = None
        # self.color = None
        # self.contoues = None
        self.category_determined = False
        self.type_determined = False

    def findCnts(self):

        # Apply Canny
        self.canned = cv2.Canny(self.grey_img, 150, 150, apertureSize=3)

        # Close the gaps
        self.closed = cv2.morphologyEx(self.canned, cv2.MORPH_CLOSE, kernel)

        # Find Contours
        self.contours, self.hierarchy = cv2.findContours(self.canned, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    def findShape(self):
        # Initialise edges value
        self.edges = 0

        # Find outer contours to extract outer frame
        contours, hierarchy = cv2.findContours(self.closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hier = hierarchy[0]

        for i, h in enumerate(hier):
            # Assign the contour
            cnt = contours[i]
            # Find the outer contour
            if cv2.contourArea(cnt) > 600:
                # print(h)
                cv2.drawContours(self.closed,[cnt],0,(127),4)
                cv2.imshow("original",self.closed)
                cv2.waitKey()
                # Approximate the contour
                epsilon_1 = 0.025 * cv2.arcLength(cnt, True)
                # epsilon_1 = 0.045 * cv2.arcLength(cnt, True)
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
                # else:
                #     print(point)

        dominant_color = max(red, brown, yellow, green, blue)
        # print("red pixels number is {}".format(red))
        # print("blue pixels number is {}".format(blue))
        # print("green pixels number is {}".format(green))
        # print("yellow pixels number is {}".format(yellow))
        # print("brown pixels number is {}".format(brown))
        # print("white pixels number is {}".format(white))
        # print("black pixels number is {}".format(black))

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
            # print(yellow)
        if blue > 0.02 * self.area:
            colors.append("blue")
            # print("blue")
        if brown > 0.04 * self.area:
            colors.append("brown")
            # print("brown")
        if green > 0.01 * self.area:
            colors.append("green")
            # print("green")
        if red > 0.23 * self.area:
            colors.append("red")
            # print("red")
        if 0.4 * self.area > black > 0.015 * self.area:
            colors.append("black")
            # print("black")

        clr = Color(dom_clr, colors,[red,blue,green,yellow,brown,white,black])
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
        elif set(['red','blue']).issubset(set(self.color.colors)):
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
            else :
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
            self.category="Undetermined"
            self.type = "Undetermined"

    def findTri(self):
        # Extract hier
        hier = self.hierarchy[0]
        # Differentiate between bumpy road and descendent
        # if len(self.contours) > 5:
        #     self.type = "Bumpy Road"
        # elif len(self.contours) == 5:
        #     self.type = "Dangerous Descendent"
        # else:
        #     self.category = "Prohibitory Sings"
        #     self.type = "Give Way"
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
        # Find the contours
        # contours, hierarchy = cv2.findContours(self.closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Extract hier
        hier = self.hierarchy[0]

        # Find the arrow contour
        for i, h in enumerate(hier):
            if h[0] == -1 and h[1] == -1 and h[2] == -1:
                # Assigning initial values
                right = 0
                left = 0
                cnt = self.contours[i]
                # Check if the contour is for the arrow
                if cv2.arcLength(cnt, True) > 200:
                    # Find the approximation
                    epsilon = 0.02 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)
                    # Determine whether the contour is on the left of the right
                    for apx in approx:
                        if apx[0][0] < ((self.w / 2) - 15):
                            left = left + 1
                        elif apx[0][0] > ((self.w / 2) + 15):
                            right = right + 1
                    if left - right > 2:
                        self.type = "Go Left"
                    elif right - left > 2:
                        self.type = "Go Right"
                    else:
                        self.type = "Go Straight"
                    return

# for im in images:
#     img = "stage_2\\"+im
#     sign = Sign(img)
#     cv2.imshow("original",sign.image)
#     cv2.waitKey()
#     print(sign.category)
#     print(sign.type)
img = "stage_4\\bumpy_road.png"
sign = Sign(img)
print(sign.category)
print(sign.type)
print(sign.color.colors)
print(sign.edges)