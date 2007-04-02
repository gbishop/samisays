import threading
import wx
import time
import os
from SoundControl import *
from Story import *

INSTR_DIR = 'instr_text/'

class AuiStorySelection:
    
    def __init__(self, env):
        self.env = env
        self.student = self.env['student']
        self.env['SoundControl'].speakTextFile(INSTR_DIR + 'selection_welcome.txt') # Play Welcome
        
        if(len(self.student.stories) != 0):
            self.studentIndex = 0
            self.env['guiStories'].loadStory(self.student.stories[self.env['guiStories'].lstStories.GetSelection()]);
            self.env['guiStories'].playTitle()
        else:
            self.studentIndex = -1
        
        
    ''' 
    ' Handles event when a key is pressed. 
    '''
    def onKeyDown(self, event):
        
        self.unlockStarted = False
        keyCode = event.GetKeyCode()
        if(event.ControlDown() and event.ShiftDown() and (keyCode == wx.WXK_TAB)):
            self.unlockStarted = True
        
    ''' 
    ' Handles event when a key is released by calling the correct function for 
    ' each valid key.
    '''
    def onKeyUp(self, event):
        
        CTRL = 308 # keyCode for CTRL
        
        keyCode = event.GetKeyCode()
        
        # Define dictionary of functions for valid keys
        keyFunctions = {wx.WXK_TAB : self.unlock, wx.WXK_RIGHT : self.goRight, 
                        wx.WXK_LEFT : self.goLeft, wx.WXK_SPACE : self.selectStory,
                        CTRL : self.playStory, wx.WXK_ESCAPE : self.exit,
                        wx.WXK_RETURN : self.newStory}
        
        if keyCode not in keyFunctions: # If key has no function, ignore it
            return
        else:
            keyFunctions[keyCode]()
        
    def unlock(self):
        if(self.unlockStarted):
            self.env['guiStories'].unlock()
            
    def goRight(self):
        if self.studentIndex != -1:
            self.env['SoundControl'].stopPlay()
            self.studentIndex += 1
            if(len(self.student.stories) == self.studentIndex):
                self.studentIndex = 0
            self.env['guiStories'].lstStories.SetSelection(self.studentIndex)
            self.env['guiStories'].loadStory(self.student.stories[self.env['guiStories'].lstStories.GetSelection()]);
            self.env['guiStories'].playTitle()
    
    def goLeft(self):
        if self.studentIndex != -1:
            self.env['SoundControl'].stopPlay()
            self.studentIndex -= 1
            if(self.studentIndex == -1):
                self.studentIndex = len(self.student.stories) - 1
            self.env['guiStories'].lstStories.SetSelection(self.studentIndex)
            self.env['guiStories'].loadStory(self.student.stories[self.env['guiStories'].lstStories.GetSelection()]);
            self.env['guiStories'].playTitle()
    
    def selectStory(self):
        self.env['guiStories'].btnSelectPressed(None)
    
    def playStory(self):
        self.env['SoundControl'].stopPlay()
        self.env['guiStories'].playStory()
        
    def exit(self):
        self.env['guiStories'].btnBackPressed(None)
        
    def newSotry(self):
        self.env['guiStories'].btnCreatePressed(None)
            