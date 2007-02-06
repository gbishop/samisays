import wx
import threading
import pySonic
from SoundControl import *
from Story import *
from SoundLibraryAUI import *

class StoryAUI:
    
    def __init__(self,parent,soundControl):
        self.main = parent
        self.SC = soundControl
        self.SC.playSoundFile('instr_sounds/record_title.wav')
        self.story = Story()
        self.firstTitle = True
        
        # initialize key recognition variables
        self.keyDown = False
        self.keyDownCode = -1
        
        self.deleteConfirmed = False
              
    
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
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight,
                        wx.WXK_RETURN: self.exportToMp3}
        
        if keyCode not in keyFunctions:
            return      
        
        if keyCode != wx.WXK_UP:
            self.deleteConfirmed = False
        
        self.stopPlayback = True
        self.SC.stopPlay()
        
        if self.story.needsTitle() and keyCode != wx.WXK_SPACE:
            self.SC.playSoundFile('instr_sounds/record_title.wav')
        else:
            keyFunctions[keyCode]()
            
        event.Skip()
    
    def recordingFinished(self):
        ''' Called when spacebar has been released after recording '''
        
        soundBytes = self.SC.stopRecord()
        story = self.story
        
        if story.needsTitle() and self.firstTitle:
            self.firstTitle = False
            story.replaceTitle(soundBytes)
            self.SC.playSoundBytes(soundBytes + resamplePySonic(pySonic.FileSample('instr_sounds/main_instructions.wav')))
        elif story.needsTitle():
            story.replaceTitle(soundBytes)
            self.SC.playSoundBytes(soundBytes)
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
        
        if self.deleteConfirmed:
            story = self.story
        
            if story.currClip == 0:
                story.replaceTitle('')
                self.SC.playSoundFile('instr_sounds/record_title.wav')
            else:
                self.SC.playSoundBytes(story.deleteClip())
        
        else:
            self.SC.playSoundFile('instr_sounds/confirm_delete.wav')
            self.deleteConfirmed = True
                
            
        
    def navLeft(self):
        self.SC.playSoundBytes(self.story.getPreviousClip())
    
    def navRight(self):
        self.SC.playSoundBytes(self.story.getNextClip())
        
    def exportToMp3(self):
        encodeToMp3(self.story.getStory(),'test.mp3')
        

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
        
        
        
        
        