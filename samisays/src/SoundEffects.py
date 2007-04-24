from numpy import *
from Story import *
import time
from SoundControl import *
from Constants import *

class SoundEffects:
    
    def __init__(self,env):
        self.env = env
    
        # Define array of functions for sound effects
        self.sfxFunctions = [SpeedUp, LargeSpeedUp, SlowDown, LargeSlowDown, ShortEcho, LongEcho, Reverse]
        self.sfxList = ["Speed Up", "Super Speed Up", "Slow Down", "Super Slow Down", "Short Echo", "Long Echo", "Reverse"]
        self.currSFX = -1
        self.currSFXClip = ''
        
    '''
    ' Increments the current sound effect in a circular fashion
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified soundclip for playback
    '''
    def getNextSFXClip(self):
        self.currSFX = (self.currSFX+1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        self.currSFXClip = self.sfxFunctions[self.currSFX](currClip)
        return self.getCurrSFXClip()
    
    '''
    ' Decrements the current sound effect in a circular fashion
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified soundclip for playback
    '''
    def getPrevSFXClip(self):
        if self.currSFX == -1:
            self.currSFX = len(self.sfxFunctions)-1
        else:
            self.currSFX = (self.currSFX-1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        self.currSFXClip = self.sfxFunctions[self.currSFX](currClip)
        return self.getCurrSFXClip()
    
    '''
    ' Returns the current sound effect
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified soundclip and deletes the current one
    '''
    def getCurrSFXClip(self):
        if self.currSFX != -1:
            return self.currSFXClip
    '''
    ' getCurrSFXName - returns the name of the currently selected sound effect
    '''    
    def getCurrSFXName(self):
        if self.currSFX != -1:
            return self.sfxList[self.currSFX]
        else :
            return ''
    
    
def LongEcho(clip):
        return Echo(clip, delay = 5000)
    
def ShortEcho(clip):
        return Echo(clip, delay = 1000)
        
    
'''
' Applies an echo to the soundclip.
'''
def Echo(clip, delay, echoFactor = 0.5):
    
    soundArray = concatenate((fromstring(clip, int16), zeros(delay, int16)))
    delayArray = array(soundArray[0:-delay]*echoFactor,int16)
    delayArray = concatenate((zeros(delay, int16), delayArray))
    soundArray += delayArray
    return soundArray.tostring()

'''
' Resamples soundclip at a faster rate, speeding it up and raising pitch.
'''
def SpeedUp(clip):
    newRate = int(RATE/1.5)
    return resampleSoundBytes(clip, newRate, CHANNELS)

'''
' Resamples soundclip at a faster rate, speeding it up and raising pitch.
'''
def LargeSpeedUp(clip):
    newRate = RATE/2
    return resampleSoundBytes(clip, newRate, CHANNELS)
   
'''
' Resamples soundclip at a slower rate, slowing it down and lowering pitch.
'''
def SlowDown(clip):
    newRate = int(RATE*1.5)
    return resampleSoundBytes(clip, newRate, CHANNELS)

'''
' Resamples soundclip at a slower rate, slowing it down and lowering pitch.
'''
def LargeSlowDown(clip):
    newRate = RATE*2
    return resampleSoundBytes(clip, newRate, CHANNELS)

'''
' Reverses a soundclip
'''
def Reverse(clip):
    soundArray = fromstring(clip, int16)
    return soundArray[::-1].tostring()
    #newclip = fromstring(clip, int16)
    #cliplen = len(soundArray)
    #for i in xrange(cliplen) :
    #    newclip[i] = soundArray[cliplen-i-1]
    #newclip = array(newclip, uint16)
    return newclip.tostring()
    
    
    
     
       