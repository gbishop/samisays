from numpy import *
from Story import *

class SoundEffects:
    
    def __init__(self,env):
        self.env = env
    
        # Define dictionary of functions for sound effects
        self.sfxFunctions = [ self.doRobot, self.doHighPitch, self.doLowPitch, self.doEcho ]
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
    
    def doRobot(self, clip):
        return clip
    
    def doHighPitch(self, clip):
        return clip
    
    def doLowPitch(self, clip):
        return clip
    
    def doEcho(self, clip):
        soundArray = fromstring(clip, int16)
        newclip = soundArray
        delay = 1.0
        echoFactor = 0.6
        for i in xrange(delay+1,len(soundArray)) :
            newclip[i] = newclip[i] + echoFactor*soundArray[i-delay]
        return newclip.tostring()
    
    
    
     
       