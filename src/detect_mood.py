from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password, pipeline_id
from os import path
import time

def main():
    myhero = Heuro(email, password)
    #mypipe = myhero.make_pipeline(pipeline="test_pipe")
    #print(mypipe)
    # upload = myhero.ingest_file('../data/images/test_faces_2.jpg', pipeline_id)
    file_to_ingest = '../data/audio/man-woman.mp3'
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
    r_output = r['result']['output']
    for x, y in zip(r_output.keys(), r_output.values()):
        print(str(x)+": "+str(y))




if __name__ == "__main__":
    main()