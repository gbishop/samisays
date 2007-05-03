import os
from numpy import *
from SoundEffects import *
from SoundControl import *
from Constants import *

class SoundLibrary:
    '''
    This class mirrors the structure of the Sound Library stored in the file system,
    providing support for the AuiInsertSound class during story creation.
    It keeps track of the different categories and the sounds within each category.
    The structure can be traversed easily with navigation methods.  A sound manipulation
    category is also supported through the SoundEffects class.  A trash can is supported
    through the Story class.
    '''
    
    def __init__(self, env):
        '''
        Constructor receives global objects.
        '''
        
        self.env = env

    
    def loadLibrary(self):
        ''' 
        Loads filenames of soundlibrary into matrix with rows as categories and 
        creates list of category names. The current sound and category are both set to 
        -1 to flag that the user does not currently have a sound or category to select.  Trash
        and SFX categories are added to the end of the category list.
        '''
        
        self.catList = os.listdir(SOUND_LIB_DIR)
        self.catList.sort()
        if '.svn' in self.catList:
            self.catList.remove('.svn') # Ignore SVN files
            
        # casing for prioritized sounds
        if 'assigned sounds' in self.catList:
            self.catList.remove('assigned sounds')
            self.catList = ['assigned sounds'] + self.catList

        
        self.soundMatrix = [[] for i in xrange(len(self.catList)+1)]
        for i in xrange(len(self.catList)):
            soundList = os.listdir(SOUND_LIB_DIR + self.catList[i])
            soundList.sort()
            for sound in soundList:
                sFormat = sound.split('.')[1]
                if sFormat.lower() in SOUND_FORMATS:
                    self.soundMatrix[i] += [sound]
             
        # Remove empty categories
        i = 0
        while True:
            if i == len(self.catList):
                break
            if len(self.soundMatrix[i]) == 0:
                del self.soundMatrix[i]
                del self.catList[i]
            else:
                i += 1
                        
        self.soundMatrix += [self.env['story'].getTrash()]
        self.catList += ['Trash Can', 'Sound Manipulations']
        self.currCat = -1
        self.currSound = -1
        self.numCats = len(self.catList)
        self.sfxCat = self.numCats - 1
        self.trashCat = self.numCats -2
        self.SFX = SoundEffects(self.env)
    

    def onValidCat(self):
        '''
        Returns true if user has moved off -1 category which is used for initial instructions.
        '''
        
        return self.currCat != -1
   
    def onValidSound(self):
        '''
        Returns true if user has moved off -1 sound which is used for initial instructions.
        '''
        
        return self.currSound != -1
        
    def getCurrCatName(self):
        '''
        Returns the text name of the current category from the list.
        '''
        
        if self.currCat != -1 :
            return self.catList[self.currCat]
        else:
            return ''
    
    def getNextCatName(self):
        '''
        Increments the current category in a circular fashion and returns new 
        category's name.  Skips Manipulations if clip is locked and skips Trash 
        if there is no trash.
        '''
        
        self.currSound = -1
        self.currCat = (self.currCat + 1)%self.numCats
        
        if (self.currCat == self.trashCat and not self.env['story'].hasTrash() or # skip empty trash
            self.currCat == self.sfxCat and self.env['story'].clipIsLocked()): # skip sfx if clip is locked
            return self.getNextCatName()
        elif self.currCat == self.trashCat:
            self.soundMatrix[self.trashCat] = self.env['story'].getTrash()
            
        self.currCatLen = self.getCatLen(self.currCat)
        return self.getCurrCatName()
    
  
    def getPrevCatName(self):
        '''
        Decrements the current category in a circular fashion and 
        returns new category's name.  Ensures that the initial
        instructions case is handled correctly. Skips Manipulations
        if clip is locked and skips Trash if there is no trash.
        '''
        
        self.currSound = -1
        
        if self.currCat == -1: # Handle initial case
            self.currCat = self.numCats-1
        else:
            self.currCat = (self.currCat - 1)%self.numCats
        
        if (self.currCat == self.trashCat and not self.env['story'].hasTrash() or # skip empty trash
            self.currCat == self.sfxCat and self.env['story'].clipIsLocked()): # skip sfx if clip is locked
            return self.getPrevCatName()
        elif self.currCat == self.trashCat:
            self.soundMatrix[self.trashCat] = self.env['story'].getTrash()
            
        self.currCatLen = self.getCatLen(self.currCat)
        return self.getCurrCatName()
         
           
    def getNextSoundBytes(self):
        '''
        Increments the current sound in a circular fashion and returns 
        the bytes of the new sound.
        '''
        
        if self.currCat != self.sfxCat:
            self.currSound = (self.currSound + 1)%self.currCatLen
        else:
            self.SFX.getNextSFXClip()
        return self.getCurrSoundBytes()
        
        
    def getPrevSoundBytes(self):
        '''
        Decrements the current sound in a circular fashion and returns 
        the bytes of the new sound.  Ensures that the initial instructions
        case is handled correctly.
        '''
        
        if self.currCat != self.sfxCat:
            if self.currSound == -1: # Handle inital case
                self.currSound = self.currCatLen-1
            else:
                self.currSound = (self.currSound - 1)%self.currCatLen
        else:
            self.SFX.getPrevSFXClip()
        return self.getCurrSoundBytes()
  
  
    def getCurrSoundBytes(self):
        '''
        Returns the bytes of the currently selected sound file.  Improper 
        behavior if current category or current sound are -1 (initial setting
        for each category).
        '''
        
        if self.currCat == self.trashCat:
            return self.soundMatrix[self.currCat][self.currSound]
        elif self.currCat == self.sfxCat:
            return self.SFX.getCurrSFXClip()
        else:
            catName = self.getCurrCatName()
            soundName = self.soundMatrix[self.currCat][self.currSound]
            filePath = '%s%s/%s' % (SOUND_LIB_DIR, catName, soundName)
            return soundFileToBytes(filePath)
       
    def getCurrType(self):
        '''
        Returns whether the current sound is a sound (SND) or a manipulation (SFX).
        '''
        
        if self.currCat == self.sfxCat:
            return SFX
        else:
            return SND
  
  
    def getCatLen(self, cat):
        '''
        Returns number of sounds (or sound manipulations) in the current category.
        '''
        
        if self.currCat == self.sfxCat:
            return len(self.SFX.sfxFunctions)
        else:
            return len(self.soundMatrix[cat])
 
 
    def getCurrSoundName(self):
        '''
        Returns the name of the sound file/manipulation/etc curently indexed.
        '''
        
        if self.currCat == self.trashCat:
            return 'Trash'
        elif self.currCat == self.sfxCat:
            return self.SFX.getCurrSFXName()
        elif self.currCat != -1 and self.currSound != -1:
            return self.soundMatrix[self.currCat][self.currSound]
        else:
            return ''

        
        