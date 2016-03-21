import json
import requests

"""
This class was copied from https://github.com/SumoLogic/sumologic-python-sdk
It has a hack that bypasses the 401 session problem that you get if you try to call
the endpoint in a correct manner.
"""
class SumoLogic(object):

    def __init__(self, accessId, accessKey, endpoint=None):
        self.session = requests.Session()
        self.session.auth = (accessId, accessKey)
        self.session.headers = {'content-type': 'application/json', 'accept': 'application/json'}
        if endpoint is None:
            self.endpoint = self._get_endpoint()
        else:
            self.endpoint = endpoint

    def _get_endpoint(self):
        """
        When the default REST endpoint (https://api.sumologic.com/api/v1) is used the server
        responds with a 401 and causes the SumoLogic class instantiation to fail and this very
        unhelpful message is shown 'Full authentication is required to access this resource'

        This method makes a request to the default REST endpoint and resolves the 401 to learn
        the right endpoint
        """
        self.endpoint = 'https://api.sumologic.com/api/v1'
        self.response = self.session.get('https://api.sumologic.com/api/v1/collectors')  # Dummy call to get endpoint
        endpoint = self.response.url.replace('/collectors', '')  # dirty hack to sanitise URI and retain domain
        return endpoint

    def get(self, method, params=None):
        r = self.session.get(self.endpoint + method, params=params)
        r.raise_for_status()
        return r

    def collectors(self, limit=None, offset=None):
        params = {'limit': limit, 'offset': offset}
        r = self.get('/collectors', params)
        return json.loads(r.text)['collectors']
