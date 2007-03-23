import os
import wx
from SoundControl import *
from Story import *
from SoundLibrary import *


INSTR_DIR = 'instr_sounds/'

class InsertSoundAUI:
    
    def __init__(self, env):
        self.env = env
        
        self.SL = SoundLibrary()
        
        self.keyDown = False # Flag to tell if a key is already being held down
        self.keyDownCode = -1 # Code to recognize which key is being held down
    
        self.getHelp()
        
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
        keyFunctions = {wx.WXK_SPACE : self.select, wx.WXK_ESCAPE : self.getHelp,
                        wx.WXK_DOWN : self.navDown, wx.WXK_UP : self.navUp,
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight}
        

        if not keyCode in keyFunctions: # Ignore invalid keys
            return
        
        self.env['SoundControl'].stopPlay() # Stop any sound that is playing
        
        # If not yet navigated to a category, ignore keys and repeat instructions
        if not self.SL.onValidCat() and not (keyCode==wx.WXK_LEFT or keyCode==wx.WXK_RIGHT):
            self.getHelp()
        else:
            keyFunctions[keyCode]() # Call function for valid key
        
        event.Skip()
     
    '''
    ' Called when navigate left key is released.
    ' Moves to the category to previous category in cyclical fashion.
    '''
    def navLeft(self):
        self.env['SoundControl'].playSoundFile(self.SL.getPrevCatNameFile())
    
    '''
    ' Called when navigate right key is released.
    ' Moves to the next category in cyclical fashion.
    '''    
    def navRight(self):
        self.env['SoundControl'].playSoundFile(self.SL.getNextCatNameFile())
 
    '''
    ' Called when navigate up key is released.
    ' Moves to the previous sound of the current category in cyclical fashion.
    '''   
    def navUp(self):
        self.env['SoundControl'].playSoundFile(self.SL.getPrevSoundFile())
    
    '''
    ' Called when navigate down key is released.
    ' Moves to the next sound of the current category in cyclical fashion.
    '''       
    def navDown(self):
        self.env['SoundControl'].playSoundFile(self.SL.getNextSoundFile())

    
    ''' 
    ' Called when help key is released.
    ' Notifies the user of the current options.
    '''
    def getHelp(self):
        self.env['SoundControl'].playSoundFile(INSTR_DIR + 'insert_sound.mp3')
    
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
        
        soundBytes = resampleSoundFile(self.SL.getCurrSoundFile())
        soundBytes = normalizeSoundBytes(soundBytes)
        self.env['Story'].insertClip(soundBytes)
        self.env['SoundControl'].playSoundBytes(soundBytes)
        
        # Return key bindings to StoryCreationAUI class that called me
        self.env['keyDownFunct'] = self.env['auiStoryCreation'].onKeyDown
        self.env['keyUpFunct'] = self.env['auiStoryCreation'].onKeyUp