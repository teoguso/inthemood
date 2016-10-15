from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password, pipeline_id
from os import path
import time

def main():
    myhero = Heuro(email, password)
    #mypipe = myhero.make_pipeline(pipeline="test_pipe")
    #print(mypipe)
    upload = myhero.process_faces('../data/test_faces.jpg', pipeline_id)
    pipeline_key = upload['pipelinekey']
    #print(upload)
    results = myhero.get_results(pipeline_id, pipeline_key)
    while results.status_code == 202:
        time.sleep(5)
        results = myhero.get_results(pipeline_id, pipeline_key)
    print('Success')
    print(results.json())




if __name__ == "__main__":
    main()