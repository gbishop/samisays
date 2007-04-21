import os
from numpy import *
from SoundEffects import *
from SoundControl import *
from Constants import *

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
        
        self.catList += ['Sound Manipulations', 'Trash Can']
        self.currCat = -1
        self.currSound = -1
        self.numCats = len(self.catList)
        self.sfxCat = self.numCats - 2
        self.trashCat = self.numCats - 1
        
    def onValidCat(self):
        return self.currCat != -1
    
    def onValidSound(self):
        return self.currSound != -1
    
    def getCurrCatName(self):
        return self.catList[self.currCat]
    
    '''
    ' Increments the current category in a circular fashion and returns new 
    ' category's name.
    '''
    def getNextCatName(self):
        self.currSound = -1
        self.currCat = (self.currCat + 1)%self.numCats
        self.currCatLen = self.getCatLen(self.currCat)
        if self.currCat == self.trashCat and not self.env['story'].hasTrash():
            return self.getNextCatName()
        return self.getCurrCatName()
    
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
        self.currCatLen = self.getCatLen(self.currCat)
        if self.currCat == self.trashCat and not self.env['story'].hasTrash():
            return self.getPrevCatName()
        return self.getCurrCatName()
        
    '''
    ' Increments the current sound in a circular fashion and returns the bytes
    ' of the new sound.
    '''    
    def getNextSoundBytes(self):
        if self.currCat < self.sfxCat:
            self.currSound = (self.currSound + 1)%self.currCatLen
        elif self.currCat == self.trashCat:
            self.currSound = 0
        elif self.currCat == self.sfxCat:
            self.currSound = 0
            self.SFX.getNextSFXClip()
        return self.getCurrSoundBytes()
        
    '''
    ' Decrements the current category in a circular fashion and returns the bytes
    ' of the new sound.  Ensures that the initial case is handled correctly.
    '''
    def getPrevSoundBytes(self):
        if self.currCat < self.sfxCat:
            if self.currSound == -1:
                self.currSound = self.currCatLen-1
            else:
                self.currSound = (self.currSound - 1)%self.currCatLen
        elif self.currCat == self.trashCat:
            self.currSound = 0
        elif self.currCat == self.sfxCat:
            self.currSound = 0
            self.SFX.getPrevSFXClip()
        return self.getCurrSoundBytes()
    '''
    ' Returns the bytes of the currently selected sound file.  Improper behavior if 
    ' current category or current sound are -1 (initial settings).
    '''
    def getCurrSoundBytes(self):
        if self.currCat < self.sfxCat:
            filePath = SOUND_LIB_DIR + self.catList[self.currCat] + '/' + self.soundMatrix[self.currCat][self.currSound]
            return soundFileToBytes(filePath)
        elif self.currCat == self.trashCat:
            return self.env['story'].lastDelete
        elif self.currCat == self.sfxCat:
            return self.SFX.getCurrSFXClip()
    
    def getCurrType(self):
        if self.currCat == self.sfxCat:
            return SFX
        else:
            return SND
        
    def getCatLen(self, cat):
        if self.currCat == self.sfxCat:
            return len(self.SFX.sfxFunctions)
        elif self.currCat == self.trashCat:
            return 1
        else:
            return len(self.soundMatrix[cat])

        
        