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
        # fetch a list of our existing pipelines to prevent us creating duplicates
        open_pipes = [pipe['name'] for pipe in self.get_pipeline()]
        if pipeline not in open_pipes:
            r = self.session.post(url, data=json.dumps(data), headers=headers)
            if r.status_code not in [200, 201]:
                return r.json()
            else:
                raise Exception('Error creating pipeline, response: {}'.format(r.status_code))
        else:
            raise Exception('Error creating pipeline, {} already exists'.format(pipeline))

    def get_pipeline(self, pipeline=None):
        """
        Fetches all pipelines available
        : inputs: a pipeline name as a string
        : side-effects: None
        : returns: returns a list of dicts of pipelines if pipeline is not specified
        """
        url = 'http://api.cognitio.heurolabs.com/v1/pipelines'
        headers = {'Content-Type': 'application/json',
                    'User': self.id,
                    'Key' : self.key
                }
        r = self.session.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Error with get_pipelines, response: {}'.format(r.status_code))

    def ingest_file(self, filename, pipe_id):
        url = 'http://api.cognitio.heurolabs.com/v1/pipelines/{}/ingestfile'.format(pipe_id)
        headers = { 'Key': self.key,
                }
        with open(filename, 'rb') as open_file:
            file = {'file': open_file}
            r = self.session.post(url, headers=headers, files=file)
            if r.status_code in [200, 201]:
                return r.json()
            else:
                raise Exception('Error ingesting file, response: {}'.format(r.status_code))

    def get_results(self, pipeline_key, pipeline_id):
        url = 'http://api.cognitio.heurolabs.com/v1/pipelines/{}/results/query'.format(pipeline_key)
        headers = {'Content-Type': 'application/json; charset=UTF-8',
                    'Key': self.key
                }
        data = {'pipelinekey': pipeline_id}
        r = self.session.post(url, data=json.dumps(data), headers=headers)#.json()
        return r
