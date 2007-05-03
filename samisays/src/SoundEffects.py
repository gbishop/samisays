from numpy import *
from Story import *
import time
from SoundControl import *
from Constants import *

class SoundEffects:
    
    def __init__(self,env):
        ''' Constructor '''
        self.env = env
    
        # Define array of functions for sound effects
        self.sfxFunctions = [SpeedUp, LargeSpeedUp, SlowDown, LargeSlowDown, ShortEcho, LongEcho, Reverse]
        self.sfxList = ["Speed Up", "Super Speed Up", "Slow Down", "Super Slow Down", "Short Echo", "Long Echo", "Reverse"]
        self.currSFX = -1
        self.currSFXClip = ''
        
    
    def getNextSFXClip(self):
        '''Increments the current sound effect in a circular fashion
        Calls the relevant sound effect function mapped in self.sfxFunctions array
        Returns modified soundclip for playback'''
        
        self.currSFX = (self.currSFX+1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        self.currSFXClip = self.sfxFunctions[self.currSFX](currClip)
        return self.getCurrSFXClip()
    
   
    def getPrevSFXClip(self):
        '''Decrements the current sound effect in a circular fashion
        Calls the relevant sound effect function mapped in self.sfxFunctions array
        Returns modified soundclip for playback'''
        
        if self.currSFX == -1:
            self.currSFX = len(self.sfxFunctions)-1
        else:
            self.currSFX = (self.currSFX-1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        self.currSFXClip = self.sfxFunctions[self.currSFX](currClip)
        return self.getCurrSFXClip()
    
    
    def getCurrSFXClip(self):
        '''Returns the current sound effect
        Calls the relevant sound effect function mapped in self.sfxFunctions array
        Returns modified soundclip and deletes the current one'''
        if self.currSFX != -1:
            return self.currSFXClip
    
       
    def getCurrSFXName(self):
        '''Returns the name of the currently selected sound effect'''
        if self.currSFX != -1:
            return self.sfxList[self.currSFX]
        else :
            return ''
    
    
def LongEcho(clip):
    ''' Adds a long echo to the clip'''
    return Echo(clip, delay = 5000)
    
def ShortEcho(clip):
    '''Adds a long echo to the clip'''
    return Echo(clip, delay = 1000)
        
    
def Echo(clip, delay, echoFactor = 0.5):
    '''Applies an echo to the soundclip.'''
    
    soundArray = concatenate((fromstring(clip, int16), zeros(delay, int16)))
    delayArray = array(soundArray[0:-delay]*echoFactor,int16)
    delayArray = concatenate((zeros(delay, int16), delayArray))
    soundArray += delayArray
    return soundArray.tostring()


def SpeedUp(clip):
    '''Resamples soundclip at a faster rate, speeding it up and raising pitch.'''
    newRate = int(RATE/1.5)
    return resampleSoundBytes(clip, newRate, CHANNELS)


def LargeSpeedUp(clip):
    '''Resamples soundclip at a faster rate, speeding it up and raising pitch.'''
    newRate = RATE/2
    return resampleSoundBytes(clip, newRate, CHANNELS)
   

def SlowDown(clip):
    '''Resamples soundclip at a slower rate, slowing it down and lowering pitch.'''
    newRate = int(RATE*1.5)
    return resampleSoundBytes(clip, newRate, CHANNELS)


def LargeSlowDown(clip):
    '''Resamples soundclip at a slower rate, slowing it down and lowering pitch.'''
    newRate = RATE*2
    return resampleSoundBytes(clip, newRate, CHANNELS)

def Reverse(clip):
    '''Reverses a soundclip'''
    soundArray = fromstring(clip, int16)
    return soundArray[::-1].tostring()
    return newclip.tostring()
    
    
    
     
       