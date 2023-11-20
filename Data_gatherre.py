import cv2
import os
from djitellopy import Tello

tello = Tello()
tello.connect()

face_id = input('\n enter user id end press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")# Initialize individual sampling face count

tello.streamon()
cam = cv2.VideoCapture('udp://@0.0.0.0:11111')
# cam = cv2.VideoCapture(0)

width = 640
height = 480
cam.set(3, width)
cam.set(4, height)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")# For each person, enter one numeric face id

count = 0

directory = "/Users/vetlesjaberg/Documents/Minverden/Universitet/Elektronikkingeniør/5semester/ELVE3610/Prosjekt/Python/Mains/ProsjektH/Robotikk/dataset"
  
os.chdir(directory)

while(True):
    ret, img = cam.read()
     # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("/Users/vetlesjaberg/Documents/Minverden/Universitet/Elektronikkingeniør/5semester/ELVE3610/Prosjekt/Python/Mains/ProsjektH/Robotikk/dataset/User"+"." + str(face_id) + '.' +  
                    str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break # Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
tello.streamoff()  # Stop video stream
tello.end() 