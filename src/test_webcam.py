import cv2
from credentials import email, password, pipeline_id
from heuro_api import Heuro
myhero = Heuro(email, password)

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
frame_count = 0
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    frame_count +=1
    if frame_count%30 ==
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")
print frame_count