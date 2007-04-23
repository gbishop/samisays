import os
import wx
import copy
from SoundControl import *
from Story import *
from SoundLibrary import *

class AuiInsertSound:
    
    def __init__(self, env):
        self.env = env

    def takeOver(self):
        self.keyDown = False # Flag to tell if a key is already being held down
        self.keyDownCode = -1 # Code to recognize which key is being held down
        
        self.mode = CAT_MODE
        
        self.setInstructions()

        self.env['keyUpFunct'] = self.onKeyUp
        self.env['keyDownFunct'] = self.onKeyDown
        
        if self.SL.currCat == -1:
            self.getHelp()
        else:
            self.env['SoundControl'].speakText(self.SL.getCurrCatName())
    
    def reloadSoundLibrary(self):
        self.SL = SoundLibrary(self.env)
    
    def setInstructions(self):
        if self.mode == CAT_MODE:
            self.currInstr = file(INSTR_DIR + 'insert_sound_cat.txt', 'r').read()
        elif self.mode == SND_MODE:
            self.currInstr = file(INSTR_DIR + 'insert_sound_snd.txt', 'r').read()
        
        self.env['guiWorking'].setInstructions(self.currInstr)
        
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
        keyFunctions = {wx.WXK_UP : self.select, wx.WXK_RETURN : self.getHelp,
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight,
                        wx.WXK_HOME : self.jumpLeft, wx.WXK_END : self.jumpRight,
                        wx.WXK_DOWN : self.getHelp, wx.WXK_ESCAPE : self.back}
        

        if not keyCode in keyFunctions: # Ignore invalid keys
            return
        
        self.env['SoundControl'].stopPlay() # Stop any sound that is playing
        
        # If not yet navigated to a category, ignore keys and repeat instructions
        if not self.SL.onValidCat() and keyCode not in [wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_ESCAPE]:
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
        if self.mode == CAT_MODE:
            self.env['SoundControl'].speakText(self.SL.getPrevCatName())
        elif self.mode == SND_MODE:
            self.env['SoundControl'].playSoundBytes(self.SL.getPrevSoundBytes())
    
    '''
    ' Called when navigate right key is released.
    ' Moves to the next category in cyclical fashion.
    '''    
    def navRight(self):
        if self.mode == CAT_MODE:
            self.env['SoundControl'].speakText(self.SL.getNextCatName())
        elif self.mode == SND_MODE:
            self.env['SoundControl'].playSoundBytes(self.SL.getNextSoundBytes())
 
    def jumpLeft(self):
        if self.mode == CAT_MODE:
            self.SL.currCat = 0
            self.env['SoundControl'].speakText(self.SL.getCurrCatName())
        elif self.mode == SND_MODE:
            self.SL.currSND = 0
            self.env['SoundControl'].playSoundBytes(self.SL.getCurrSoundBytes())
        
    def jumpRight(self):
        if self.mode == CAT_MODE and self.env['story'].hasTrash():
            self.SL.currCat = self.SL.trashCat
            self.env['SoundControl'].speakText(self.SL.getCurrCatName())
        elif self.mode == CAT_MODE:
            self.SL.currCat = self.SL.sfxCat
            self.env['SoundControl'].speakText(self.SL.getCurrCatName())
        elif self.mode == SND_MODE:
            self.SL.currSND = self.currCatLen-1
            self.env['SoundControl'].playSoundBytes(self.SL.getCurrSoundBytes())
    ''' 
    ' Called when help key is released.
    ' Notifies the user of the current options.
    '''
    def getHelp(self):
        self.env['SoundControl'].speakText(self.currInstr)
    
    ''' 
    ' Called when selection key is released.
    ' If a sound has been navigated to, it is inserted into the story
    ' and control is returned to the StoryCreationAUI class that called
    ' this object.
    '''    
    def select(self):
        
        if self.mode == CAT_MODE and self.SL.onValidCat():
            self.mode = SND_MODE
            self.SL.currSound = -1
            self.setInstructions()
            self.getHelp()
        elif self.mode == SND_MODE and (self.SL.onValidSound() or self.SL.currCat == self.SL.sfxCat):   
            soundBytes = self.SL.getCurrSoundBytes()
            type = SND_MODE
            if self.SL.currCat == self.SL.sfxCat:
                if self.env['story'].clipIsTitle():
                    self.env['story'].replaceTitle(soundBytes)
                    self.quit()
                    return
                else:
                    self.env['story'].deleteClip()
                    type = SFX
            self.env['story'].insertClip(soundBytes, type)
            self.quit()
        else:
            self.getHelp()
            
    def back(self):
        if self.mode == CAT_MODE:
            self.quit()
        elif self.mode == SND_MODE:
            self.mode = CAT_MODE
            self.setInstructions()
            self.env['SoundControl'].speakText(self.SL.getCurrCatName())
        
    def quit(self):
        self.env['SoundControl'].playSoundBytes(self.env['story'].getCurrClip())
        self.env['auiStoryCreation'].takeKeyBindings()
        self.env['auiStoryCreation'].setInstructions()