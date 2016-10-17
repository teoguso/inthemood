import requests
import json
from credentials import email, password

class Heuro(object):
    """Basic API wrapper"""
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
        self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))
        self.connectTimeout = 5
        self.readTimeout = 5
        self.headers = {'Content-Type': 'application/json'}
        self._get_key_id()

    def _get_key_id(self):
        """
        Logs in and gets the key for the user
        """
        url = 'http://api.cognitio.heurolabs.com/v1/users/login'
        data = {'email': self.email, 'password': self.password}
        r = self.session.post(url, data=json.dumps(data), headers=self.headers).json()
        # update the headers to contain our id and key for future requests
        # print r
        self.id, self.key = r['id'], r['Key']
        #self.headers.update(r)

    def make_pipeline(self, pipeline="default"):
        """
        : returns a dict contain all the info we need for the pipeline
        : example response
        :   {"id":30,"name":"examplePipline","user_id":542,"status":1,"sources":[]}

        """
        url = 'http://api.cognitio.heurolabs.com/v1/pipelines'
        data = {'name': pipeline}
        headers = {'Content-Type': 'application/json',
                    'User': self.id,
                    'Key' : self.key
                }
        r = self.session.post(url, data=json.dumps(data), headers=headers).json()
        return r

    def ingest_file(self, filename, pipe_id):
        url = 'http://api.cognitio.heurolabs.com/v1/pipelines/{}/ingestfile'.format(pipe_id)
        headers = { 'Key': self.key,
                }
        with open(filename, 'rb') as open_file:
            file = {'file': open_file}
            r = self.session.post(url, headers=headers, files=file).json()
            return r

    def get_results(self, pipeline_key, pipeline_id):
        url = 'http://api.cognitio.heurolabs.com/v1/pipelines/{}/results/query'.format(pipeline_key)
        headers = {'Content-Type': 'application/json; charset=UTF-8',
                    'Key': self.key
                }
        data = {'pipelinekey': pipeline_id}
        r = self.session.post(url, data=json.dumps(data), headers=headers)#.json()
        return r
