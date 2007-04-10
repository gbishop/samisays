import wx
import sets
from SoundControl import *
from Story import *

INSTR_DIR = 'instr_text/'

class AuiStorySelection:
	
	def __init__(self, env):
		self.env = env

	def takeOver(self):
		welcomeTest = file(INSTR_DIR + 'selection_welcome.txt').read()
		self.env['SoundControl'].speakText(welcomeTest % self.env['student'].getName()) # Play Welcome
		
		self.storyIndex = -1
		self.env['guiStories'].lstStories.SetSelection(self.storyIndex)
		self.numStories = len(self.env['student'].stories)
		
		self.unlock = False
		self.unlockStarted = False
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
		
		if (self.unlockStarted and len(self.allDowns) == 3 
			and CTRL in self.allDowns 
			and wx.WXK_TAB in self.allDowns
			and wx.WXK_SHIFT in self.allDowns):
			self.unlock = True
			
		if not (keyCode == CTRL or keyCode == wx.WXK_TAB or keyCode == wx.WXK_SHIFT):
			self.unlockStarted = False
			
		if self.firstDown != -1:
			return
		
		if keyCode == CTRL or keyCode == wx.WXK_TAB or keyCode == wx.WXK_SHIFT:
			self.unlockStarted = True
			
		self.firstDown = keyCode

		
	''' 
	' Handles event when a key is released by calling the correct function for 
	' each valid key.
	'''
	def onKeyUp(self, event):
		
		CTRL = 308 # keyCode for CTRL
		
		keyCode = event.GetKeyCode()
		
		self.allDowns.remove(keyCode)
		
		if self.unlock:
			if len(self.allDowns) == 0:
				self.env['guiStories'].unlock()
				self.unlock = False
			return
		
		if self.firstDown != keyCode:
			return

		self.firstDown = -1
		
		# Define dictionary of functions for valid keys
		keyFunctions = {wx.WXK_RIGHT : self.goRight,
						wx.WXK_LEFT : self.goLeft, wx.WXK_SPACE : self.selectStory,
						CTRL : self.playStory, #wx.WXK_ESCAPE : self.exit,
						wx.WXK_DOWN : self.newStory, wx.WXK_UP : self.deleteStory}
		
		if keyCode not in  keyFunctions: # If key has no function, ignore it
			return
		
		if self.numStories == 0 and not (keyCode == wx.WXK_DOWN or keyCode == wx.WXK_ESCAPE):
			self.env['SoundControl'].speakTextFile(INSTR_DIR + 'no_stories.txt')
			return

		if keyCode != wx.WXK_UP: # If key is not the delete key, a delete is not being confirmed
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
		self.storyIndex = self.env['guiStories'].lstStories.GetSelection()
		if self.storyIndex == -1:
			self.env['SoundControl'].speakTextFile(INSTR_DIR + 'no_story_selected.txt')
		else:
			if self.env['story'].justTitle:
				self.env['guiStories'].loadFullStory()
			storyBytes = self.env['story'].getStoryBytes()
			self.env['SoundControl'].playSoundBytes(storyBytes)
		
	def exit(self):
		self.env['guiStories'].btnBackPressed(None)
		self.env['guiStories'].unlock()
		self.unlock = False
		
	def newStory(self):
		self.env['guiStories'].btnCreatePressed(None)