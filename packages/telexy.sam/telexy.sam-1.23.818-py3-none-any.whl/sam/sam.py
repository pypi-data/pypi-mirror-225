from mars import *
import cherrypy
import os
import cv2
from datetime import datetime
import threading
from Telexy.DS import VirtualFileAccessor
import torch
import numpy as np
import torchvision.transforms as transforms
from segment_anything import sam_model_registry, SamPredictor

from torchvision.ops import masks_to_boxes


@cherrypy.tools.allow(methods=['POST'])
@cherrypy.tools.json_out()
class SamPlugin(MarsPluginBase):

    #sam model uid
    samModelUid = 'FBF5D932-4A68-4998-B1DF-48069A470B4E'
    samModelId = 0

    # keeps track of cached images
    imageCacheDictionary = {}
    # keeps track of tracked image predictors
    predictorCacheDictionary = {}

    device = "cpu"
    sam = None

    def __init__(self):
        """default constructor"""
        super().__init__("sam")
        if torch.cuda.is_available():
            device = "cuda"

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

        try:
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

            self.sam = sam_model_registry["vit_h"](self.getModelPath(self.samModelFileName()))
            self.sam.to(device = self.device)
        except:
            print("Error occurred")
        finally:
            lock.release()

    def populateImagesFromDisk(self):
        """populates images into cache from disk"""
        files = os.listdir(self.getImagesFolder())
        now = datetime.utcnow()
        #notNow = datetime.utcnow()
        #(now - notNow).total_seconds()
        lock = threading.Lock()
        lock.acquire()
        for f in files:
            self.imageCacheDictionary[f] = now

        lock.release()
        # start the timer to manage files
        tenMins = 60 * 10
        self.cacheThread = marsthreading.RecursiveTimer(tenMins, self.cleanupImages)
        self.cacheThread.start()


    def cleanupImages(self):
        """Cleans up images on a timer"""
        lock = threading.Lock()
        lock.acquire()
        fiveMins = 60*5
        now = datetime.utcnow()
        toDelete = []
        for k in self.imageCacheDictionary.keys():
            diff = (now - self.imageCacheDictionary[k]).total_seconds()
            if(diff > fiveMins):
                # delete file and delete record
                self.deleteFile(self.getImagePath(k))
                toDelete.append(k)
                
        for k in toDelete:
            print(k)
            self.imageCacheDictionary.pop(k)
            if self.predictorCacheDictionary.get(k) != None:
                self.predictorCacheDictionary.pop(k)

        lock.release()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def predict(self):
        self.modelSyncThread.join()
        inferenceData = cherrypy.request.json

        predictor = self.getImagePredictor(inferenceData['Key'])
        masks, scores, logits = predictor.predict(point_coords=np.array([[inferenceData['Coordinate']['x'], inferenceData['Coordinate']['y']]]),
                                                  point_labels=np.array([1]), 
                                                  multimask_output=True)

        rv = []
        for mask in masks:
            # format masks and make them a coordinate system
            h,w = mask.shape[-2:]
            mask_image = mask.reshape(h, w, 1)
            m = []

            for y in range(h):
                mi = mask_image[y]
                for x in range(w):
                    if mi[x][0] == True:
                        m.append({'x': x, 'y': y})
            rv.append(m)

        return rv


    def getImagePredictor(self, key):
        """retrieves image predictor"""
        lock = threading.Lock()
        lock.acquire()
        predictor = self.predictorCacheDictionary.get(key)
        if(predictor == None):
            predictor = SamPredictor(self.sam)
            predictor.set_image(self.getImage(key))
            self.predictorCacheDictionary[key] = predictor
        lock.release()
        return predictor

    def getImage(self, key):
        """Retrieves image"""
        imgPath = self.getImagePath(key) 
        if(self.imageExists(key) == False):
            faApi = VirtualFileAccessor.VirtualFileAccessApi()
            file = faApi.getFile(key)
            f = open(imgPath, "wb")
            f.write(file)
            f.close()

        # update or create cache record
        lock = threading.Lock()
        lock.acquire()
        self.imageCacheDictionary[key] = datetime.utcnow()
        lock.release()

        return cv2.cvtColor(cv2.imread(imgPath), cv2.COLOR_BGR2RGB)


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