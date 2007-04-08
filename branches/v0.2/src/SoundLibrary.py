import os
from numpy import *
from SoundEffects import *
from SoundControl import *

SOUND_LIB_DIR  = 'sound_library/'

class SoundLibrary:
    
    def __init__(self, env):
        self.env = env
        self.SFX = SoundEffects(env)
        self.loadLibrary(SOUND_LIB_DIR)

    '''
    ' Loads filenames of soundlibrary into matrix where different rows are 
    ' different categories and creates a list of category names.  Ignores
    ' the sound files of the category names.  The current sound and category
    ' are both set to -1 to flag that the user does not currently have a sound
    ' or category to select.
    '''   
    def loadLibrary(self, libraryDir):
        self.catList = os.listdir(libraryDir)
        self.catList.sort()
        if '.svn' in self.catList:
            self.catList.remove('.svn') # Ignore SVN files

        
        self.soundMatrix = [[] for i in xrange(len(self.catList)+1)]
        for i in xrange(len(self.catList)):
            soundList = os.listdir(SOUND_LIB_DIR + self.catList[i])
            soundList.sort()
            for sound in soundList:
                if sound != 'cat_name.mp3' and sound != '.svn': # Ignore category names and SVN files
                    self.soundMatrix[i] += [sound] 
        
        self.catList += ['Sound Manipulations']
        self.currCat = -1
        self.currSound = -1
        self.numCats = len(self.catList)
       
    def onValidCat(self):
        return self.currCat != -1
    
    def onValidSound(self):
        return self.currSound != -1
    
    '''
    ' Increments the current category in a circular fashion and returns new 
    ' category's name.
    '''
    def getNextCatName(self):
        self.currSound = -1
        self.currCat = (self.currCat + 1)%self.numCats
        return self.catList[self.currCat]
    
    '''
    ' Decrements the current category in a circular fashion and returns new
    ' category's name .  Ensures that the initial case is handled correctly.
    '''
    def getPrevCatName(self):
        self.currSound = -1
        if self.currCat == -1:
            self.currCat = self.numCats-1
        else:
            self.currCat = (self.currCat - 1)%self.numCats
        return self.catList[self.currCat]
        
    '''
    ' Increments the current sound in a circular fashion and returns the bytes
    ' of the new sound.
    '''    
    def getNextSoundBytes(self):
        if self.currCat < self.numCats-1:
            self.currSound = (self.currSound + 1)%len(self.soundMatrix[self.currCat])
            return self.getCurrSoundBytes()
        else:
            self.currSound = 0
            return self.SFX.getNextSFXClip()
        
    '''
    ' Decrements the current category in a circular fashion and returns the bytes
    ' of the new sound.  Ensures that the initial case is handled correctly.
    '''
    def getPrevSoundBytes(self):
        if self.currCat < self.numCats-1:
            if self.currSound == -1:
                self.currSound = len(self.soundMatrix[self.currCat])-1
            else:
                self.currSound = (self.currSound - 1)%len(self.soundMatrix[self.currCat])
            return self.getCurrSoundBytes()
        else:
            self.currSound = 0
            return self.SFX.getPrevSFXClip()
    
    '''
    ' Returns the bytes of the currently selected sound file.  Improper behavior if 
    ' current category or current sound are -1 (initial settings).
    '''
    def getCurrSoundBytes(self):
        if self.currCat < self.numCats-1:
            filePath = SOUND_LIB_DIR + self.catList[self.currCat] + '/' + self.soundMatrix[self.currCat][self.currSound]
            return soundFileToBytes(filePath)
        else:
            return self.SFX.getCurrSFXClip()