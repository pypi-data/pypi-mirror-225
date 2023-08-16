from datetime import datetime
from ..DS.FusionFS import FusionFS
import os
from ..Constants import *
from notebook.services.contents.manager import ContentsManager
from notebook.services.contents.filecheckpoints import GenericCheckpointsMixin, Checkpoints
from traitlets import Any, Unicode, Bool, TraitError, observe, default, validate

class TelexyCMCheckpoints(GenericCheckpointsMixin, Checkpoints):

    JupyterFusionFileSetDS = 'JUPYTER_FUSION_FS_DS'

    """requires the following methods:"""
    def create_file_checkpoint(self, content, format, path):
        """ -> checkpoint model"""
        """Create a checkpoint from the current content of a file."""
        path = path.strip('/')
        # only the one checkpoint ID:
        checkpoint_id = u"checkpoint"

        return dict(
            id=checkpoint_id,
            last_modified=datetime.utcnow(),
            format=format,
            path=path
        )

    def create_notebook_checkpoint(self, nb, path):
        """ -> checkpoint model"""

    def get_file_checkpoint(self, checkpoint_id, path):
        """ -> {'type': 'file', 'content': <str>, 'format': {'text', 'base64'}}"""

    def get_notebook_checkpoint(self, checkpoint_id, path):
        """ -> {'type': 'notebook', 'content': <output of nbformat.read>}"""

    def delete_checkpoint(self, checkpoint_id, path):
        """deletes a checkpoint for a file"""

    def list_checkpoints(self, path):
        """returns a list of checkpoint models for a given file,
        default just does one per file
        """
        return []
    def rename_checkpoint(self, checkpoint_id, old_path, new_path):
        """renames checkpoint from old path to new path"""

class TelexyContentManager(ContentsManager):
    """Telexy content manager for jupyter"""

    @default('checkpoints_class')
    def _checkpoints_class_default(self):
        return TelexyCMCheckpoints

    def dir_exists(self, path):
        """Does a directory exist at the given path?

        Like os.path.isdir

        Override this method in subclasses.

        Parameters
        ----------
        path : string
            The path to check

        Returns
        -------
        exists : bool
            Whether the path does indeed exist.
        """
        fs = self._get_fs()
        exists = fs.directoryExists(self.__verify_path(path))
        return exists

    def is_hidden(self, path):
        """Is path a hidden directory or file?

        Parameters
        ----------
        path : string
            The path to check. This is an API path (`/` separated,
            relative to root dir).

        Returns
        -------
        hidden : bool
            Whether the path is hidden.

        """
        return False

    def file_exists(self, path=''):
        """Does a file exist at the given path?

        Like os.path.isfile

        Override this method in subclasses.

        Parameters
        ----------
        path : string
            The API path of a file to check for.

        Returns
        -------
        exists : bool
            Whether the file exists.
        """
        fs = self._get_fs()
        exists = fs.fileExists(self.__verify_path(path))
        return exists

    """Dictionary to store Fusion Ids of file"""
    __fusionFileIdDictionary = {}

    def __dict_key_exists(self, path):
        """Determine if path key exists in the private file id dictionary"""
        return self.__verify_path(path) in self.__fusionFileIdDictionary


    def __convert_to_saving_model(self, model, path):
        """converts jupyter model to model trying to save"""
        p = self.__verify_path(path)
        retModel = {
            "Id": 0,
            "Path": p
        }
        if 'content' in model:
            retModel['StringContent'] = model['content']

        if self.__dict_key_exists(path):
            retModel['Id'] = self.__fusionFileIdDictionary[self.__verify_path(path)]

        if 'type' in model:
            retModel['IsFolder'] = model['type'] == 'directory'

        return retModel

    def _base_model(self, data):
        """Returns base model that works for all"""
        path = self.__verify_path(data['Path'])
        if path not in self.__fusionFileIdDictionary:
            self.__fusionFileIdDictionary[path]=data['Id']

        return {
            'Id': data['Id'],
            'name': data['Name'],
            'path': path,
            'last_modified': data['CreatedString'],
            'created': data['CreatedString'],
            'writable': True,
            'content': None,
            'format': None,
            'mimetype': None
        }
        
    def _file_model(self, data, content=True):
        """Model if this is a file"""
        model = self._base_model(data)
        model['type'] = 'file'
        model['mimetype'] = 'text/plain'
        if content:
            model['format'] = 'text'
            model['content'] = data["StringContent"]
        return model

    def _dir_model(self, data, content=True):
        """Model if this is a directory"""
        model = self._base_model(data)
        model['type'] = 'directory'
        if(content):
            model['format'] = 'json'
            model['content'] = contents = []
            for c in data['Children']:
                if c['IsFolder']:
                    contents.append(self._dir_model(c, False))
                else:
                    contents.append(self._file_model(c, False))
        
        return model

    def _get_fs(self):
        """Gets fusion fs instance with credentials"""
        
        url=os.getenv(FusionAppUrl)
        if url is None:
            raise Exception(FusionAppUrl + ' environment variable is not specified')

        key = os.getenv(self.JupyterFusionFileSetDS)
        if key is None:
            raise Exception(self.JupyterFusionFileSetDS + ' environment variable is not specified')

        return FusionFS(url, key)

    def __verify_path(self, path):
        """standardizes path, seems to be a jupyter inconsistency sometimes having a / at first and sometimes not"""
        if len(path) > 0 and path[0] != '/':
            return '/' + path
        return path

    def get(self, path, content=True, type=None, format=None):
        """Get a file or directory model."""
        #clear the file id dictionary
        self.__fusionFileIdDictionary = {}
        path = self.__verify_path(path)
        #TEMP
        fs = self._get_fs()
        #temp
        data = fs.browse(bool(content), path, False)
        if data["IsFolder"]:
            return self._dir_model(data, bool(content))
        return self._file_model(data, bool(content))

    def save(self, model, path):
        """
        Save a file or directory model to path.
        Should return the saved model with no content.  Save implementations
        should call self.run_pre_save_hook(model=model, path=path) prior to
        writing any data.
        """
        self.run_pre_save_hook(model, path)
        fs = self._get_fs()

        # must find out what kind of save this is
        # if this is create, call create
        itemExists = self.__dict_key_exists(path)
        savingModel = self.__convert_to_saving_model(model, path)
        if itemExists:
            model = fs.save(savingModel, False, False)
        else:
            # create a new file
            model = fs.create(savingModel, False, False)
            
        if model["IsFolder"]:
            return self._dir_model(model, False)
        return self._file_model(model, False)

    def delete_file(self, path):
        """Delete the file or directory at path."""
        fileId = {
            "Id": self.__fusionFileIdDictionary[self.__verify_path(path)],
        }
        fs = self._get_fs()
        fs.delete(fileId)

    def rename_file(self, old_path, new_path):
        """Rename a file or directory."""
        fs = self._get_fs()
        fs.move(self.__verify_path(old_path), self.__verify_path(new_path))
