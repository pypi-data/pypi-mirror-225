import requests
from Telexy.Fusion import REST

class DSAccessBase(object):

    def __init__(self, baseUrl, key, dsUid):
        """default constructor"""
        super().__init__()
        self.__baseUrl = baseUrl
        self.__key = key
        self.__dsUid = dsUid

    def _getAccess(self):
        """Getter for access key"""
        return {"DS-ACCESS-KEY": self.__key}

    def _baseUrl(self):
        """Getter for base url"""
        return self.__baseUrl

    def _dsControllerUrl(self, functionName):
        """returns the url of the controller"""
        return '/FusionBusApi/' + self.__dsUid + '/' + functionName