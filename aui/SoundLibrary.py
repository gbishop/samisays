import os
from numpy import *

SOUND_LIB_DIR  = 'sound_library/'

class SoundLibrary:
    
    def __init__(self):
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
        self.catList.remove('.svn') # Ignore SVN files
        
        self.soundMatrix = [[] for i in xrange(len(self.catList))]
        for i in xrange(len(self.catList)):
            soundList = os.listdir(SOUND_LIB_DIR + self.catList[i])
            soundList.sort()
            for sound in soundList:
                if sound != 'cat_name.mp3' and sound != '.svn': # Ignore category names and SVN files
                    self.soundMatrix[i] += [sound] 
        
        self.currCat = -1
        self.currSound = -1
       
    def onValidCat(self):
        return self.currCat != -1
    
    def onValidSound(self):
        return self.currSound != -1
    
    '''
    ' Increments the current category in a circular fashion and returns a path
    ' to the new category's name sound file.
    '''
    def getNextCatNameFile(self):
        self.currSound = -1
        self.currCat = (self.currCat + 1)%len(self.catList)
        return SOUND_LIB_DIR + self.catList[self.currCat] + '/cat_name.mp3'
    
    '''
    ' Decrements the current category in a circular fashion and returns a path
    ' to the new category's name sound file.  Ensures that the initial case
    ' is handled correctly.
    '''
    def getPrevCatNameFile(self):
        self.currSound = -1
        if self.currCat == -1:
            self.currCat = len(self.catList)-1
        else:
            self.currCat = (self.currCat - 1)%len(self.catList)
        return SOUND_LIB_DIR + self.catList[self.currCat] + '/cat_name.mp3'
    
    '''
    ' Increments the current sound in a circular fashion and returns a path
    ' to the new sound.
    '''    
    def getNextSoundFile(self):
        self.currSound = (self.currSound + 1)%len(self.soundMatrix[self.currCat])
        return self.getCurrSoundFile()
        
    '''
    ' Decrements the current category in a circular fashion and returns a path
    ' to the new sound.  Ensures that the initial case is handled correctly.
    '''
    def getPrevSoundFile(self):
        if self.currSound == -1:
            self.currSound = len(self.soundMatrix[self.currCat])-1
        else:
            self.currSound = (self.currSound - 1)%len(self.soundMatrix[self.currCat])
        return self.getCurrSoundFile()
    
    '''
    ' Returns a path to the currently selected sound file.  Improper behavior if 
    ' current category or current sound are -1 (initial settings).
    '''
    def getCurrSoundFile(self):
       return SOUND_LIB_DIR + self.catList[self.currCat] + '/' + self.soundMatrix[self.currCat][self.currSound]