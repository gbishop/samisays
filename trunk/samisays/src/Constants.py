''' 
'   This file is for holding constants. Any repeated constants are eliminated in the
'   subsequent sections.
''' 

''' Imports '''
import wx
import sets

''' AuiInsertSound '''
INSTR_DIR = 'instr_text/'
CAT_MODE = 0
SND_MODE = 1

''' AuiStoryCreation '''
SYS_SOUND_DIR = 'sys_sounds/'
BREAK_SOUND = SYS_SOUND_DIR + 'lilbeep.wav'
INTRO_SOUND = SYS_SOUND_DIR + 'xylophone_intro.mp3'
WAIT_SOUND = SYS_SOUND_DIR + 'wait_noise.mp3'
DEFAULT_CROP = 5000
DELETE_KEY = wx.WXK_BACK
CTRL = 308 # keyCode for CTRL

''' AuiStorySelection '''
LOCK_KEYS = sets.Set([CTRL, wx.WXK_SHIFT, wx.WXK_TAB])
NEW_KEY = wx.WXK_SPACE

''' Class '''
STUDENT_DIR = 'students/'
BACKUP_DIR = STUDENT_DIR + 'removed/'

''' ConvertSounds '''
SOUND_DIR = 'sound_library/'

''' GuiStart '''
BIG_FONT = None
NORMAL_FONT = None

''' GuiStories '''
ARTDIR = "art/"
LOCK_KEYS_NO_TAB = sets.Set([CTRL, wx.WXK_SHIFT]) # TAB is also included but is handled separately
                                                  # due to wx quirk

''' SoundControl '''
RATE = 16000    # samples per second
BITS = 16       # BITS per sample
CHANNELS = 1    # 1 is mono, 2 is stereo
BUFF_DURATION = 1 # in seconds
TTS_RATE = 44000
MP3_RATE = 6400

''' SoundLibrary '''
SOUND_LIB_DIR  = 'sound_library/'
SFX_CAT = -2

''' Story '''
NON = 0
REC = 1
SFX = 2
SND = 3
LCK = 4
BRK = 5
COMPRESS_RATE = 9                                      