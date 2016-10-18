from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password, pipeline_id
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
# from os import path
# import numpy as np
import time
import os
import sys


def analyse_file_api(files_to_ingest, target_api, pipeline_id):
    """
    Tries to mimic a socket ingesting files and requesting results
    in pseudo-parallel.
    :param files_to_ingest:
    :param target_api:
    :param pipeline_id:
    :return: a list of results for each ingestion
    """
    uploads = []
    pipe_keys = []
    for afile in files_to_ingest:
        print("Ingesting file {}...".format(afile))
        myup = target_api.ingest_file(afile, pipeline_id)
        uploads.append(myup)
        pipe_keys.append(myup['pipelinekey'])
    tot_t = 0
    dt = 3
    stats = [target_api.get_results(pipeline_id, key).status_code for key in pipe_keys]
    # while results.status_code == 202: target_api.get_results(pipeline_id, pipe_keys[0])
    # print(stats)
    while any([s == 202 for s in stats]):
        time.sleep(dt)
        tot_t += dt
        results = [target_api.get_results(pipeline_id, key) for key in pipe_keys]
        stats = [target_api.get_results(pipeline_id, key).status_code for key in pipe_keys]
        # for key in pipe_keys:
        #     results.append(target_api.get_results(pipeline_id, key))
    print("Total time (secs):", tot_t)
    r = [res.json() for res in results]
    # print("Status:", r['status'])
    return r

def detect_jpeg(file_to_ingest):
    is_jpeg = False
    if file_to_ingest[-3:] == "jpg" or \
                    file_to_ingest[-4:] == "jpeg":
        is_jpeg = True
    return is_jpeg


def main():
    myhero = Heuro(email, password)
    # Small dictionary to convert API output to a readable format
    mygender = {
        0: "female",
        1: "male"
    }
    #mypipe = myhero.make_pipeline(pipeline="test_pipe")
    #print(mypipe)
    # upload = myhero.ingest_file('../data/images/test_faces_2.jpg', pipeline_id)
    """
    file_to_ingest = '../data/audio/man-woman.mp3'
    file_to_ingest = '../data/images/four-in-car.jpeg'
    file_to_ingest = '../data/images/family1.jpeg'
    audio_to_ingest = '../data/audio/man-woman.mp3'
    audio_to_ingest = '../data/video/tagueule.mp3'
    image_to_ingest = '../data/video/tagueule.png'
    """


    # Image first, just because
    image_to_ingest = "../data/images/thb1.jpg"
    audio_to_ingest = "../data/audio/baby-talk.mp3"
    files_to_ingest = [image_to_ingest, audio_to_ingest]

    if image_to_ingest[-3:] != "png" and \
                    image_to_ingest[-3:] != "jpg" and \
                    image_to_ingest[-4:] != "jpeg" and \
            audio_to_ingest[-3:] != "mp3":
        sys.exit(" Sorry. File format is not recognized.")

    is_jpeg = detect_jpeg(image_to_ingest)
    results = analyse_file_api(files_to_ingest, target_api=myhero, pipeline_id=pipeline_id)
    # print(results)
    # r1 = analyse_file_api(image_to_ingest, target_api=myhero, pipeline_id=pipeline_id)
    r1 = results[0]
    watch_json = True
    if watch_json:
        import json
        with open('jsonwatch_image.txt', 'w') as outf:
            json.dump(r1, outf, sort_keys = True, indent = 4, separators=(',', ':'))

    # Audio second
    if audio_to_ingest[-3:] != "mp3":
        sys.exit(" Sorry. Image file format is not recognized.")

    # r2 = analyse_file_api(audio_to_ingest, target_api=myhero, pipeline_id=pipeline_id)
    r2 = results[1]

    # Distinguish between image and audio (different output formats)
    inference_audio = {}
    inference_image = {}

    r_video = r1['result']['output']['classification']
    # for x, y in zip(r_output.keys(), r_output.values()):
    #     print(str(x)+": "+str(np.array(y).shape)+str(y))
    people = r_video.get('objects')

    # Test if we got anything at all out
    if not people:
        sys.exit("Error: the API did not detect any people.")

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
        plt.text(face[0],face[1], str(age)+" "+str(mygender[gend]), color='black', \
                 fontsize=24) #, alpha=.8)
    plt.show()
    # Remove png file, only needed for visualization
    if is_jpeg:
        os.remove('Foto.png')




if __name__ == "__main__":
    main()