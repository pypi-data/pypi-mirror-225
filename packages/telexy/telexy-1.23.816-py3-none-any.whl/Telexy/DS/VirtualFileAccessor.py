from Telexy.Fusion import REST
from Telexy.Fusion import FusionDS
import os
from ..Constants import *

# class for virtual file access
class VirtualFileAccessApi(FusionDS.DSAccessBase):

    VFAKey = 'VFA_DS_KEY'

    def __init__(self):
        """Default constructor"""
        url = os.getenv(FusionAppUrl)
        if url is None:
            raise Exception(FusionAppUrl + ' environment variable is not specified')
        
        key = os.getenv(self.VFAKey)
        if key is None:
            raise Exception(self.VFAKey + ' environment variable is not specified')

        super().__init__(url, key, 'EB2F60F7-34FC-495E-B112-A3B18C49A4F3')

    def virtualFileAccessors(self):
        """Gets a list of virtual file accessors"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl("VirtualFileAccessors"))
        return faReq.json()
    
    def getFile(self, key):
        """Gets file by key"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl("GetFile"), {"key": key})
        return faReq.content
