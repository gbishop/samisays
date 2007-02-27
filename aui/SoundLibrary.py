import os

from numpy import *

soundLibraryDir = 'sound_library/'

class SoundLibrary:
    def __init__(self):
        self.catList = os.listdir(soundLibraryDir)
        self.catList.sort()
        self.catList.remove('.svn')
        
        self.soundMatrix = [[] for i in xrange(len(self.catList))]
        for i in xrange(len(self.catList)):
            soundList = os.listdir(soundLibraryDir + self.catList[i])
            soundList.sort()
            for sound in soundList:
                if sound != 'cat_name.wav' and sound != '.svn':
                    self.soundMatrix[i] += [sound] 
        
        self.currCat = -1
        self.currSound = -1
       
    def getNextCatNameFile(self):
        self.currSound = -1
        self.currCat = (self.currCat + 1)%len(self.catList)
        return soundLibraryDir + self.catList[self.currCat] + '/cat_name.wav'
        
    def getPrevCatNameFile(self):
        self.currSound = -1
        self.currCat = (self.currCat - 1)%len(self.catList)
        return soundLibraryDir + self.catList[self.currCat] + '/cat_name.wav'
        
    def getNextSoundFile(self):
        self.currSound = (self.currSound + 1)%len(self.soundMatrix[self.currCat])
        return self.getCurrSoundFile()
        
    def getPrevSoundFile(self):
        self.currSound = (self.currSound - 1)%len(self.soundMatrix[self.currCat])
        return self.getCurrSoundFile()
    
    def getCurrSoundFile(self):
       return soundLibraryDir + self.catList[self.currCat] + '/' + self.soundMatrix[self.currCat][self.currSound]