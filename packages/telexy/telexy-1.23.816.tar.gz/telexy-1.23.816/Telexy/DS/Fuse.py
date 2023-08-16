#import os
#import sys

#import current dir as directory for python to search modules
#CURR_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(CURR_DIR)

from Telexy.Fusion import REST
from Telexy.Fusion import FusionDS

class FuseApi(FusionDS.DSAccessBase):
    
    def __init__(self, baseUrl, key):
        """default contstuctor"""
        super().__init__(baseUrl, key, 'd17e86e7-0107-41f5-85a9-25555480e858')

    def FuseElements(self, typeUid):
        """Gets fuse elements"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        feReq = fa.Post(self._dsControllerUrl('FuseElements'), 
                        {'typeUid': typeUid})
        return feReq.json()

    def FuseTypes(self):
        """Gets fuse element types"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('FuseTypes'))
        return faReq.json()

    def CreateElement(self, typeUid, entityUid, entityId, context):
        """Create fuse element"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('CreateElement'),
                        jsonParams=
                            {'TypeUid' : typeUid,
                             'EntityUid': entityUid,
                             'EntityId': entityId,
                             'Context': context})
        return faReq.json()