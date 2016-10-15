from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password, pipeline_id
# from os import path
import json
import numpy as np
import time

def main():
    myhero = Heuro(email, password)
    #mypipe = myhero.make_pipeline(pipeline="test_pipe")
    #print(mypipe)
    # upload = myhero.ingest_file('../data/images/test_faces_2.jpg', pipeline_id)
    file_to_ingest = '../data/audio/man-woman.mp3'
    file_to_ingest = '../data/images/two-in-car.jpg'
    file_to_ingest = '../data/images/four-in-car.jpeg'
    file_to_ingest = '../data/images/family1.jpeg'
    upload = myhero.ingest_file(file_to_ingest, pipeline_id)
    pipeline_key = upload['pipelinekey']
    #print(upload)
    results = myhero.get_results(pipeline_id, pipeline_key)
    tot_t = 0
    while results.status_code == 202:
        time.sleep(5)
        tot_t += 5
        results = myhero.get_results(pipeline_id, pipeline_key)
    print(" Success!")
    print(" Total time (secs):", tot_t)
    r = results.json()
    print(" Status:", results.json()['status'])
    # Distinguish between image and audio (different output formats)
    inference_audio = {}
    inference_image = {}
    if file_to_ingest[-3:] == "mp3":
        # with open('jsonwatch_audio.txt', 'w') as outf:
        #     json.dump(r, outf, sort_keys = True, indent = 4, separators=(',', ':'))
        r_output = r['result']['output']
        # for x, y in zip(r_output.keys(), r_output.values()):
        #     print(str(x)+": "+str(y))
        gender_audio = r_output['gender']
        age_audio = r_output['age']
        language = r_output['language']
    elif file_to_ingest[-3:] == "jpg" or file_to_ingest[-4:] == "jpeg":
        # with open('jsonwatch_image.txt', 'w') as outf:
        #     json.dump(r, outf, sort_keys = True, indent = 4, separators=(',', ':'))
        r_output = r['result']['output']['classification']
        # for x, y in zip(r_output.keys(), r_output.values()):
        #     print(str(x)+": "+str(np.array(y).shape)+str(y))
        people = r_output['objects']
        n_people = len(people)
        gender_image = []
        age_image = []
        for person in people:
            gender_image.append(person['gender'])
            age_image.append(person['ageGroup'])

    # print(" gender_audio: ", gender_audio)
    # print(" age_audio: ", age_audio)
    print("n_people: ", n_people)
    print(" gender_image: ", gender_image)
    print(" age_image: ",  age_image)




if __name__ == "__main__":
    main()