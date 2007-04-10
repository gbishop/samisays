from numpy import *
from Story import *
import time
from SoundControl import *


class SoundEffects:
    
    def __init__(self,env):
        self.env = env
    
        # Define array of functions for sound effects
        self.sfxFunctions = [ self.SpeedUp, self.LargeSpeedUp, self.SlowDown, self.LargeSlowDown, self.Echo, self.Reverse ]
        self.currSFX = -1
        self.currSFXClip = ''
        
    '''
    ' Increments the current sound effect in a circular fashion
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified sound clip for playback
    '''
    def getNextSFXClip(self):
        self.currSFX = (self.currSFX+1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        self.currSFXClip = self.sfxFunctions[self.currSFX](currClip)
        return self.getCurrSFXClip()
    
    '''
    ' Decrements the current sound effect in a circular fashion
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified sound clip for playback
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
    ' Returns modified sound clip and deletes the current one
    '''
    def getCurrSFXClip(self):
        if self.currSFX != -1:
            return self.currSFXClip
    
    '''
    ' Applies an echo to the sound clip.
    '''
    def Echo(self, clip):
        soundArray = fromstring(clip, int16)
        newclip = fromstring(clip, int16)
        delay = 1000
        echoFactor = 0.6
        for i in xrange(delay+1,len(soundArray)) :
            newclip[i] = soundArray[i] + echoFactor*soundArray[i-delay]

        return newclip.tostring()
    
    '''
    ' Resamples sound clip at a faster rate, speeding it up and raising pitch.
    '''
    def SpeedUp(self, clip):
        newRate = int(RATE/1.5)
        return resampleSoundBytes(clip, newRate, CHANNELS)
    
    '''
    ' Resamples sound clip at a faster rate, speeding it up and raising pitch.
    '''
    def LargeSpeedUp(self, clip):
        newRate = RATE/2
        return resampleSoundBytes(clip, newRate, CHANNELS)
       
    '''
    ' Resamples sound clip at a slower rate, slowing it down and lowering pitch.
    '''
    def SlowDown(self, clip):
        newRate = int(RATE*1.5)
        return resampleSoundBytes(clip, newRate, CHANNELS)
    
    '''
    ' Resamples sound clip at a slower rate, slowing it down and lowering pitch.
    '''
    def LargeSlowDown(self, clip):
        newRate = RATE*2
        return resampleSoundBytes(clip, newRate, CHANNELS)
    
    '''
    ' Reverses a sound clip
    '''
    def Reverse(self, clip):
        soundArray = fromstring(clip, int16)
        newclip = fromstring(clip, int16)
        cliplen = len(soundArray)
        
        for i in xrange(cliplen) :
            newclip[i] = soundArray[cliplen-i-1]
        newclip = array(newclip, uint16)
        return newclip.tostring()
    
    
    
     
       