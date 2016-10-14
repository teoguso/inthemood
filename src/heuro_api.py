import requests
import json

class Heuro(object):
    """Basic API wrapper"""
    def __init__(self, email, password):
        self.username = email
        self.password = password
        self.session = requests.Session()
        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
        self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))
        self.connectTimeout = 5
        self.readTimeout = 5
        self.headers = {'Content-Type': 'application/json'}
        self._get_key_id

    def _get_key_id(self):
        """
        Logs in and gets the key for the user
        """
        url = 'http://api.cognitio.heurolabs.com/v1/users/login'
        data = {'email': self.email, 'password': self.password}
        r = self.session.post(url, data=json.dumps(data), headers=self.headers).json()
        self.key = r['Key']
        self.id = r['id']

        



