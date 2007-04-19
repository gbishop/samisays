import wx
import sets
from SoundControl import *
from Story import *

INSTR_DIR = 'instr_text/'
CTRL = 308 # keyCode for CTRL
LOCK_KEYS = sets.Set([CTRL, wx.WXK_SHIFT, wx.WXK_TAB])
DELETE_KEY = wx.WXK_BACK
NEW_KEY = wx.WXK_SPACE

class AuiStorySelection:
	
	def __init__(self, env):
		self.env = env

	def takeOver(self):
		welcomeText = file(INSTR_DIR + 'selection_welcome.txt').read()
		self.env['SoundControl'].speakText(welcomeText % self.env['student'].getName()) # Play Welcome
		
		self.storyIndex = -1
		self.env['guiStories'].lstStories.SetSelection(self.storyIndex)
		self.numStories = len(self.env['student'].stories)
		
		self.doUnlock = False
		self.firstDown = -1
		self.allDowns = sets.Set([])
		self.deleteConfirmed = False
		
		self.env['keyUpFunct'] = self.onKeyUp
		self.env['keyDownFunct'] = self.onKeyDown
		
	''' 
	' Handles event when a key is pressed. 
	'''
	def onKeyDown(self, event):
		CTRL = 308 # keyCode for CTRL
		keyCode = event.GetKeyCode()
		
		self.allDowns.union_update([keyCode])
		
		if (self.firstDown in LOCK_KEYS and self.allDowns == LOCK_KEYS):
			self.doUnlock = True
			
		if self.firstDown != -1:
			return
			
		self.doUnlock = False
		self.firstDown = keyCode

		
	''' 
	' Handles event when a key is released by calling the correct function for 
	' each valid key.
	'''
	def onKeyUp(self, event):
		
		keyCode = event.GetKeyCode()
		
		#if len(self.allDowns) > 0:
		self.allDowns.remove(keyCode)
		
		if len(self.allDowns) == 0 and self.doUnlock:
			self.env['guiStories'].unlock()
			self.doUnlock = False
		
		if self.firstDown != keyCode:
			return
		
		self.firstDown = -1
		
		# Define dictionary of functions for valid keys
		keyFunctions = {wx.WXK_RIGHT : self.goRight, wx.WXK_LEFT : self.goLeft, 
					    NEW_KEY : self.newStory, CTRL : self.playStory,
						wx.WXK_DOWN : self.getHelp, wx.WXK_UP : self.selectStory,
						DELETE_KEY : self.deleteStory}
		
		if keyCode not in  keyFunctions: # If key has no function, ignore it
			return
		
		if self.numStories == 0 and not keyCode in [NEW_KEY, wx.WXK_ESCAPE]:
			self.env['SoundControl'].speakTextFile(INSTR_DIR + 'no_stories.txt')
			return

		if keyCode != DELETE_KEY: # If key is not the delete key, a delete is not being confirmed
			self.deleteConfirmed = False

		
		self.env['SoundControl'].stopPlay()
		keyFunctions[keyCode]()
		
	'''
	' Called when delete key is released.
	' If previous key pressed was also the delete key, deletes the current story. Otherwise,
	' requests confirmation for delete.
	'''	
	def deleteStory(self):
		if self.storyIndex == -1:
		   self.env['SoundControl'].speakTextFile(INSTR_DIR + 'no_story_selected.txt')
		   return
		
		if self.deleteConfirmed:
			self.env['guiStories'].deleteStory()
			self.numStories -= 1
			if self.numStories == 0:
				self.storyIndex = -1
			else:
				self.storyIndex = (self.storyIndex - 1) % self.numStories
				self.env['guiStories'].lstStories.SetSelection(self.storyIndex)
				self.env['guiStories'].loadTitle()
				self.playTitle()
			self.deleteConfirmed = False
		else:
			self.env['SoundControl'].speakTextFile(INSTR_DIR + 'delete_confirm.txt')
			self.deleteConfirmed = True

			
	def goRight(self):
		
		self.storyIndex = (self.storyIndex + 1) % self.numStories
		
		self.env['guiStories'].lstStories.SetSelection(self.storyIndex)
		self.env['guiStories'].loadTitle();
		self.playTitle()
	
	def goLeft(self):
		
		if self.storyIndex == -1:
			self.storyIndex = self.numStories-1
		else:
			self.storyIndex = (self.storyIndex - 1) % self.numStories
		
		self.env['guiStories'].lstStories.SetSelection(self.storyIndex)
		self.env['guiStories'].loadTitle();
		self.playTitle()
	
	def selectStory(self):
		if self.storyIndex == -1:
			self.env['SoundControl'].speakTextFile(INSTR_DIR + 'no_story_selected.txt')
		else:
			self.env['guiStories'].btnSelectPressed(None)
	
	def playTitle(self):
		self.env['SoundControl'].stopPlay()
		titleBytes = self.env['story'].getTitleBytes()
		self.env['SoundControl'].playSoundBytes(titleBytes)
	
	def playStory(self):
		self.env['SoundControl'].stopPlay()
		if self.env['guiStories'].getSelection() == -1:
			self.env['SoundControl'].speakTextFile(INSTR_DIR + 'no_story_selected.txt')
		else:
			self.env['auiStoryCreation'].loadFullStory()
			storyBytes = self.env['story'].getStoryBytes()
			self.env['SoundControl'].playSoundBytes(storyBytes)
			
	def newStory(self):
		self.env['guiStories'].btnCreatePressed(None)
		
	def getHelp(self):
		self.env['SoundControl'].speakTextFile(INSTR_DIR + 'selection_instructions.txt')
		
	def exit(self):
		self.env['guiStories'].btnBackPressed(None)
		self.env['guiStories'].unlock()
		self.unlock = False
	