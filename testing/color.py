import cv2
import numpy as np
from main import Color
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
# BRG_img = cv2.imread(images[9])
# cv2.imshow("Original", BRG_img)
# cv2.waitKey()
# img = cv2.cvtColor(BRG_img, cv2.COLOR_BGR2HSV)
#
# w = img.shape[0]
# h = img.shape[1]
# h = img[50][100][0]
# s = img[50][100][1]w
# v = img[50][100][2]
# print([h,s,v])
# for im in images :

BRG_img = cv2.imread(images[1])
cv2.imshow("Original", BRG_img)
cv2.waitKey()
img = cv2.cvtColor(BRG_img, cv2.COLOR_BGR2HSV)

w = img.shape[0]
h = img.shape[1]
# h = img[33][72][0]
# s = img[33][72][1]
# v = img[33][72][2]
# print([h,s,v])
# green = np.uint8([[[h,s,v ]]])
# hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
# print(hsv_green)
#
def findColors():
    red = 0
    yellow = 0
    blue = 0
    brown = 0
    green = 0
    white = 0
    black = 0
    colors = []
    dom_clr = ""
    for i in range(w):
        for j in range(h):
            point = img[i][j]
            if point[1] < 30:
                white = white+1
            elif point[2] < 30:
                black = black+1
            elif (5 >= point[0] >= 0) or(180 >= point[0] >= 165):
                red = red+1
            elif 15 >= point[0] >= 5:
                brown = brown + 1
            elif 30 >= point[0] >=20:
                yellow = yellow + 1
            elif 85 >= point[0] >= 65:
                green = green+1
            elif 100 >= point[0] >= 90:
                blue = blue+1
            # else:
            #     print(point)

    dominant_color = max(red, brown, yellow, green, blue)
    print("red pixels number is {}".format(red))
    print("blue pixels number is {}".format(blue))
    print("green pixels number is {}".format(green))
    print("yellow pixels number is {}".format(yellow))
    print("brown pixels number is {}".format(brown))
    print("white pixels number is {}".format(white))
    print("black pixels number is {}".format(black))


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
    if yellow > 200:
        colors.append("yellow")
        # print(yellow)
    if blue > 500:
        colors.append("blue")
        # print("blue")
    if brown > 800:
        colors.append("brown")
        # print("brown")
    if green > 200:
        colors.append("green")
        # print("green")
    if red > 4500:
        colors.append("red")
        # print("red")
    if black > 300:
        colors.append("black")
        # print("black")

    clr = Color(dom_clr,colors)
    return clr
clr = findColors()
print(clr.colors)
print(clr.dominant_color)