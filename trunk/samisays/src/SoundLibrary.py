import os
from numpy import *
from SoundEffects import *
from SoundControl import *
from Constants import *

class SoundLibrary:
    
    def __init__(self, env):
        self.env = env

    '''
    ' loadLibrary - Loads filenames of soundlibrary into matrix with rows as
    '               categories and creates list of category names.  The current 
    '                sound and category are both set to -1 to flag that the user 
    '                does not currently have a sound or category to select.  Trash
    '                and SFX categories are added to the end of the category list.
    '''   
    def loadLibrary(self):
        self.catList = os.listdir(SOUND_LIB_DIR)
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
        
        self.soundMatrix += [self.env['story'].getTrash()]
        self.catList += ['Trash Can', 'Sound Manipulations']
        self.currCat = -1
        self.currSound = -1
        self.numCats = len(self.catList)
        self.sfxCat = self.numCats - 1
        self.trashCat = self.numCats -2
        self.SFX = SoundEffects(self.env)
    
    '''
    ' onValidCat - Returns true if user has moved off -1 category which is used
    '              for initial instructions.
    '''    
    def onValidCat(self):
        return self.currCat != -1

    '''
    ' onValidCat - Returns true if user has moved off -1 sound which is used
    '              for initial instructions.
    '''     
    def onValidSound(self):
        return self.currSound != -1
    
    '''
    ' onValidCat - Returns the text name of the current category from the list.
    '''    
    def getCurrCatName(self):
        if self.currCat != -1 :
            return self.catList[self.currCat]
        else:
            return ''
    
    '''
    ' getNextCatName - Increments the current category in a circular fashion and
    '                  returns new category's name.  Skips Manipulations if clip
    '                  is locked and skips Trash if there is no trash.
    '''
    def getNextCatName(self):
        self.currSound = -1
        self.currCat = (self.currCat + 1)%self.numCats
        if (self.currCat == self.trashCat and not self.env['story'].hasTrash() or
            self.currCat == self.sfxCat and self.env['story'].clipIsLocked()):
            return self.getNextCatName()
        elif self.currCat == self.trashCat:
            self.soundMatrix[self.trashCat] = self.env['story'].getTrash()
            
        self.currCatLen = self.getCatLen(self.currCat)
        return self.getCurrCatName()
    
    
    '''
    ' getPrevCatName - Decrements the current category in a circular fashion and 
    '                  returns new category's name.  Ensures that the initial
    '                  instructions case is handled correctly. Skips Manipulations
    '                  if clip is locked and skips Trash if there is no trash.
    '''
    def getPrevCatName(self):
        self.currSound = -1
        if self.currCat == -1:
            self.currCat = self.numCats-1
        else:
            self.currCat = (self.currCat - 1)%self.numCats
        if (self.currCat == self.trashCat and not self.env['story'].hasTrash() or
            self.currCat == self.sfxCat and self.env['story'].clipIsLocked()):
            return self.getPrevCatName()
        elif self.currCat == self.trashCat:
            self.soundMatrix[self.trashCat] = self.env['story'].getTrash()
            
        self.currCatLen = self.getCatLen(self.currCat)
        return self.getCurrCatName()
        
    '''
    ' getNextSoundBytes - Increments the current sound in a circular fashion and returns 
    '                     the bytes of the new sound.
    '''    
    def getNextSoundBytes(self):
        if self.currCat != self.sfxCat:
            self.currSound = (self.currSound + 1)%self.currCatLen
        else:
            self.SFX.getNextSFXClip()
        return self.getCurrSoundBytes()
        
    '''
    ' getPrevSoundBytes - Decrements the current sound in a circular fashion and returns 
    '                     the bytes of the new sound.  Ensures that the initial instructions
    '                     case is handled correctly.
    '''
    def getPrevSoundBytes(self):
        if self.currCat != self.sfxCat:
            if self.currSound == -1:
                self.currSound = self.currCatLen-1
            else:
                self.currSound = (self.currSound - 1)%self.currCatLen
        else:
            self.SFX.getPrevSFXClip()
        return self.getCurrSoundBytes()
    '''
    ' getCurrSoundBytes - Returns the bytes of the currently selected sound file.  Improper 
    '                     behavior if current category or current sound are -1 (initial settings)
    '''
    def getCurrSoundBytes(self):
        if self.currCat == self.trashCat:
            return self.soundMatrix[self.currCat][self.currSound]
        elif self.currCat == self.sfxCat:
            return self.SFX.getCurrSFXClip()
        else:
            catName = self.getCurrCatName()
            soundName = self.soundMatrix[self.currCat][self.currSound]
            filePath = '%s%s/%s' % (SOUND_LIB_DIR, catName, soundName)
            return soundFileToBytes(filePath)
       
    '''
    ' getCurrType - Returns whether the current sound is a sound (SND) or a manipulation.
    '''
    def getCurrType(self):
        if self.currCat == self.sfxCat:
            return SFX
        else:
            return SND
    '''
    ' getCatLen - Returns number of sounds (or sound manipulations) in the current category.
    '''
    def getCatLen(self, cat):
        if self.currCat == self.sfxCat:
            return len(self.SFX.sfxFunctions)
        else:
            return len(self.soundMatrix[cat])
    '''
    ' getSoundName - Returns the name of the sound file/manipulation/etc you're currently on
    '''
    def getCurrSoundName(self):
        if self.currCat == self.trashCat:
            return 'Trash'
        elif self.currCat == self.sfxCat:
            return self.SFX.getCurrSFXName()
        elif self.currCat != -1 and self.currSound != -1:
            return self.soundMatrix[self.currCat][self.currSound]
        else:
            return ''

        
        