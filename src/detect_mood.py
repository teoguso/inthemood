from __future__ import print_function
from heuro_api import Heuro
from credentials import email, password
from os import path

def main():
    myhero = Heuro(email, password)
    #mypipe = myhero.make_pipeline(pipeline="test_pipe")
    #print(mypipe)
    upload = myhero.process_faces('../data/test_faces.jpg', 1707)
    pipeline_key = upload['pipelinekey']
    #print(upload)
    results = myhero.get_results(1707, pipeline_key)
    print(results)


if __name__ == "__main__":
    main()