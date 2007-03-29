

class AuiStorySelection:
    
    def __init__(self, env):
        self.env = env
        
    ''' 
    ' Handles event when a key is pressed. 
    '''
    def onKeyDown(self, event):
        
        if self.keyDown: # Some key is already being held down
            return
        
        self.keyDownCode = event.GetKeyCode()
        self.keyDown = True
        
        if self.keyDownCode == wx.WXK_SPACE: # If key is record button, begin recording
            self.stopPlayback = True 
            self.env['SoundControl'].stopPlay()
            self.env['SoundControl'].startRecord()
        
        event.Skip()
        
    ''' 
    ' Handles event when a key is released by calling the correct function for 
    ' each valid key.
    '''
    def onKeyUp(self, event):

        CTRL = 308 # keyCode for CTRL
        
        keyCode = event.GetKeyCode()
        if self.keyDownCode != keyCode: # If released key is not the first one pressed, ignore it
            return
        
        self.keyDown = False
        
        # Define dictionary of functions for valid keys
        keyFunctions = {wx.WXK_SPACE : self.recordingFinished, CTRL : self.playbackStory, 
                        wx.WXK_DOWN : self.insertSound, wx.WXK_UP : self.deleteClip,
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight,
                        wx.WXK_ESCAPE : self.quit, wx.WXK_RETURN: self.getHelp,
                        wx.WXK_PAUSE: self.insertBreak}
        
        if keyCode not in keyFunctions: # If key has no function, ignore it
            return      
        
        if keyCode != wx.WXK_UP: # If key is not the delete key, a delete is not being confirmed
            self.deleteConfirmed = False
        
        # Stop any sound that is playing
        self.stopPlayback = True 
        self.env['SoundControl'].stopPlay()
        
        
        if self.env['story'].needsTitle() and keyCode != wx.WXK_SPACE: 
            # If no title exists, nothing is to be done until one is recorded
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'needs_title.txt')
        else:
            # Key and context is valid, go to the function required
            keyFunctions[keyCode]()
            