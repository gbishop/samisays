import threading
import wx
import time
from SoundControl import *
from Story import *
from InsertSoundAUI import *

INSTR_DIR = 'instr_text/'

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
    def __init__(self, env):
        self.env = env
        self.env['SoundControl'].speakTextFile(INSTR_DIR + 'creation_welcome.txt') # Play Welcome
        name = ''.join([str(time.localtime()[i]) + '_' for i in xrange(6)])[0:-1]
        self.env['Story'] = Story(name,'adam')
        
        self.keyDown = False # Flag to tell if a key is already being held down
        self.keyDownCode = -1 # Code to recognize which key is being held down
                
        self.deleteConfirmed = False # Flag for whether delete needs confirmation
        self.firstTitle = True # Flag for whether a title has been recorded yet (for first time)
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
                        wx.WXK_ESCAPE : self.getHelp, wx.WXK_RETURN: self.exportToMp3}
        
        if keyCode not in keyFunctions: # If key has no function, ignore it
            return      
        
        if keyCode != wx.WXK_UP: # If key is not the delete key, a delete is not being confirmed
            self.deleteConfirmed = False
        
        # Stop any sound that is playing
        self.stopPlayback = True 
        self.env['SoundControl'].stopPlay()
        
        
        if self.env['Story'].needsTitle() and keyCode != wx.WXK_SPACE: 
            # If no title exists, nothing is to be done until one is recorded
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'needs_title.txt')
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
        textFile = INSTR_DIR

        if len(self.env['Story']) == 1:
            textFile += 'after_title.txt'
        else:
            textFile += 'creation_instructions.txt'
        
        self.env['SoundControl'].speakTextFile(soundFile)
        
    ''' 
    ' Called when record key is lifted.
    ' Ends recording of clip, inserts it into the story, and replays it. 
    '''
    def recordingFinished(self):
        
        soundBytes = self.env['SoundControl'].stopRecord() # End record and get recorded bytes
        soundBytes = normalizeSoundBytes(soundBytes)
        story = self.env['Story']
        
        if story.needsTitle() and self.firstTitle: 
            self.firstTitle = False
            story.replaceTitle(soundBytes)
            soundBytes = soundBytes #+ resampleSoundFile(INSTR_DIR + 'after_title.mp3')
        elif story.needsTitle():
            story.replaceTitle(soundBytes)
        else:
            story.insertClip(soundBytes)
        
        self.env['SoundControl'].playSoundBytes(soundBytes)
        
    ''' 
    ' Called when Story Playback key is released.
    ' Starts a thread to play back the entire story in order. If interrupted by a valid key, 
    ' the current clip is the last to begin being played.  A separate thread is used to allow
    ' this functionality.
    '''
    def playbackStory(self):
        self.stopPlayback = False
        spb = StoryPlayback(self.env) 
        spb.start()
        
    '''
    ' Called when insert sound key is released. 
    ' Passes control to the InsertSoundAUI class to allow user to insert a sound effect.
    '''
    def insertSound(self):
        ISA = InsertSoundAUI(self.env)
        
        # Pass key bindings to InsertSoundAUI
        self.env['keyUpFunct'] = ISA.onKeyUp
        self.env['keyDownFunct'] = ISA.onKeyDown
    
    '''
    ' Called when delete key is released.
    ' If previous key pressed was also the delete key, deletes the current clip. Otherwise,
    ' requests confirmation for delete.  If current clip is title, notifies user that a new
    ' title must be recorded before anything else can be done.
    '''    
    def deleteClip(self):
        
        story = self.env['Story']
        
        if self.deleteConfirmed:
            
            if story.currClip == 0:
                story.replaceTitle('')
                self.env['SoundControl'].speakTextFile(INSTR_DIR + 'needs_title.txt')
            else:
                self.env['SoundControl'].playSoundBytes(story.deleteClip())
        
        else:
            if story.currClip == 0:
                self.env['SoundControl'].speakTextFile(INSTR_DIR + 'delete_title.txt')
            else:
                self.env['SoundControl'].speakTextFile(INSTR_DIR + 'delete_clip.txt')
            self.deleteConfirmed = True
                
    '''
    ' Called when navigate left key is released.
    ' Moves to the previous clip in the story and plays it back.
    '''
    def navLeft(self):
        self.env['SoundControl'].playSoundBytes(self.story.getPreviousClip())
    
    '''
    ' Called when navigate right key is released.
    ' Moves to the next clip in the story and plays it back.
    '''
    def navRight(self):
        self.env['SoundControl'].playSoundBytes(self.story.getNextClip())
       
    ''' Test function for exporting to mp3. '''
    def exportToMp3(self):
        encodeToMp3(self.story.getStory(),'test.mp3',64000)
        
        
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
    def __init__(self, env):
        self.env = env
        threading.Thread.__init__(self)
    
    '''
    ' Called when thread is started.  Plays back each clip of the story in sequence and exits when
    ' either the stopPlayback flag is set to True or the last clip in the story has been played.
    '''
    def run(self):
        
        story = self.env['Story']
        story.currClip = -1
        
        while not self.env['auiStoryCreation'].stopPlayback and (story.currClip < len(story)-1):
            self.env['SoundControl'].playSoundBytes(story.getNextClip())
            while (self.env['SoundControl'].isPlaying()):
                pass
        
        
        
        
        