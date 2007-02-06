import wx
import threading
from SoundControl import *
from Story import *
from SoundLibraryAUI import *

class StoryAUI:
    
    def __init__(self,parent,soundControl):
        self.main = parent
        self.SC = soundControl
        self.SC.playSoundFile('opening.wav')
        self.story = Story()
        
        # initialize key recognition variables
        self.keyDown = False
        self.keyDownCode = -1
        
             
    
    def onKeyDown(self, event):
        '''This gets called on when a key is pressed.'''
        
        if self.keyDown:
            return
        
        self.keyDownCode = event.GetKeyCode()
        self.keyDown = True
        
        if self.keyDownCode == wx.WXK_SPACE:
            self.stopPlayback = True
            self.SC.stopPlay()
            self.SC.startRecord()
        
        event.Skip()
        
    def onKeyUp(self, event):
        '''This gets called when a key is released.'''
        CTRL = 308 # keyCode for CTRL
        
        keyCode = event.GetKeyCode()
        if self.keyDownCode != keyCode:
            return
        
        self.keyDown = False
        
        keyFunctions = {wx.WXK_SPACE : self.recordingFinished, CTRL : self.playbackStory, 
                        wx.WXK_DOWN : self.insertSound, wx.WXK_UP : self.deleteClip,
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight}
        
        if keyCode not in keyFunctions:
            return      
        
        
        self.stopPlayback = True
        self.SC.stopPlay()
        
        if self.story.needsTitle() and keyCode != wx.WXK_SPACE:
            self.SC.playSoundFile('delete_title.wav')
        elif keyCode in keyFunctions:
            keyFunctions[keyCode]()
            
        event.Skip()
    
    def recordingFinished(self):
        ''' Called when spacebar has been released after recording '''
        
        soundBytes = self.SC.stopRecord()
        story = self.story
        
        if story.needsTitle():
            story.replaceTitle(soundBytes)
        else:
            story.insertClip(soundBytes)
      
        self.SC.playSoundBytes(soundBytes)
            
    
    def playbackStory(self):
        self.stopPlayback = False
        spb = StoryPlayback(self)
        spb.start()
        
    def insertSound(self):
        SLA = SoundLibraryAUI(self)
        self.main.keyUpFunct = SLA.onKeyUp
        self.main.keyDownFunct = SLA.onKeyDown
        
    def deleteClip(self):
        story = self.story
        
        if story.currClip == 0:
            self.SC.playSoundFile('delete_title.wav')
            story.replaceTitle('')
        else:
            story.deleteClip()
        
    def navLeft(self):
        self.SC.playSoundBytes(self.story.getPreviousClip())
    
    def navRight(self):
        self.SC.playSoundBytes(self.story.getNextClip())
        

class StoryPlayback(threading.Thread):
    def __init__(self, parent):
        self.SA = parent
        threading.Thread.__init__(self)
        
    def run(self):
        story = self.SA.story
        SC = self.SA.SC
        
        story.currClip = -1
        
        while not self.SA.stopPlayback and (story.currClip < story.getNumClips()-1):
            SC.playSoundBytes(story.getNextClip())
            while (SC.isPlaying()):
                pass
        
        
        
        
        