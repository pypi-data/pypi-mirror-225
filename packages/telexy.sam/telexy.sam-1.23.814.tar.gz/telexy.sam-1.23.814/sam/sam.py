from mars import *
import cherrypy
import os
import cv2

@cherrypy.tools.allow(methods=['POST'])
@cherrypy.tools.json_out()
class SamPlugin(MarsPluginBase):

    #sam model uid
    samModelUid = 'FBF5D932-4A68-4998-B1DF-48069A470B4E'
    #metadata file name
    metadataFileName = 'metadata'

    def __init__(self):
        """default constructor"""
        super().__init__("sam")
        # verify existance of any model and check for updated models
        self.syncModels()
   
    def syncModels(self):
        """Synchronize models"""
        # retrieve metadata file (if exists) and read out latest model version id
        ds = ModelApi()
        activeVersion = ds.activeVersion(self.samModelUid)
        print(activeVersion['Id'])

    def getFile(self, key):
        """retrieves file via key"""
        directory = self.getCurrentDirectory() + key
        return open(directory)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def predict(self):
        key = cherrypy.request.json
        filePath = self.getCurrentDirectory() + key
        if(os.path.exists(filePath) == False):
            print("need to download file here")
        
        image = cv2.imread(filePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return key

    def configuration(self):
        return {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }