from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password, pipeline_id
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
# from os import path
# import json
# import numpy as np
import time
import os


def analyse_file_api(file_to_ingest, target_api, pipeline_id):
    upload = target_api.ingest_file(file_to_ingest, pipeline_id)
    pipeline_key = upload['pipelinekey']
    tot_t = 0
    dt = 3
    results = target_api.get_results(pipeline_id, pipeline_key)
    while results.status_code == 202:
        time.sleep(dt)
        tot_t += dt
        results = target_api.get_results(pipeline_id, pipeline_key)
    print("Total time (secs):", tot_t)
    r = results.json()
    print("Status:", r['status'])
    return r

def detect_jpeg(file_to_ingest):
    is_jpeg = False
    if file_to_ingest[-3:] == "jpg" or \
                    file_to_ingest[-4:] == "jpeg":
        is_jpeg = True
    return is_jpeg


def main():
    myhero = Heuro(email, password)
    #mypipe = myhero.make_pipeline(pipeline="test_pipe")
    #print(mypipe)
    # upload = myhero.ingest_file('../data/images/test_faces_2.jpg', pipeline_id)
    """
    file_to_ingest = '../data/audio/man-woman.mp3'
    file_to_ingest = '../data/images/four-in-car.jpeg'
    file_to_ingest = '../data/images/family1.jpeg'
    """
    # Image first, just because
    image_to_ingest = '../data/images/two-in-car.jpg'
    if image_to_ingest[-3:] != "png" and \
                    image_to_ingest[-3:] != "jpg" and \
                    image_to_ingest[-4:] != "jpeg":
        sys.exit(" Sorry. Image file format is not recognized.")

    is_jpeg = detect_jpeg(image_to_ingest)
    r1 = analyse_file_api(image_to_ingest, target_api=myhero, pipeline_id=pipeline_id)

    # Audio second
    audio_to_ingest = '../data/audio/man-woman.mp3'
    if audio_to_ingest[-3:] != "mp3":
        sys.exit(" Sorry. Image file format is not recognized.")

    r2 = analyse_file_api(audio_to_ingest, target_api=myhero, pipeline_id=pipeline_id)

    # Distinguish between image and audio (different output formats)
    inference_audio = {}
    inference_image = {}

    r_video = r1['result']['output']['classification']
    # for x, y in zip(r_output.keys(), r_output.values()):
    #     print(str(x)+": "+str(np.array(y).shape)+str(y))
    people = r_video['objects']
    n_people = len(people)
    gender_image = []
    age_image = []
    face_xy = []
    for person in people:
        gender_image.append(person['gender'])
        age_image.append(person['ageGroup'])
        face_xy.append((person['face']['X'], person['face']['Y']))

    r_audio = r2['result']['output']
    # for x, y in zip(r_output.keys(), r_output.values()):
    #     print(str(x)+": "+str(y))
    gender_audio = r_audio['gender']
    age_audio = r_audio['age']
    language = r_audio['language']

    # if file_to_ingest[-3:] == "mp3":
        # with open('jsonwatch_audio.txt', 'w') as outf:
        #     json.dump(r, outf, sort_keys = True, indent = 4, separators=(',', ':'))
    # elif file_to_ingest[-3:] == "png" or\
    #                 file_to_ingest[-3:] == "jpg" or\
    #                 file_to_ingest[-4:] == "jpeg":
        # with open('jsonwatch_image.txt', 'w') as outf:
        #     json.dump(r, outf, sort_keys = True, indent = 4, separators=(',', ':'))

    print("=== Audio evaluation ===")
    print("gender_audio: ", gender_audio)
    print("age_audio: ", age_audio)
    print("language: ", language)

    print("=== Video evaluation ===")
    print("n_people: ", n_people)
    print("gender_image: ", gender_image)
    print("age_image: ",  age_image)
    print("faces: ",  face_xy)

    if is_jpeg:
        import Image
        im = Image.open(image_to_ingest)
        im.save('Foto.png')
        img = mpimage.imread('Foto.png')
    else:
        img = mpimage.imread(image_to_ingest)
    plt.imshow(img)

    for age, gend, face in zip(age_image, gender_image, face_xy):
        plt.text(face[0],face[1], str(age)+" "+str(gend), color='black', \
                 backgroundcolor='black', fontsize=24)
    plt.show()
    # Remove png file, only needed for visualization
    if is_jpeg:
        os.remove('Foto.png')




if __name__ == "__main__":
    main()