import numpy as np
from cv2 import cv2

vertical_limit = 2 / 3  # This number should be less than 1. It is how much of the the frame is considered.


def detect_which_lane(image):
    """
        This method should return a single value that tells if we are in the left lane or the right lane
    """
    lane = "NoneType"
    white_lower_hsv = np.array([50, 0, 200])
    white_upper_hsv = np.array([150, 100, 255])
    yellow_lower_hsv = np.array([10, 110, 0])  # 10, 110, 0
    yellow_upper_hsv = np.array([45, 255, 255])  # 45, 255, 255

    image = image[int(len(image) * vertical_limit):]
    halfway = int(len(image[0]) / 2)
    image_left = image[:, :halfway]
    image_right = image[:, halfway:]

    mask_yellow_left = cv2.inRange(image_left, yellow_lower_hsv, yellow_upper_hsv)
    mask_yellow_right = cv2.inRange(image_right, yellow_lower_hsv, yellow_upper_hsv)

    sum_left_yellow = sum(sum(mask_yellow_left[:, :]))
    sum_right_yellow = sum(sum(mask_yellow_right[:, :]))

    if sum_right_yellow > sum_left_yellow:
        lane = "right"
    else:
        lane = "left"

    cv2.imshow("left", mask_yellow_left)
    cv2.imshow("right", mask_yellow_right)

    mask_white_left = cv2.inRange(image_left, white_lower_hsv, white_upper_hsv)
    mask_white_right = cv2.inRange(image_right, white_lower_hsv, white_upper_hsv)

    sum_left_white = sum(sum(mask_white_left[:, :]))
    sum_right_white = sum(sum(mask_white_right[:, :]))

    if sum_right_white > sum_left_white:
        lane = lane + "right"
    else:
        lane = lane + "left"

    return lane


"""
arr = misc.imread(image)
        arr_list=arr.tolist()
        r=g=b=0
        for row in arr_list:
            for item in row:
                r=r+item[0]
                g=g+item[1]
                b=b+item[2]  
        total=r+g+b
        red=r/total*100
        green=g/total*100
        blue=b/total*100
"""
