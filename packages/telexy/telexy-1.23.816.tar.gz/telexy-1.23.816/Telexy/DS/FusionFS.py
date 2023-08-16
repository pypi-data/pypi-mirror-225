from Telexy.Fusion import REST
from Telexy.Fusion import FusionDS

class FusionFS(FusionDS.DSAccessBase):

    def __init__(self, baseUrl, key):
        """Default constructor"""
        super().__init__(baseUrl, key, 'e6161e69-5a7f-4e22-855b-cf5c974fe8d4')

    def browse(self, getContent, path, asBytes):
        """Gets fusion file system item via path"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('Browse'), {'includeContent': getContent, 'path': path, 'bytes': asBytes})
        return faReq.json()

    def save(self, model, getContent, asBytes):
        """Saves content item"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('Save'), {'includeContent': getContent, 'bytes': asBytes}, jsonParams=model)
        return faReq.json()

    def fileExists(self, path):
        """Call to determine if path exists"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('FileExists'), {'path': path, })
        return bool(faReq.json())

    def directoryExists(self, path):
        """call to determine if directory exists"""        
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('DirectoryExists'), {'path': path, })
        return bool(faReq.json())

    def delete(self, model):
        """Deletes file"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('Delete'), jsonParams=model)

    def create(self, model, getContent, asBytes):
        """Creates a file or folder"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl('Create'), {'includeContent': getContent, 'bytes': asBytes}, jsonParams=model)
        return faReq.json()

    def move(self, oldPath, newPath):
        """Moves and renames files and folders"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        fa.Post(self._dsControllerUrl('Move'), {'oldPath': oldPath, 'newPath': newPath })