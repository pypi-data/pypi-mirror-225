import os

class MarsPluginBase(object):

    def __init__(self, subdirectory):
        """constructor"""
        self.subdirectory = subdirectory.strip("/")

    def getHomeDirectory(self):
        """gets or creates current directory of this plugin"""
        currDir = os.path.dirname(__file__) + "/" + self.subdirectory
        if(os.path.exists(currDir) == False):
            os.makedirs(currDir)
        return os.path.dirname(__file__) + "/" + self.subdirectory


    def close(self):
        """track closure"""
        print("closing")

    def configuration(self):
        """get configuration"""
        return {}

