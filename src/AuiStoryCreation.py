import threading
import wx
import time
from SoundControl import *
from Story import *
from AuiInsertSound import *

INSTR_DIR = 'instr_text/'
BREAK_SOUND = 'lilbeep.wav'
INTRO_SOUND = 'xylophone_intro.mp3'
WAIT_SOUND = 'wait_noise.mp3'
DEFAULT_CROP = 5000
CTRL = 308 # keyCode for CTRL

'''
' Class Name:  StoryCreationAUI
' Description: Captures keys and gives audio cues to control the creation of a story.
'              Allows user to create, navigate, and delete the clips of a story.  Also
'              enables user to enter the module for inserting sound effects.  Exiting
'              this module returns the user to managing his or her stories.
'''
class AuiStoryCreation:
    
    ''' 
    ' Constructor initializes object. 
    '''
    def __init__(self, env):
        self.env = env
        self.breakSoundBytes = soundFileToBytes(BREAK_SOUND)
        self.introSound = soundFileToBytes(INTRO_SOUND)
        self.waitSound = soundFileToBytes(WAIT_SOUND)*50
    
    def takeOver(self):
        self.env['SoundControl'].playSoundBytes(self.introSound, True)
        self.teacherMode = self.env['student'] == self.env['class'].teacher
        
        if self.teacherMode and self.env['story'].needsTitle():
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'template_welcome.txt')
        elif self.env['story'].needsTitle():
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'creation_welcome.txt')
        else:
            self.env['SoundControl'].playSoundBytes(self.env['story'].getTitleBytes())
            
        self.env['auiInsertSound'].reloadSoundLibrary()
        
        self.firstDown = -1 # Code to remmeber which key was held down first
                
        self.deleteConfirmed = False # Flag for whether delete needs confirmation
        self.stopPlayBack = False # Flag to interrupt full playback of story
      
        self.takeKeyBindings()
        self.setInstructions()
        
    def takeKeyBindings(self):
        self.env['keyUpFunct'] = self.onKeyUp
        self.env['keyDownFunct'] = self.onKeyDown
    
    def loadFullStory(self):
        self.env['SoundControl'].playSoundBytes(self.waitSound)
        self.env['story'] = self.env['story'].loadFullStory()
        self.env['SoundControl'].stopPlay()
    
    def setInstructions(self):
        instrFile = INSTR_DIR
        if self.deleteConfirmed:
            if self.env['story'].currClip == 0:
                instrFile += 'delete_title.txt'
            else:
                instrFile += 'delete_confirm.txt'
        elif self.env['story'].needsTitle():
            instrFile += 'needs_title.txt'
        elif self.teacherMode:
            instrFile += 'template_instructions.txt'
        else:
            instrFile += 'creation_instructions.txt'
        self.currInstr = file(instrFile, 'r').read()
        self.env['guiWorking'].setInstructions(self.currInstr)
    
    ''' 
    ' Handles event when a key is pressed. 
    '''
    def onKeyDown(self, event):
        
        if self.firstDown != -1: # Some key is already being held down
            return
        
        self.firstDown = event.GetKeyCode()
        
        if self.firstDown == wx.WXK_SPACE: # If key is record button, begin recording
            self.stopPlayback = True 
            self.env['SoundControl'].stopPlay()
            self.env['SoundControl'].startRecord()
        
        
    ''' 
    ' Handles event when a key is released by calling the correct function for 
    ' each valid key.
    '''
    def onKeyUp(self, event):
        
        keyCode = event.GetKeyCode()
        if self.firstDown != keyCode: # If released key is not the first one pressed, ignore it
            return
        
        self.firstDown = -1
        
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
            self.setInstructions()
        
        # Stop any sound that is playing
        self.stopPlayback = True 
        self.env['SoundControl'].stopPlay()
        
        
        if self.env['story'].needsTitle() and not (keyCode in [wx.WXK_SPACE, wx.WXK_ESCAPE]): 
            # If no title exists, nothing is to be done until one is recorded
            self.getHelp()
        else:
            # Key and context is valid, go to the function required
            keyFunctions[keyCode]()
            self.env['guiWorking'].updateStats()


    ''' 
    ' Called when help key is released.
    ' Notifies the user of the current options.  The case where there is no title 
    ' (len(story) == 0) is already handled in OnKeyUp.
    '''
    def getHelp(self):
        self.env['SoundControl'].speakText(self.currInstr)
        
    ''' 
    ' Called when record key is lifted.
    ' Ends recording of clip, inserts it into the story, and replays it. 
    '''
    def recordingFinished(self):
        
        crop = DEFAULT_CROP*RATE/44100
        
        soundBytes = self.env['SoundControl'].stopRecord() # End record and get recorded bytes
        
        soundBytes = soundBytes[crop:]
        soundBytes = normalizeSoundBytes(soundBytes)

        
        story = self.env['story']
        
        if story.needsTitle():
            story.replaceTitle(soundBytes)
            self.setInstructions()
        else:
            story.insertClip(soundBytes, type = REC)

        
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
    ' Passes control to the AuiInsertSound class to allow user to insert a sound effect.
    '''
    def insertSound(self):
        self.env['auiInsertSound'].takeOver()
    
    def insertBreak(self):
        if not self.teacherMode:
            return
        
        story = self.env['story']
        if story.clipIsBreak():
            self.env['SoundControl'].speakText('You may not have two breaks in a row.')
        else:
            story.insertClip(self.breakSoundBytes, type = BRK)
            self.env['SoundControl'].playSoundBytes(self.breakSoundBytes)
        
    '''
    ' Called when delete key is released.
    ' If previous key pressed was also the delete key, deletes the current clip. Otherwise,
    ' requests confirmation for delete.  If current clip is title, notifies user that a new
    ' title must be recorded before anything else can be done.
    '''    
    def deleteClip(self):

        story = self.env['story']
        if story.clipIsLocked() and not self.teacherMode:
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'no_delete_locked.txt')
        elif self.deleteConfirmed:
            self.deleteConfirmed = False
            if story.currClip == 0:
                story.replaceTitle('')
                self.setInstructions()
                self.getHelp()
            else:
                self.env['SoundControl'].playSoundBytes(story.deleteClip())
                self.setInstructions()
            
        else:
            self.deleteConfirmed = True
            self.setInstructions()
            self.getHelp()
                
    '''
    ' Called when navigate left key is released.
    ' Moves to the previous clip in the story and plays it back.
    '''
    def navLeft(self):
        self.env['SoundControl'].playSoundBytes(self.env['story'].getPreviousClip())
    
    '''
    ' Called when navigate right key is released.
    ' Moves to the next clip in the story and plays it back.
    '''
    def navRight(self):
        self.env['SoundControl'].playSoundBytes(self.env['story'].getNextClip())
           
    ''' Function for gracefully exiting story creation and returning to menu '''
    def quit(self):
        self.env['SoundControl'].playSoundBytes(self.waitSound)
        while not self.env['story'].threadSem.acquire(False):
            pass
        self.env['story'].pickleMutex.acquire()
        self.env['SoundControl'].stopPlay()
        self.env['guiWorking'].Hide()
        self.env['guiStories'].Show()
        self.env['timer'].Stop()
        
        
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
        
        story = self.env['story']
        story.currClip = -1
        
        while not self.env['auiStoryCreation'].stopPlayback and (story.currClip < len(story)-1):
            self.env['SoundControl'].playSoundBytes(story.getNextClip())
            self.env['guiWorking'].updateStats()
            while (self.env['SoundControl'].isPlaying()):
                pass
         