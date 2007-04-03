from numpy import *
from Story import *
from SoundControl import *

DEFAULT_RATE = 44100
DEFAULT_CHANS = 1

class SoundEffects:
    
    def __init__(self,env):
        self.env = env
    
        # Define array of functions for sound effects
        self.sfxFunctions = [ self.SpeedUp, self.LargeSpeedUp, self.SlowDown, self.LargeSlowDown, self.Echo, self.Reverse ]
        self.currSFX = -1
        
    '''
    ' Increments the current sound effect in a circular fashion
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified sound clip for playback
    '''
    def getNextSFXClip(self):
        self.currSFX = (self.currSFX+1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        return self.sfxFunctions[self.currSFX](currClip)
    
    '''
    ' Decrements the current sound effect in a circular fashion
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified sound clip for playback
    '''
    def getPrevSFXClip(self):
        self.currSFX = (self.currSFX-1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        return self.sfxFunctions[self.currSFX](currClip)
    
    '''
    ' Returns the current sound effect
    ' Calls the relevant sound effect function mapped in self.sfxFunctions array
    ' Returns modified sound clip and deletes the current one
    '''
    def getCurrSFXClip(self):
        if self.currSFX != -1:
            currClip = self.env["story"].getCurrClip()
            self.env["story"].deleteClip()
            return self.sfxFunctions[self.currSFX](currClip)
    
    '''
    ' Applies an echo to the sound clip.
    '''
    def Echo(self, clip):
        soundArray = fromstring(clip, int16)
        newclip = fromstring(clip, int16)
        delay = 10000
        echoFactor = 0.6
        
        for i in xrange(delay+1,len(soundArray)) :
            newclip[i] = soundArray[i] + echoFactor*soundArray[i-delay]
        newclip = array(newclip, uint16)
        return newclip.tostring()
    
    '''
    ' Resamples sound clip at a faster rate, speeding it up and raising pitch.
    '''
    def SpeedUp(self, clip):
        newRate = 32000
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
    
    '''
    ' Resamples sound clip at a faster rate, speeding it up and raising pitch.
    '''
    def LargeSpeedUp(self, clip):
        newRate = 25200
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
       
    '''
    ' Resamples sound clip at a slower rate, slowing it down and lowering pitch.
    '''
    def SlowDown(self, clip):
        newRate = 57300
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
    
    '''
    ' Resamples sound clip at a slower rate, slowing it down and lowering pitch.
    '''
    def LargeSlowDown(self, clip):
        newRate = 77175
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
    
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
    
    
    
     
       