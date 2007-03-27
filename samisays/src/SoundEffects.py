from numpy import *
from Story import *
from SoundControl import *

DEFAULT_RATE = 44100
DEFAULT_CHANS = 1

class SoundEffects:
    
    def __init__(self,env):
        self.env = env
    
        # Define dictionary of functions for sound effects
        self.sfxFunctions = [ self.SpeedUp, self.LargeSpeedUp, self.SlowDown, self.LargeSlowDown, self.Echo ]
        self.currSFX = -1
        
    '''
    ' Increments the current sound effect in a circular fashion
    ' Calls the relevant sound effect function mapped in self.sfxFunctions dictionary
    ' Returns modified sound clip for playback
    '''
    def getNextSFXClip(self):
        self.currSFX = (self.currSFX+1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        return self.sfxFunctions[self.currSFX](currClip)
    
    def getPrevSFXClip(self):
        self.currSFX = (self.currSFX-1)%len(self.sfxFunctions)
        currClip = self.env["story"].getCurrClip()
        return self.sfxFunctions[self.currSFX](currClip)
    
    def doRobot(self, clip):
        return clip
    
    def doHighPitch(self, clip):
        return clip
    
    def doLowPitch(self, clip):
        return clip
    
    def Echo(self, clip):
        soundArray = fromstring(clip, int16)
        newclip = fromstring(clip, int16)
        delay = 10000
        echoFactor = 0.6
        
        for i in xrange(delay+1,len(soundArray)) :
            newclip[i] = soundArray[i] + echoFactor*soundArray[i-delay]
        newclip = array(newclip, uint16)
        return newclip.tostring()
    
    def SpeedUp(self, clip):
        newRate = 32000
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
    
    def LargeSpeedUp(self, clip):
        newRate = 25200
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
       
    def SlowDown(self, clip):
        newRate = 57300
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
    
    def LargeSlowDown(self, clip):
        newRate = 77175
        return resampleSoundBytes(clip, newRate, DEFAULT_CHANS)
    
    
    
     
       