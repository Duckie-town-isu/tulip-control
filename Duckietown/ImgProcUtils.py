from cv2 import cv2
from scipy import misc
import numpy as np

#This will always return 0 not sure if you need this line. 
vertical_limit = 2//3  # This number should be less than 1. It is how much of the the frame is considered.


def detect_which_lane(image):
    """
        This method should return a single value that tells if we are in the left lane or the right lane
    """
    white_lower_hsv = np.array([50, 0, 200])
    white_upper_hsv = np.array([150, 100, 255])
    yellow_lower_hsv = np.array([10, 110, 0])     # 10, 110, 0
    yellow_upper_hsv = np.array([45, 255, 255])   # 45, 255, 255
    
    
    image = image[int(len(image)*vertical_limit):]
    #You need //(integer division just in case if the number is odd)
    halfway = int(len(image[0])//2)
    image_left = image[:, :halfway]
    image_right = image[:, halfway:]
    
    #When you do inrange the return is 2-d array. Picture only picks out colors in range and modify the array/
    mask_white_left = cv2.inRange(image_left, white_lower_hsv, white_upper_hsv)
    mask_yellow_left = cv2.inRange(image_left, yellow_lower_hsv, yellow_upper_hsv)

    mask_white_right = cv2.inRange(image_right, white_lower_hsv, white_upper_hsv)
    mask_yellow_right = cv2.inRange(image_right, yellow_lower_hsv, yellow_upper_hsv)
    
    #Adding these lines for your understanding
    print(mask_white_right.shape)
    print(mask_white_left.shape)
    print(mask_yellow_right.shape)
    print(mask_yellow_left.shape)
    
    print("left yellow ", sum(mask_yellow_left))
    # print("left white  ", sum(mask_white_left[0:0, 0]))
    #you Need less indicies here. Your image just converted to 2-d array
    print("right yellow  ", sum(mask_yellow_right[:, :]))
    # print("right white   ", sum(mask_white_right[0]))

    cv2.imshow("left", mask_yellow_left[:, :])
    cv2.waitKey(0)
    cv2.imshow("right", mask_yellow_right)
    cv2.waitKey(0)
    return image

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
