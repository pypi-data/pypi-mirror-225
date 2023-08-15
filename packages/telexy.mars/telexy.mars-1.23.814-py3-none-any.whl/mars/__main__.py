import cherrypy
from .registry import *
from .plugin import *

class Mars(object):

    def __init__(self, keys, values):
        for(key, value) in zip(keys, values):
            self.__dict__[key] = value

    @cherrypy.expose
    def index(self):
        return 'Mars is running!'

    
#fusePlugin = MARSApplicationRegistryPlugin("FuseApi", "Fuse", "Telexy.DS.Fuse")
#register(fusePlugin)

conf = {
    '/': {
    }
}

cherrypy.config.update({
    'server.socket_host' : '0.0.0.0',
    'server.socket_port' : 8080
})

#retrieve registered plug ins and instantiate them
regItems = getRegisteredPlugins()
paths = []
instances = []
for i in regItems:
    # get paths
    paths.append(i.applicationPath)
    # create instance
    inst = i.instantiate()
    # append instance
    instances.append(inst)
    # retrieve configurations
    conf['/' + i.applicationPath] = inst.configuration()

webapp = Mars(paths, instances)

cherrypy.quickstart(webapp, '/', conf)