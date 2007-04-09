import os
import wx
import copy
from SoundControl import *
from Story import *
from SoundLibrary import *


INSTR_DIR = 'instr_text/'

class AuiInsertSound:
    
    def __init__(self, env):
        self.env = env

    def takeOver(self):
        self.SL = SoundLibrary(self.env)
        
        self.keyDown = False # Flag to tell if a key is already being held down
        self.keyDownCode = -1 # Code to recognize which key is being held down
        
        self.getHelp()
        self.env['keyUpFunct'] = self.onKeyUp
        self.env['keyDownFunct'] = self.onKeyDown
                
    ''' 
    ' Handles event when a key is pressed. 
    '''
    def onKeyDown(self, event):
        if not self.keyDown:
            self.keyDown = True
            self.keyDownCode = event.GetKeyCode()
            
        event.Skip()
    
    ''' 
    ' Handles event when a key is released by calling the correct function for 
    ' each valid key.
    '''
    def onKeyUp(self, event):
        
        keyCode = event.GetKeyCode()
        if self.keyDownCode != keyCode: # If released key is not the first one pressed, ignore it
            return
        
        self.keyDown = False
        
        # Define dictionary of functions for valid keys
        keyFunctions = {wx.WXK_SPACE : self.select, wx.WXK_RETURN : self.getHelp,
                        wx.WXK_DOWN : self.navDown, wx.WXK_UP : self.navUp,
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight,
                        wx.WXK_ESCAPE : self.quit}
        

        if not keyCode in keyFunctions: # Ignore invalid keys
            return
        
        self.env['SoundControl'].stopPlay() # Stop any sound that is playing
        
        # If not yet navigated to a category, ignore keys and repeat instructions
        if not self.SL.onValidCat() and not (keyCode==wx.WXK_LEFT or 
                                             keyCode==wx.WXK_RIGHT or 
                                             keyCode == wx.WXK_ESCAPE):
            self.getHelp()
        else:
            keyFunctions[keyCode]() # Call function for valid key
            self.env['guiWorking'].updateStats()
        
        event.Skip()
     
    '''
    ' Called when navigate left key is released.
    ' Moves to the category to previous category in cyclical fashion.
    '''
    def navLeft(self):
        self.env['SoundControl'].speakText(self.SL.getPrevCatName())
    
    '''
    ' Called when navigate right key is released.
    ' Moves to the next category in cyclical fashion.
    '''    
    def navRight(self):
        self.env['SoundControl'].speakText(self.SL.getNextCatName())
 
    '''
    ' Called when navigate up key is released.
    ' Moves to the previous sound of the current category in cyclical fashion.
    '''   
    def navUp(self):
        
        self.env['SoundControl'].playSoundBytes(self.SL.getPrevSoundBytes())
    
    '''
    ' Called when navigate down key is released.
    ' Moves to the next sound of the current category in cyclical fashion.
    '''       
    def navDown(self):
        self.env['SoundControl'].playSoundBytes(self.SL.getNextSoundBytes())

    
    ''' 
    ' Called when help key is released.
    ' Notifies the user of the current options.
    '''
    def getHelp(self):
        self.env['SoundControl'].speakTextFile(INSTR_DIR + 'insert_sound.txt')
    
    ''' 
    ' Called when selection key is released.
    ' If a sound has been navigated to, it is inserted into the story
    ' and control is returned to the StoryCreationAUI class that called
    ' this object.
    '''    
    def select(self):
        if not self.SL.onValidSound():
            self.getHelp()
            return
        
        soundBytes = self.SL.getCurrSoundBytes()
        type = SND
        if self.SL.currCat == self.SL.sfxCat:
            self.env['story'].deleteClip()
            type = SFX
        self.env['story'].insertClip(''.join(soundBytes), type)
        self.env['SoundControl'].playSoundBytes(soundBytes)
        self.quit()
        
    def quit(self):
        self.env['SoundControl'].playSoundBytes(self.env['story'].getCurrClip())
        self.env['auiStoryCreation'].takeKeyBindings()