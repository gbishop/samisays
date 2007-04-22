''' Imports '''
import wx
import sys
import sets
import shutil
import os
from SoundControl import *
from Story import *
from AuiStoryCreation import *
from AuiStorySelection import *
from Constants import *

'''
' Class Name: GuiStories
' Description: A subclass of the wx Frame class. It is displayed when a student is
'              selected and has a locked and unlocked mode. All buttons are available
'              in unlocked mode, whereas only the unlock button is available in locked
'              mode.
'''
class GuiStories(wx.Frame):
    
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, -1)
        self.lstStories = wx.ListBox(self.panel, -1, choices=[])
        self.lstStories.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnSelect = wx.Button(self.panel, -1, "Open")
        self.btnSelect.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnCreate = wx.Button(self.panel, -1, "Write")
        self.btnCreate.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnRename = wx.Button(self.panel, -1, "Rename")
        self.btnRename.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnPlay = wx.Button(self.panel, -1, "Playback")
        self.btnPlay.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnPublishAssign = wx.Button(self.panel, -1, "Publish")
        self.btnPublishAssign.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnDelete = wx.Button(self.panel, -1, "Delete")
        self.btnDelete.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnBack = wx.Button(self.panel, wx.ID_CANCEL, "Back")
        self.btnBack.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.lblHead = wx.StaticText(self.panel,-1,"The Bookshelf")
        self.lblHead.SetFont(wx.Font(48,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnLock = wx.Button(self.panel,-1,"Lock")
        self.btnLock.SetSize((200,50))


        self.__set_properties()
        self.__do_layout()
        
        objects = [self.panel, self.lstStories, self.btnSelect, self.btnCreate, 
                   self.btnRename, self.btnPlay, self.btnPublishAssign, self.btnDelete,
                   self.btnLock, self.lblHead]
        for obj in objects:
            obj.Bind(wx.EVT_KEY_UP, self.onKeyUp)
            obj.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
            
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.lstStoriesDblClick, self.lstStories)
        self.Bind(wx.EVT_LISTBOX, self.lstStoriesSelected, self.lstStories)
        self.Bind(wx.EVT_BUTTON, self.btnSelectPressed, self.btnSelect)
        self.Bind(wx.EVT_BUTTON, self.btnCreatePressed, self.btnCreate)
        self.Bind(wx.EVT_BUTTON, self.btnRenamePressed, self.btnRename)
        self.Bind(wx.EVT_BUTTON, self.btnDeletePressed, self.btnDelete)
        self.Bind(wx.EVT_BUTTON, self.btnPlayPressed, self.btnPlay)
        self.Bind(wx.EVT_BUTTON, self.btnPublishAssignPressed, self.btnPublishAssign)
        self.Bind(wx.EVT_BUTTON, self.btnBackPressed, self.btnBack)
        self.Bind(wx.EVT_BUTTON, self.btnLockPressed, self.btnLock)
        self.Bind(wx.EVT_SHOW, self.handleShow, self)
        self.Bind(wx.EVT_KILL_FOCUS, self.handleFocus, self)
        
        # Added By Patrick
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.env = {}
        self.visible = False
        
        # Necessary for locking
        self.firstDown = -1
        self.allDowns = sets.Set([])
        self.lockStarted = False
        self.doLock = False
    
    def __set_properties(self):
        # begin wxGlade: guiStories.__set_properties
        self.SetTitle("Sami Says")
        self.SetPosition((0,0))
        self.SetSize(wx.DisplaySize())
        self.btnSelect.SetDefault()
        self.btnSelect.SetFocus()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiStories.__do_layout
        szrParent = wx.FlexGridSizer(4, 1, 0, 0)
        szrChildList = wx.FlexGridSizer(1, 6, 0, 0)
        szrChildButtons = wx.FlexGridSizer(13, 1, 0, 0)
        szrTitle = wx.BoxSizer(wx.HORIZONTAL)
        szrTitle.Add(self.lblHead,1,wx.EXPAND,0)
        #szrTitle.AddSpacer(10)
        #szrTitle.Add(self.btnLock,0,wx.ALIGN_RIGHT,0)
        szrParent.Add(szrTitle,1,wx.ALIGN_CENTER, 0)
        szrParent.AddSpacer(10)
        szrChildList.AddSpacer(30)
        szrChildList.Add(self.lstStories, 1, wx.EXPAND, 0)
        szrChildList.AddSpacer(30)
        szrChildButtons.Add(self.btnSelect, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnCreate, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnRename, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnPlay, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnPublishAssign, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnDelete, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnBack, 1, wx.EXPAND, 0)
        szrChildButtons.AddGrowableRow(0)
        szrChildButtons.AddGrowableRow(2)
        szrChildButtons.AddGrowableRow(4)
        szrChildButtons.AddGrowableRow(6)
        szrChildButtons.AddGrowableRow(8)
        szrChildButtons.AddGrowableRow(10)
        szrChildButtons.AddGrowableRow(12)
        szrChildButtons.AddGrowableCol(0)
        szrChildList.Add(szrChildButtons, 1, wx.EXPAND, 0)
        szrChildList.AddSpacer(30)
        szrChildList.AddGrowableRow(0)
        szrChildList.AddGrowableCol(1)
        szrChildList.AddGrowableCol(3)
        szrParent.Add(szrChildList, 1, wx.EXPAND, 0)
        szrParent.AddSpacer(70)
        szrParent.AddGrowableRow(2)
        szrParent.AddGrowableCol(0)
        self.panel.SetAutoLayout(True)
        self.panel.SetSizer(szrParent)
        self.panel.Layout()
        self.Layout()
        # end wxGlade

                
    def lstStoriesSelected(self, event):
        self.loadTitle();
        self.env['auiStorySelection'].playTitle()
        
    def lstStoriesDblClick(self, event): # wxGlade: guiStories.<event_handler>
        storyName = self.env['student'].stories[self.lstStories.GetSelection()]
        studentName = self.env['student'].getName()
        self.env['auiStoryCreation'].loadFullStory()
        self.openStory()

    def btnSelectPressed(self, event): # wxGlade: guiStories.<event_handler>
        if not self.somethingSelected():
            return
        self.openStory()

    def btnLockPressed(self, event):
        if self.env['storiesLock']:
            self.unlock()
        else:
            self.lock()

    def btnCreatePressed(self, event): # wxGlade: guiStories.<event_handler>
        self.newStory()

    def btnRenamePressed(self, event): # wxGlade: guiStories.<event_handler>
        self.env['SoundControl'].stopPlay()
        if not self.somethingSelected():
            return
        
        dialog = wx.TextEntryDialog(None,'Please enter the story\'s new name:','Sami Says','')
        if dialog.ShowModal() == wx.ID_OK:
            newName = dialog.GetValue()
            studentName = self.env['student'].getName()
            if os.path.exists('%s_%s/%s.pkl' % (STUDENT_DIR, studentName, newName)):
                msg = '%s already has a story by this name.  Try a different name.' % (studentName)
                msgDialog = wx.MessageDialog(self, msg, 'Error: Story Already Exists', wx.ICON_ERROR)
                msgDialog.ShowModal()
                msgDialog.Destroy()
                self.btnRenamePressed(False)
            elif(newName != ''):
                self.env['auiStoryCreation'].loadFullStory()
                oldName = self.env['story'].name
                self.env['story'].name = newName
                self.env['story'].pickleMe(True)
                self.env['story'].pickleTitle()
                oldPath = '%s_%s/%s' % (STUDENT_DIR, studentName, oldName)
                os.remove(oldPath + '.pkl')
                os.remove(oldPath + '.ttl')
                self.populateList()
                self.lstStories.Select(self.findListItem(newName))
                
        dialog.Destroy()

    def btnDeletePressed(self, event): # wxGlade: guiStories.<event_handler>
        self.env['SoundControl'].stopPlay()
        if not self.somethingSelected():
            return
        
        dialog = wx.MessageDialog(None,'Are you sure you want to delete ' + self.env['student'].stories[self.lstStories.GetSelection()]+ '?','Sami Says',wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            selection = self.lstStories.GetSelection()
            self.deleteStory()
            if len(self.env['student'].stories) != 0:
                self.lstStories.SetSelection(max(selection-1,0))
                self.loadTitle()
                self.env['auiStorySelection'].playTitle()
        dialog.Destroy()

    def btnPlayPressed(self, event): # wxGlade: guiStories.<event_handler>
        if not self.somethingSelected():
            return
        self.env['auiStorySelection'].playStory()

    def btnPublishAssignPressed(self, event): # wxGlade: guiStories.<event_handler>
        self.env['SoundControl'].stopPlay()
        if not self.somethingSelected():
            return
            
        if self.env['student'] == self.env['class'].teacher:
            self.Enable(False)
            self.env['guiAssign'].Show()
        else:
            self.publishStory()
    


    def btnBackPressed(self, event): # wxGlade: guiStories.<event_handler>
        self.env['SoundControl'].stopPlay()
        self.Hide()
        if self.env['student'] == self.env['class'].teacher:
            self.env['guiStart'].Show()
        else:
            self.env['guiStudents'].Show()
    
    def setEnv(self,env): 
        self.env = env 
        
    def setStudent(self, index):
        
        if index == -2:
            self.env['student'] = self.env['class'].teacher
            self.lblHead.SetLabel('Teacher Templates')
            self.btnPublishAssign.SetLabel('Assign')
        else:
            self.env['student'] = self.env['class'].students[index]
            self.lblHead.SetLabel(self.env['student'].getName() + '\'s StoryBook')
            self.btnPublishAssign.SetLabel('Publish')
            
    def onClose(self, event):
        dialog = wx.MessageDialog(None,'Are you sure you want to leave?','Sami Says',wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            sys.exit()
        else:
            dialog.Destroy()
   
        
    def populateList(self):
        self.lstStories.Clear()
        self.env['student'].loadNames('students/_' + self.env['student'].getName())
        count = 0;
        for i in self.env['student'].stories:
            self.lstStories.Insert(i,count)
            count+=1
        if(self.lstStories.GetCount() > 0):
            self.btnSelect.Enable()
        else:
            self.btnSelect.Enable(False)
                  
    def loadTitle(self):
        storyName = self.env['student'].stories[self.lstStories.GetSelection()]
        studentName = self.env['student'].getName()
        self.env['story'] = unpickleTitle(storyName, studentName)
        self.env['story'].currClip = 0

        
    def newStory(self):
        storyName = '_'.join([str(time.localtime()[i]) for i in xrange(6)])
        studentName = self.env['student'].getName()
        self.env['story'] = Story(storyName, studentName)
        self.env['story'].initializeLocks()
        self.openStory()
   
    def openStory(self):
        self.env['SoundControl'].stopPlay()
        self.env['auiStoryCreation'].loadFullStory()
        self.env['auiStoryCreation'].takeOver()
        self.env['guiWorking'].Show()
        self.env['guiWorking'].SetFocus()
        self.env['timer'].Start(100)
        self.env['guiStories'].Hide()
    
    def deleteStory(self):
        selection = self.getSelection()
        studentName = self.env['student'].getName()
        storyName = self.env['student'].stories[selection]
        os.remove(STUDENT_DIR + '/_' + studentName + '/' + storyName + '.pkl')
        os.remove(STUDENT_DIR + '/_' + studentName + '/' + storyName + '.ttl')
        self.populateList()
        
    def publishStory(self):

        dialog = wx.FileDialog(None,'Please select a filename to export.','',self.env['story'].name,'*.mp3',wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.env['auiStoryCreation'].loadFullStory()
            encodeToMp3(self.env['story'].getStoryBytes(),dialog.GetPath())
        dialog.Destroy()   
    
    ''' Helper function for finding an the index of a story '''
    def findListItem(self, name):
        count = 0
        for i in self.env['student'].stories:
            if (self.env['student'].stories[count] == name):
                return count
            else:
                count += 1
        return 0
    
    def getSelection(self):
        return self.lstStories.GetSelection()
    
    def lock(self):
        self.SetFocus()
        self.btnLock.SetLabel('Unlock with CTRL-SHIFT-TAB')
        self.env['auiStorySelection'].takeOver()
        self.env['storiesLock'] = True
        
    def unlock(self):
        self.btnLock.SetLabel('Lock')
        self.env['storiesLock'] = False
        if self.btnSelect.IsEnabled():
            self.btnSelect.SetFocus()
        else:
            self.btnCreate.SetFocus()

        
    def handleFocus(self, event):
        if self.env['storiesLock']:
            if self.btnLock.HasCapture():
                self.btnLockPressed(None)
            else:
                self.SetFocus()
            
            
    def handleShow(self, event):
        self.populateList()
        if not self.visible: # Show() called
            if self.env['storiesLock']:
                self.lock()
            else:
                self.unlock()
            self.visible = True
        else: # Hide() called
            self.visible = False
    
    def somethingSelected(self):
        if self.lstStories.GetSelection() == -1:
            msgDialog = wx.MessageDialog(self, 'You must highlight a story before using this function.', 'Error: No Story Selected', wx.ICON_ERROR)
            msgDialog.ShowModal()
            msgDialog.Destroy()
            return False
        return True
    
    def onKeyDown(self, event):

        keyCode = event.GetKeyCode()
        
        if not (keyCode in LOCK_KEYS_NO_TAB or keyCode == wx.WXK_ESCAPE):
            event.Skip()
            
        self.allDowns.union_update([keyCode])
        
        if (self.firstDown in LOCK_KEYS_NO_TAB and self.allDowns == LOCK_KEYS_NO_TAB):
            self.lockStarted = True
                  
        if self.firstDown == -1:       
            self.lockStarted = False
            self.doLock = False
            self.firstDown = keyCode
        event.Skip()
        
    def onKeyUp(self, event):
        
        keyCode = event.GetKeyCode()
        
        if keyCode == wx.WXK_TAB and self.lockStarted:
            self.lockStarted = False
            self.doLock = True    
        elif keyCode in LOCK_KEYS_NO_TAB or keyCode == wx.WXK_ESCAPE:
            self.allDowns.remove(keyCode)
        else: 
            event.Skip()
        
        if len(self.allDowns) == 0 and self.doLock:
            self.doLock = False
            self.lock()
        
        if keyCode == self.firstDown:
            self.firstDown = -1
            if keyCode == wx.WXK_ESCAPE:
                self.btnBackPressed(False)
        event.Skip()
        
            
''' Handling an attempt at standalone running '''
if __name__ == "__main__":
    print 'The class "GuiStories" is not runnable.'
