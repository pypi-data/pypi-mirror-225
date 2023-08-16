import jsonpickle
import os
import importlib

class MarsApplicationRegistryPlugin(object):
    def __init__(self, name, appPath, nameSpace = None):
        """Application registration plugin"""
        self.name = name
        self.nameSpace = nameSpace
        self.applicationPath = appPath

    def instantiate(self):
        """Instantiate object of this name and namespace"""
        module = importlib.import_module(self.nameSpace)
        inst = getattr(module, self.name)
        return inst()

def register(registry):
    """register an application with MARS, presumably that registration is of type mentioned above"""
    regFileName = getRegistrationFileName()
    registryList = []
    if(os.path.exists(regFileName)):
        # here we want to open and deserialize existing registries
        file = open(regFileName, "r+")
        registryList = getRegisteredPlugins(file)
        file.seek(0)
    else:
        file = open(regFileName, "w+")

    # Find if item exists in registry
    exists = next((x for x in registryList if x.applicationPath == registry.applicationPath), None)
    if exists == None:
        registryList.append(registry)

    encoded = jsonpickle.encode(registryList)
    file.write(encoded)
    file.close()

def getRegisteredPlugins(file = None):
    """returns a list of registered plug ins"""
    if(file == None):
        regFileName = getRegistrationFileName()
        if(os.path.exists(regFileName)):
            file = open(regFileName, "r")
        else:
            return []

    return jsonpickle.decode(file.read())

def getRegistrationFileName():
    """Gets full file name for where to register"""
    return os.path.dirname(__file__) + "/registry"
