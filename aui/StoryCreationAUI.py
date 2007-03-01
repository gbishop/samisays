import threading
import wx
from SoundControl import *
from Story import *
from InsertSoundAUI import *

INSTR_DIR = 'instr_sounds/'

'''
' Class Name:  StoryCreationAUI
' Description: Captures keys and gives audio cues to control the creation of a story.
'              Allows user to create, navigate, and delete the clips of a story.  Also
'              enables user to enter the module for inserting sound effects.  Exiting
'              this module returns the user to managing his or her stories.
'''
class StoryCreationAUI:
    
    ''' 
    ' Constructor initializes object. 
    '''
    def __init__(self, parent, story=None):
        self.main = parent # Story Manager
        self.SC = parent.SC # Sound Control
        self.SC.playSoundFile(INSTR_DIR + 'creation_welcome.wav') # Play Welcome
        if story == None:
            self.story = Story() # Initialize Empty Story
            #self.firstTitle = True
        else:
            self.story = story # Open existing story

        
        self.keyDown = False # Flag to tell if a key is already being held down
        self.keyDownCode = -1 # Code to recognize which key is being held down
                
        self.deleteConfirmed = False # Flag for whether delete needs confirmation
        
        self.stopPlayBack = False # Flag to interrupt full playback of story
              
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
            self.SC.stopPlay()
            self.SC.startRecord()
        
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
                        wx.WXK_ESCAPE : self.getHelp, wx.WXK_RETURN: self.exportToMp3}
        
        if keyCode not in keyFunctions: # If key has no function, ignore it
            return      
        
        if keyCode != wx.WXK_UP: # If key is not the delete key, a delete is not being confirmed
            self.deleteConfirmed = False
        
        # Stop any sound that is playing
        self.stopPlayback = True 
        self.SC.stopPlay()
        
        
        if self.story.needsTitle() and keyCode != wx.WXK_SPACE: 
            # If no title exists, nothing is to be done until one is recorded
            self.SC.playSoundFile(INSTR_DIR + 'needs_title.wav')
        else:
            # Key and context is valid, go to the function required
            keyFunctions[keyCode]()
            
        event.Skip()

    ''' 
    ' Called when help key is released.
    ' Notifies the user of the current options.  The case where there is no title 
    ' (len(story) == 0) is already handled in OnKeyUp.
    '''
    def getHelp(self):
        
        story = self.story
        soundFile = INSTR_DIR

        if len(story) == 1:
            soundFile += 'after_title.wav'
        elif len(story) == 2:
            soundFile += 'after_first_clip.wav'
        else:
            soundFile += 'creation_instructions.wav'
        
        self.SC.playSoundFile(soundFile)
        
    ''' 
    ' Called when record key is lifted.
    ' Ends recording of clip, inserts it into the story, and replays it. 
    '''
    def recordingFinished(self):
        
        soundBytes = self.SC.stopRecord() # End record and get recorded bytes
        soundBytes = normalizeSoundBytes(soundBytes)
        story = self.story
        
 #       if story.needsTitle() and self.firstTitle: 
 #           self.firstTitle = False
 #           story.replaceTitle(soundBytes)
 #           self.SC.playSoundBytes(soundBytes + resamplePySonic(pySonic.FileSample('instr_sounds/main_instructions.wav')))
 
        if story.needsTitle():
            story.replaceTitle(soundBytes)
        else:
            story.insertClip(soundBytes)
        
        self.SC.playSoundBytes(soundBytes)
        
    ''' 
    ' Called when Story Playback key is released.
    ' Starts a thread to play back the entire story in order. If interrupted by a valid key, 
    ' the current clip is the last to begin being played.  A separate thread is used to allow
    ' this functionality.
    '''
    def playbackStory(self):
        self.stopPlayback = False
        spb = StoryPlayback(self) 
        spb.start()
        
    '''
    ' Called when insert sound key is released. 
    ' Passes control to the InsertSoundAUI class to allow user to insert a sound effect.
    '''
    def insertSound(self):
        ISA = InsertSoundAUI(self)
        
        # Pass key bindings to InsertSoundAUI
        self.main.keyUpFunct = ISA.onKeyUp
        self.main.keyDownFunct = ISA.onKeyDown
    
    '''
    ' Called when delete key is released.
    ' If previous key pressed was also the delete key, deletes the current clip. Otherwise,
    ' requests confirmation for delete.  If current clip is title, notifies user that a new
    ' title must be recorded before anything else can be done.
    '''    
    def deleteClip(self):
        
        story = self.story
        
        if self.deleteConfirmed:
            
            if story.currClip == 0:
                story.replaceTitle('')
                self.SC.playSoundFile(INSTR_DIR + 'needs_title.wav')
            else:
                self.SC.playSoundBytes(story.deleteClip())
        
        else:
            if story.currClip == 0:
                self.SC.playSoundFile(INSTR_DIR + 'delete_title.wav')
            else:
                self.SC.playSoundFile(INSTR_DIR + 'delete_clip.wav')
            self.deleteConfirmed = True
                
    '''
    ' Called when navigate left key is released.
    ' Moves to the previous clip in the story and plays it back.
    '''
    def navLeft(self):
        self.SC.playSoundBytes(self.story.getPreviousClip())
    
    '''
    ' Called when navigate right key is released.
    ' Moves to the next clip in the story and plays it back.
    '''
    def navRight(self):
        self.SC.playSoundBytes(self.story.getNextClip())
       
    ''' Test function for exporting to mp3. '''
    def exportToMp3(self):
        encodeToMp3(self.story.getStory(),'test.mp3')
        
        
'''
' Class Name:  StoryPlayback
' Description: This class is run as a separate thread. Its only function is to play back
'              the entire story in order.  If any valid key is pressed during the playback,
'              a flag is set by the StoryCreationAUI object that causes this thread to exit
'              early.  Therefore, the current clip will remain the last clip that the thread
'              began to play.  This class is run as a separate thread in order to facilitate
'              this functionality.
'''
class StoryPlayback(threading.Thread):
    
    '''
    ' Constructor initializes thread.
    '''
    def __init__(self, parent):
        self.SCA = parent
        threading.Thread.__init__(self)
    
    '''
    ' Called when thread is started.  Plays back each clip of the story in sequence and exits when
    ' either the stopPlayback flag is set to True or the last clip in the story has been played.
    '''
    def run(self):
        story = self.SCA.story
        SC = self.SCA.SC
        
        story.currClip = -1
        
        while not self.SCA.stopPlayback and (story.currClip < len(story)-1):
            SC.playSoundBytes(story.getNextClip())
            while (SC.isPlaying()):
                pass
        
        
        
        
        