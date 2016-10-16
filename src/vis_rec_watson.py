from credentials import watson_visual_rec_key as key
from watson_developer_cloud import VisualRecognitionV3
from os import path
import json

vis_rec = VisualRecognitionV3('2016-10-16', api_key=key)

two_in_car = '../data/images/two-in-car.jpg'

with open(two_in_car, 'rb') as image:
    print json.dumps(
        vis_rec.detect_faces(images_file=image),
        indent=2
    )