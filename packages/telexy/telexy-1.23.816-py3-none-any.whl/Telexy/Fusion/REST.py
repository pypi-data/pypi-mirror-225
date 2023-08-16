import requests
#import os
#import sys

#import current dir as directory for python to search modules
#CURR_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(CURR_DIR)

#api client class
class ApiClient(object):
    
    """Default constructor"""
    def __init__(self, baseUrl, headers = {}):
        super().__init__()
        if baseUrl.endswith('/') == False:
            baseUrl += '/'

        self.baseUrl = baseUrl
        self.headers = headers
        
    """Post api method"""    
    def Post(self, method, urlParams={}, bodyParams={}, jsonParams={}):
        req = requests.post(self.baseUrl + method, headers=self.headers, params=urlParams, data=bodyParams, json=jsonParams)
        if(req.ok == False):
            raise Exception(req.text)
        return req
        