from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password, pipeline_id
from os import path
import time

def main():
    myhero = Heuro(email, password)
    #mypipe = myhero.make_pipeline(pipeline="test_pipe")
    #print(mypipe)
    upload = myhero.ingest_file('../data/images/test_faces_2.jpg', pipeline_id)
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
    print(results.json())




if __name__ == "__main__":
    main()