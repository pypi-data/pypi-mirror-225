import cherrypy
import os

class MarsPluginBase(object):

    def __init__(self, subdirectory):
        """constructor"""
        self.subdirectory = subdirectory.strip("/")
        currDirectory = self.getCurrentDirectory()
        if(os.path.exists(currDirectory) == False):
            os.makedirs(currDirectory)


    def getCurrentDirectory(self):
        """gets current directory of this plugin"""
        return os.path.dirname(__file__) + self.subdirectory


    def configuration(self):
        """get configuration"""
        return {}

