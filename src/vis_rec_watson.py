from credentials import watson_visual_rec_key as key
from watson_developer_cloud import VisualRecognitionV3
from threading import Thread
from os import path
import json
import cv2

vis_rec = VisualRecognitionV3('2016-10-16', api_key=key)

two_in_car = '../data/images/two-in-car.jpg'
all_images = '../data/images/images.zip'

def detect_faces(image_path):
    with open(image_path, 'rb') as image:
        return json.dumps(
            vis_rec.detect_faces(images_file=image),
            indent=2
        )

def web_cam_detect():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False
    frame_count = 0
    while rval:
        frame_count +=1
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        if frame_count%100 == 0:
            cv2.imwrite('temp_image.jpg', frame)
            faces = detect_faces('temp_image.jpg')
            print faces
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")

print detect_faces(all_images)

