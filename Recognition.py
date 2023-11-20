import cv2
import numpy as np
import os 
from djitellopy import tello
import time

# def control_drone(drone, face_center_x, w, pid, pError):

#     ## PID ##
#     error = face_center_x - w // 2
#     speed = pid[0]*error + pid[1]*(error-pError)
#     speed = np.clip(speed, -100, 100)
#     print(speed)
#     # print("Dette er face_center_x: ", face_center_x)
#     # print("W: ", w)


#     if face_center_x != 0:
#         # drone.yaw_velocity = speed
#         pass
#     else:
#         # drone.for_back_velocity = 0
#         # drone.left_right_velocity = 0
#         # drone.up_down_velocity = 0 
#         # drone.yaw_velocity = 0
#         error = 0
#         print("No")
    
#     # if drone.send_rc_control:
#     #     drone.send_rc_control(drone.left_right_velocity, 
#     #                           drone.for_back_velocity, 
#     #                           drone.up_down_velocity, 
#     #                           drone.yaw_velocity)
    
#     return error

########################################################################
#Drone del)
drone = tello.Tello()
drone.connect()

print("Batteristatus(%):)", drone.get_battery())


drone.takeoff()

drone.move_up(50)

########################################################################


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/Users/vetlesjaberg/Documents/Minverden/Universitet/Elektronikkingeniør/5semester/ELVE3610/Prosjekt/Python/Mains/ProsjektH/Robotikk/trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml");
font = cv2.FONT_HERSHEY_SIMPLEX #iniciate id counter
id = 0 # names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Vetle', 'Christina', 'Haavard', 'Kimberly', 'W'] # Initialize and start realtime video capture
drone.streamon()
cam = cv2.VideoCapture('udp://@0.0.0.0:11111')
# cam = cv2.VideoCapture(0)

width = 640
height = 480
cam.set(3, width)
cam.set(4, height)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

hkf = 0
v = 0
v1 = 0
v2 = 0
v3 = 0 
c = 0
k = 0

pid = [0.5, 0.5, 0]
pError = 0

while True:
    ret, img = cam.read() # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                # If confidence is less them 100 ==> "0" : perfect match 
        # print("This is w: ", w)
        # print("Confidense before: ", confidence)

        # face_center_x = x + w // 2

        if (confidence < 100):
            id = names[id]
            # print("Confidence 1: ", confidence)
            confidence = 100 - confidence
            # print("Confidence: ", confidence)
            if confidence > 5: 
                # if hkf != 1: 
                # #     if id == "Haavard":
                # #         print("ID is 3", id)
                # #         print("The drone rotates counter clockwise")
                # #         drone.rotate_counter_clockwise(360)
                # #         hkf = hkf + 1
                #     drone.rotate_counter_clockwise(360)
                #     hkf = hkf + 1
                # if v != 1:   
                #     if id == "Vetle":
                #         if v1 != 1:
                #             print("ID is 1", id)
                #             v1 = v1 + 1
                #         # pError = control_drone(drone, face_center_x, w, pid, pError)
                #             print("w: ", w)
                        
                #             if w <= 140:
                #                 drone.send_rc_control(0,15,0,0)
                #                 v1 = v1 + 1
                # if v != 2:   
                #     if id == "Vetle":
                #         if v2 != 1:
                #             if w >= 175: 
                #                 drone.send_rc_control(0,-15,0, 0)  
                #                 v2 = v2 + 1 
                if v != 1:   
                    if id == "Vetle":
                        if v1 != 1:
                            # print("ID is 1", id)
                        
                            if w <= 140:
                                
                                print("w: ", w)
                                drone.move_forward(50)
                                time.sleep(4)
                                drone.move_back(100)
                                print("Under 140")
                                v1 = v1 + 1

                if v3 != 1:        
                    if id == "Vetle":
                        if v2 != 1:
                            
                            if w >= 175: 
                                print("w: ", w)
                                drone.move_back(100)
                                time.sleep(4)
                                drone.move_forward(150)
                                print("Over 175")
                                v2 = v2 + 1
                # if c != 1:    
                #     if id == "Christina":
                #         print("ID is 2", id)
                #         print("The drone rotates clockwise")
                #         drone.rotate_clockwise(360)
                #         c = c + 1

            confidence = "  {0}%".format(round(confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(
                    img, 
                    str(id), 
                    (x+5,y-5), 
                    font, 
                    1, 
                    (255,255,255), 
                    2
                   )
        cv2.putText(
                    img, 
                    str(confidence), 
                    (x+5,y+h-5), 
                    font, 
                    1, 
                    (255,255,0), 
                    1
                   )  
    
    # cv2.imshow('camera',img) 
    
    key = cv2.waitKey(1)    #dersom esc knappen trykkes, avsluttes programmet
    if key == 27:
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        drone.streamoff()  # Stop video stream
        drone.end() 
        drone.land()
        break
    
# print("\n [INFO] Exiting Program and cleanup stuff")
# cam.release()
# cv2.destroyAllWindows()

# drone.streamoff()  # Stop video stream
# drone.end() 