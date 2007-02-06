import os, threading
import wx, pySonic
from SoundControl import *
from Story import *
from SoundLibraryAUI import *
from SoundLibrary import *


class SoundLibraryAUI:
    
    def __init__(self, parent):
        self.storyAUI = parent
        self.SC = parent.SC
        self.story = parent.story
        
        self.SL = SoundLibrary()
        
        self.SC.playSoundFile('insert_sound_instructions.wav')
        
    def onKeyDown(self, event):
        event.Skip()
        
    def onKeyUp(self, event):
        
        keyCode = event.GetKeyCode()
        
        keyFunctions = {wx.WXK_SPACE : self.select,
                        wx.WXK_DOWN : self.navDown, wx.WXK_UP : self.navUp,
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight}
        

        if keyCode in keyFunctions:
            keyFunctions[keyCode]()
        
        event.Skip()
        
    def navLeft(self):
        self.SC.playSoundFile(self.SL.getPrevCatNameFile())
        
    def navRight(self):
        self.SC.playSoundFile(self.SL.getNextCatNameFile())
        
    def navUp(self):
        self.SC.playSoundFile(self.SL.getPrevSoundFile())
        
    def navDown(self):
        self.SC.playSoundFile(self.SL.getNextSoundFile())
        
    def select(self):
        currSound = pySonic.FileSample(self.SL.getCurrSoundFile())
        soundBytes = self.SC.resamplePySonic(currSound)
        self.story.insertClip(soundBytes)
        parent = self.storyAUI
        parent.main.keyDownFunct = parent.onKeyDown
        parent.main.keyUpFunct = parent.onKeyUp