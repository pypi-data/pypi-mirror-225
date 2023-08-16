from Telexy.Fusion import REST
from Telexy.Fusion import FusionDS
from Telexy.Constants import *
import os

"""Model api class to interface with model related data sources"""
class ModelApi(FusionDS.DSAccessBase):

    ModelDSKey = 'ML_MODEL_DS_KEY'

    def __init__(self):
        """default constructor"""
        url = os.getenv(FusionAppUrl)
        if url is None:
            raise Exception(FusionAppUrl + ' environment variable is not specified')
        
        key = os.getenv(self.ModelDSKey)
        if key is None:
            raise Exception(self.ModelDSKey + " environment variable is not specified")

        super().__init__(url, key, 'E02903C6-A9E5-4E15-8886-CDD8C19E891A')

    def modelTypes(self):
        """retrieves model types"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl("ModelTypes"))
        return faReq.json()
    
    def activeVersion(self, modelTypeUid):
        """Gets model active version"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl("ActiveVersion"), {"modelTypeUid": modelTypeUid})
        return faReq.json()
    
    def getModelFile(self, versionId):
        """gets model file for active version"""
        fa = REST.ApiClient(self._baseUrl(), self._getAccess())
        faReq = fa.Post(self._dsControllerUrl("GetModelFile"), {"versionId": versionId})
        return faReq.content