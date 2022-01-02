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
# cap = cv2.VideoCapture(0)

dispW = 320
dispH = 240
flip = 2
# How to locate the camera through the PCI
camSet = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
camera = cv2.VideoCapture(camSet)

while camera.isOpened():
    ret, frame = camera.read()
    if ret:
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        else:
            cv2.imshow("Name", frame)
            # left, right = img.detectLane(frame)
            # cv2.imshow("Detect left lane or right",
            detect_which_lane(frame)
    else:
        break

camera.release()
cv2.destroyAllWindows()


"""
dispW=320 dispH=240 flip=2 camSet='nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink' camera = cv2.VideoCapture(camSet): while Ture: ret. frame=cam.read() cv2.imshow("Open_camera_window", frame) if cv2.waitKey(1)==ord('q'): break cam.release() #cv2.destroyAllWindows()"""

