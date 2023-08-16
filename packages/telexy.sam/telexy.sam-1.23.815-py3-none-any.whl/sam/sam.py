from mars import *
import cherrypy
import os
import cv2
from datetime import datetime
import threading

@cherrypy.tools.allow(methods=['POST'])
@cherrypy.tools.json_out()
class SamPlugin(MarsPluginBase):

    #sam model uid
    samModelUid = 'FBF5D932-4A68-4998-B1DF-48069A470B4E'
    samModelId = 0

    imageCacheDictionary = {}

    def __init__(self):
        """default constructor"""
        super().__init__("sam")
        # verify existance of any model and check for updated models
        self.modelSyncThread = Thread(target=self.syncModels)
        self.modelSyncThread.start()
        self.populateImagesFromDisk()
   
    def syncModels(self):
        """Synchronize models"""
        # retrieve metadata file (if exists) and read out latest model version id
        ds = ModelApi()
        # sam model active id 
        activeVersionId = int(ds.activeVersion(self.samModelUid)['Id'])
        # get resource lock
        lock = threading.Lock()
        lock.acquire()

        # check if there is a file starting with sam model uid
        # if there are and they are not of the version we want, delete them
        localVersion = self.samModelId
        for f in os.listdir(self.getHomeDirectory()):
            if f.startswith(self.samModelUid):
                localVersion = int(f.split('_')[1])
                if(localVersion != activeVersionId):
                    self.deleteFile(self.getModelPath(f))
                else:
                    self.samModelId = localVersion
                

        # if the active version is not the same as the one we have on disk
        if(activeVersionId != self.samModelId):
            # download file
            v = ds.getModelFile(activeVersionId)
            self.samModelId = activeVersionId
            f = open(self.getModelPath(self.samModelFileName()) , "wb")
            f.write(v)
            f.close()
        lock.release()

    def populateImagesFromDisk(self):
        """populates images into cache from disk"""
        files = os.listdir(self.getImagesFolder())
        now = datetime.utcnow()
        #notNow = datetime.utcnow()
        #(now - notNow).total_seconds()
        for f in files:
            self.imageCacheDictionary[f] = now

        # start the timer to manage files
        tenMins = 60 * 10
        self.cacheThread = marsthreading.RecursiveTimer(tenMins, self.cleanupImages)
        self.cacheThread.start()


    def cleanupImages(self):
        """Cleans up images on a timer"""
        lock = threading.Lock()
        lock.acquire()



        lock.release()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def predict(self):
        self.modelSyncThread.join()
        key = cherrypy.request.json
        filePath = self.getHomeDirectory() + key
        if(os.path.exists(filePath) == False):
            print("need to download file here")
        
        image = cv2.imread(filePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return key


    def getImagesFolder(self):
        """retrieves images folder"""
        imagesFolder = self.getHomeDirectory() + "/images"
        if(os.path.exists(imagesFolder) == False):
            os.makedirs(imagesFolder)
        return imagesFolder

    def getImagePath(self, key):
        """Gets image path"""
        return self.getImagesFolder() + "/" + key

    def imageExists(self, key):
        """reeturns if image exists"""
        return self.fileExists(self.getImagePath(key))
    
    def getModelPath(self, key):
        """gets file path"""
        return self.getHomeDirectory() + "/" + key

    def samModelFileName(self):
        """Gets sam model file name"""
        return self.samModelUid + "_" + str(self.samModelId)

    def getFile(self, path):
        """retrieves file via key"""
        return open(path)

    def fileExists(self, path):
        return os.path.exists(path)

    def deleteFile(self, path):
        #deletes file with given key
        if self.fileExists(path):
            os.remove(path)

    def close(self):
        """close threads when application is killed"""
        super().close()
        if self.cacheThread != None:
            self.cacheThread.cancel()

    def configuration(self):
        return {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }