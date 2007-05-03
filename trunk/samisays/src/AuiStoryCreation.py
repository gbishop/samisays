import threading
import wx
import time
from SoundControl import *
from Story import *
from AuiInsertSound import *
from Constants import *


class AuiStoryCreation:
    ''' 
    Captures keys and gives audio cues to control the creation of a story.
    Allows user to create, navigate, and delete the clips of a story.  Also
    enables user to enter the module for inserting sound effects.  Exiting
    this module returns the user to managing his or her stories.
    '''    
    
    def __init__(self, env):
        '''
        Constructor receives global objects and initializes object.
        '''
        
        self.env = env
        self.breakSoundBytes = soundFileToBytes(BREAK_SOUND)
        self.introSound = soundFileToBytes(INTRO_SOUND)
        self.waitSound = soundFileToBytes(WAIT_SOUND)*50
    
    def takeOver(self):
        '''
        Gives user control to AuiStoryCreation by setting key bindings and initializes AUI.
        '''
        
        self.env['SoundControl'].playSoundBytes(self.introSound, True)
        self.teacherMode = self.env['student'] == self.env['class'].teacher #teacher template mode
        
        if self.teacherMode and self.env['story'].needsTitle():
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'template_welcome.txt')
        elif self.env['story'].needsTitle():
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'creation_welcome.txt')
        else:
            self.env['SoundControl'].playSoundBytes(self.env['story'].getTitleBytes())
            
        self.env['soundLibrary'].loadLibrary()
        
        self.firstDown = -1 # Code to remmeber which key was held down first
                
        self.deleteConfirmed = False # Flag for whether delete needs confirmation
        self.quitConfirmed = False
        self.stopPlayBack = False # Flag to interrupt full playback of story
      
        self.takeKeyBindings()
        self.setInstructions()
        
    def takeKeyBindings(self):
        '''
        Binds keys to this class.
        '''
        
        self.env['keyUpFunct'] = self.onKeyUp
        self.env['keyDownFunct'] = self.onKeyDown
    
    def loadFullStory(self):
        '''
        Plays wait sound while full story is loaded.  Initially, only title was loaded for story selection.
        '''
        
        self.env['SoundControl'].playSoundBytes(self.waitSound)
        self.env['story'] = self.env['story'].loadFullStory()
        self.env['SoundControl'].stopPlay()
    
    def setInstructions(self):
        '''
        Sets current instructions based on state of the story.  These will be spoken when user presses help key
        and displayed on the visualizer gui.
        '''
        
        instrFile = INSTR_DIR
        if self.deleteConfirmed:
            if self.env['story'].currClip == 0:
                instrFile += 'delete_title.txt'
            else:
                instrFile += 'delete_confirm.txt'
        elif self.quitConfirmed:
            instrFile += 'quit_confirm.txt'
        elif self.env['story'].needsTitle():
            instrFile += 'needs_title.txt'
        elif self.teacherMode:
            instrFile += 'template_instructions.txt'
        else:
            instrFile += 'creation_instructions.txt'
        self.currInstr = file(instrFile, 'r').read()
        self.env['guiVisualizer'].setInstructions(self.currInstr)
    
    
    def onKeyDown(self, event):
        '''
        Handles event when a key is pressed.  Keys track of first key to be held down and ignores all others until released.
        If key is record button, recording is started.
        '''
        
        if self.firstDown != -1: # Some key is already being held down
            return
        
        self.firstDown = event.GetKeyCode()
        
        if self.firstDown == wx.WXK_SPACE: # If key is record button, begin recording
            self.stopPlayback = True 
            self.env['SoundControl'].stopPlay()
            self.env['SoundControl'].startRecord()
            self.env['guiVisualizer'].recOn()
        
        

    def onKeyUp(self, event):
        '''
        Handles event when a key is released by calling the correct function for each valid key that was pressed
        down while no other keys were already down.
        '''
        
        keyCode = event.GetKeyCode()
        if self.firstDown != keyCode: # If released key is not the first one pressed, ignore it
            return
        
        self.firstDown = -1
        
        # Define dictionary of functions for valid keys
        keyFunctions = {wx.WXK_SPACE : self.recordingFinished, CTRL : self.playbackStory, 
                        wx.WXK_DOWN : self.getHelp, wx.WXK_UP: self.insertSound, 
                        wx.WXK_LEFT : self.navLeft, wx.WXK_RIGHT : self.navRight,
                        wx.WXK_HOME : self.jumpLeft, wx.WXK_END : self.jumpRight,
                        wx.WXK_ESCAPE : self.quit, DELETE_KEY : self.deleteClip,
                        wx.WXK_RETURN: self.insertBreak}
        
        if keyCode not in keyFunctions: # If key has no function, ignore it
            return      
        
        if self.deleteConfirmed and keyCode != DELETE_KEY: # If key is not the delete key, a delete is not being confirmed
            self.deleteConfirmed = False
            self.setInstructions()
        elif self.quitConfirmed and keyCode != wx.WXK_ESCAPE:#If key is not the escape key, quit is not being confirmed
            self.quitConfirmed = False
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
            self.env['guiVisualizer'].updateStats()



    def getHelp(self):
        '''
        Called when help key is released.  Reads the current instructions to user.
        '''
        
        self.env['SoundControl'].speakText(self.currInstr)
        
    
    def recordingFinished(self):
        '''
        Ends recording of clip and crops the beginning so that the click will not
        affect normalization.  If clip is longer than crop, inserts it into the story and replays it. Otherwise,
        notifies the user.  If story was previously empty (this is the title) post-title instructions are appended
        to the endof the replayed clip.
        '''
    
        crop = DEFAULT_CROP*RATE/44100
        
        soundBytes = self.env['SoundControl'].stopRecord() # End record and get recorded bytes
        
        if len(soundBytes) <= crop: # Space not hold
            self.env['SoundControl'].speakTextFile(INSTR_DIR + 'hold_space.txt')
            self.env['guiVisualizer'].recOff()
            return
            
        soundBytes = soundBytes[crop:] #Crops 
        soundBytes = normalizeSoundBytes(soundBytes)

        
        story = self.env['story']
        
        if story.needsTitle():
            story.replaceTitle(soundBytes)
            self.setInstructions()
        else:
            story.insertClip(soundBytes, type = REC)

        if len(story) == 1: # Title is only clip
            soundBytes += self.env['SoundControl'].speakTextFileToBytes(INSTR_DIR + 'after_title.txt')
            
        self.env['SoundControl'].playSoundBytes(soundBytes)
        self.env['guiVisualizer'].recOff() # Turns off red record light

        

    def playbackStory(self):
        '''
        Starts a thread to play back the entire story in order. If interrupted by a valid key, 
        thread returns and  current clip is the last to begin being played.  A separate thread is
        is used to allow this functionality.
        '''
        
        self.stopPlayback = False
        spb = StoryPlayback(self.env) 
        spb.start()
        

    def insertSound(self):
        '''
        Called when insert sound key is released. Passes control to the AuiInsertSound class 
        to allow user to insert a sound effect.
        '''
        
        self.env['auiInsertSound'].takeOver()
    
    def insertBreak(self):
        '''
        If in teacher mode, a break is inserted in the template.  When the template is assigned to 
        a student, clips between breaks will be combined into a single undeletable clip.
        '''
        
        if not self.teacherMode:
            return
        
        story = self.env['story']
        if story.clipIsBreak():
            self.env['SoundControl'].speakText('You may not have two breaks in a row.')
        else:
            story.insertClip(self.breakSoundBytes, type = BRK)
            self.env['SoundControl'].playSoundBytes(self.breakSoundBytes)
        

    def deleteClip(self):
        '''
        Called when delete key is released. If clip is locked, notifies user. If previous key pressed 
        was also the delete key, deletes the current clip. Otherwise, requests confirmation for delete.  
        If current clip is title, notifies user that a new title must be recorded before anything else 
        can be done.
        '''    

        story = self.env['story']
        if story.clipIsLocked():
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
                

    def navLeft(self):
        '''
        Moves to the previous clip in the story and plays it back.
        '''
        
        self.env['SoundControl'].playSoundBytes(self.env['story'].getPreviousClip())
    

    def navRight(self):
        '''Moves to the next clip in the story and plays it back.'''
        
        self.env['SoundControl'].playSoundBytes(self.env['story'].getNextClip())
        
    def jumpLeft(self):
        '''
        Moves to the title of the story and plays it back.
        '''
        
        self.env['story'].currClip = 0
        self.env['SoundControl'].playSoundBytes(self.env['story'].getCurrClip())
    
    def jumpRight(self):
        '''
        Moves to the last clip of the story and plays it back.
        '''
        
        self.env['story'].currClip = len(self.env['story']) - 1
        self.env['SoundControl'].playSoundBytes(self.env['story'].getCurrClip())
        
    def quit(self):
        ''' 
        Called when quit key is pressed.  If last key pressed was also quit key, plays wait sound 
        until all pickling threads have exited then returns to story selection. Otherwise requests
        confirmation.
        '''
        
        if self.quitConfirmed:
            self.env['SoundControl'].playSoundBytes(self.waitSound)
            while not self.env['story'].threadSem.acquire(False):
                pass
            self.env['story'].pickleMutex.acquire()
            self.env['SoundControl'].stopPlay()
            self.env['guiVisualizer'].Hide()
            self.env['guiStories'].Show()
            self.env['timer'].Stop()
        else:
            self.quitConfirmed = True
            self.setInstructions()
            self.getHelp()
        
        

class StoryPlayback(threading.Thread):
    '''
    This class is run as a separate thread. Its only function is to play back
    the entire story in order.  If any valid key is pressed during the playback,
    a flag is set by the StoryCreationAUI object that causes this thread to exit
    early.  Therefore, the current clip will remain the last clip that the thread
    began to play.  This class is run as a separate thread in order to facilitate
    this functionality.
    '''
    

    def __init__(self, env):
        '''
        Constructor receives global variables and initializes thread.
        '''
        self.env = env
        threading.Thread.__init__(self)
        
    

    def run(self):
        '''
        Called when thread is started.  Plays back each clip of the story in sequence and exits when
        either the stopPlayback flag is set to True or the last clip in the story has been played.
        '''
        
        story = self.env['story']
        story.currClip = -1
        
        while not self.env['auiStoryCreation'].stopPlayback and (story.currClip < len(story)-1):
            self.env['SoundControl'].playSoundBytes(story.getNextClip())
            self.env['guiVisualizer'].updateStats()
            while (self.env['SoundControl'].isPlaying()):
                pass
         