from ImgProcUtils import detect_which_lane
from cv2 import cv2
"""
    STEPS TO TAKE TO IMPLEMENT MVP

    1. Write how the labelling function will define the characteristics
            - Contained in road: either white right and yellow left or yellow left and white right
            - To check for lane: see where the yellow line is and the white line is
            - To check for Collisions: ??
            -
    2. How to control robot wheels and make the robot turn a certain amount. Calculate based on wheel encoder odometry

    3. Figure out how to randomly sample. Sample in the cameras view at different angles? Random spots on a map?

    4. Make the robot follow a path drawn on a map. Map points on the map to distances in real life.

    5. Bring both together. Generate the Kripke struture, all the MVp methods and debug.
"""

# Getting the image from the camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        else:
            cv2.imshow("Name", frame)
            # left, right = img.detectLane(frame)
            cv2.imshow("Detect left lane or right", detect_which_lane(frame))
    else:
        break

cap.release()
cv2.destroyAllWindows()

