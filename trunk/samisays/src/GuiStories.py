#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Tue Feb 20 00:22:41 2007

import wx
import sys
import sets
import shutil
import os
from SoundControl import *
from Story import *
from AuiStoryCreation import *
from AuiStorySelection import *

ARTDIR = "art/"

class GuiStories(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiStories.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self)
        self.lstStories = wx.ListBox(self.panel, -1, choices=[])
        self.lstStories.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.btnSelect = wx.Button(self.panel, -1, "Open")
        self.btnSelect.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.btnCreate = wx.Button(self.panel, -1, "Write")
        self.btnCreate.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.btnRename = wx.Button(self.panel, -1, "Rename")
        self.btnRename.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.btnPlay = wx.Button(self.panel, -1, "Playback")
        self.btnPlay.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.btnPublishAssign = wx.Button(self.panel, -1, "Publish")
        self.btnPublishAssign.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.btnDelete = wx.Button(self.panel, -1, "Delete")
        self.btnDelete.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.btnBack = wx.Button(self.panel, wx.ID_CANCEL, "Back")
        self.btnBack.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.lblHead = wx.StaticText(self.panel,-1,"The Bookshelf")
        self.lblHead.SetFont(wx.Font(48,wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        # icons
        self.imgSelect = wx.Image(ARTDIR + "select.png", wx.BITMAP_TYPE_PNG)
	    #self.imgSelect = self.imgSelect.Scale(64,64,100) # resize to 3/4 of 128x128 at 100% quality
        self.picSelect = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.imgSelect))
        self.imgCreate = wx.Image(ARTDIR + "create.png", wx.BITMAP_TYPE_PNG)
        #self.imgCreate = self.imgCreate.Scale(64,64,100)
        self.picCreate = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.imgCreate))
        self.imgRename = wx.Image(ARTDIR + "rename.png", wx.BITMAP_TYPE_PNG)
        #self.imgRename = self.imgRename.Scale(64,64,100)
        self.picRename = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.imgRename))
        self.imgDelete = wx.Image(ARTDIR + "delete.png", wx.BITMAP_TYPE_PNG)
	    #self.imgDelete = self.imgDelete.Scale(64,64,100)
        self.picDelete = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.imgDelete))
        self.imgPlay = wx.Image(ARTDIR + "play.png", wx.BITMAP_TYPE_PNG)
	    #self.imgPlay = self.imgPlay.Scale(64,64,100)
        self.picPlay = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.imgPlay))
        self.imgPublish = wx.Image(ARTDIR + "publish.png", wx.BITMAP_TYPE_PNG)
	    #self.imgPublish = self.imgPublish.Scale(64,64,100)
        self.picPublish = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.imgPublish))
        self.imgBack = wx.Image(ARTDIR + "back2.png", wx.BITMAP_TYPE_PNG)
	    #self.imgBack = self.imgBack.Scale(64,64,100)
        self.picBack = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.imgBack))


        self.__set_properties()
        self.__do_layout()
        


        self.Bind(wx.EVT_LISTBOX_DCLICK, self.lstStoriesDblClick, self.lstStories)
        self.Bind(wx.EVT_LISTBOX, self.lstStoriesSelected, self.lstStories)
        self.Bind(wx.EVT_BUTTON, self.btnSelectPressed, self.btnSelect)
        self.Bind(wx.EVT_BUTTON, self.btnCreatePressed, self.btnCreate)
        self.Bind(wx.EVT_BUTTON, self.btnRenamePressed, self.btnRename)
        self.Bind(wx.EVT_BUTTON, self.btnDeletePressed, self.btnDelete)
        self.Bind(wx.EVT_BUTTON, self.btnPlayPressed, self.btnPlay)
        self.Bind(wx.EVT_BUTTON, self.btnPublishAssignPressed, self.btnPublishAssign)
        self.Bind(wx.EVT_BUTTON, self.btnBackPressed, self.btnBack)
        self.Bind(wx.EVT_SHOW, self.handleShow, self)
        self.Bind(wx.EVT_KILL_FOCUS, self.handleFocus, self)
        
        # Added By Patrick
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.env = {}
        self.visible = False
        
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
        szrChildButtons = wx.FlexGridSizer(19, 2, 0, 0)
        szrParent.Add(self.lblHead,0,wx.ALIGN_CENTRE, 0)
        szrParent.AddSpacer(10)
        szrChildList.AddSpacer(30)
        szrChildList.Add(self.lstStories, 1, wx.EXPAND, 0)
        szrChildList.AddSpacer(30)
        szrChildButtons.Add(self.picSelect, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnSelect, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.picCreate, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnCreate, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.picRename, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnRename, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.picPlay, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnPlay, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.picPublish, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnPublishAssign, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.picDelete, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnDelete, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.picBack, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnBack, 1, wx.EXPAND, 0)
        szrChildButtons.AddGrowableRow(0)
        szrChildButtons.AddGrowableRow(2)
        szrChildButtons.AddGrowableRow(4)
        szrChildButtons.AddGrowableRow(6)
        szrChildButtons.AddGrowableRow(8)
        szrChildButtons.AddGrowableRow(10)
        szrChildButtons.AddGrowableRow(12)
        #szrChildButtons.AddGrowableCol(0)
        szrChildButtons.AddGrowableCol(1)
        szrChildList.Add(szrChildButtons, 1, wx.EXPAND, 0)
        szrChildList.AddSpacer(30)
        szrChildList.AddGrowableRow(0)
        szrChildList.AddGrowableCol(1)
        szrChildList.AddGrowableCol(3)
        szrParent.Add(szrChildList, 1, wx.EXPAND, 0)
        szrParent.AddSpacer(70)
        self.panel.SetAutoLayout(True)
        self.panel.SetSizer(szrParent)
        szrParent.AddGrowableRow(2)
        szrParent.AddGrowableCol(0)
        #szrParent.AddGrowableRow(3)
        self.panel.Layout()
        # end wxGlade

                
    def lstStoriesSelected(self, event):
        self.loadStory();
        self.env['auiStorySelection'].playTitle()
        
    def lstStoriesDblClick(self, event): # wxGlade: guiStories.<event_handler>
        self.loadStory();
        self.openStory()

    def btnSelectPressed(self, event): # wxGlade: guiStories.<event_handler>
        if not self.somethingSelected():
            return
        self.loadStory();
        self.openStory()

    def btnCreatePressed(self, event): # wxGlade: guiStories.<event_handler>
        self.newStory()

    def btnRenamePressed(self, event): # wxGlade: guiStories.<event_handler>
        self.env['SoundControl'].stopPlay()
        if not self.somethingSelected():
            return
        
        dialog = wx.TextEntryDialog(None,'Please enter the story\'s new name:','Sami Says','')
        if dialog.ShowModal() == wx.ID_OK:
            newName = dialog.GetValue()
            if(newName != ''):
                self.env['story'].name = newName
                self.env['story'].pickleMe()
                storyPath = STUDENT_DIR + '/_' + self.env['student'].getName() + '/'
                os.remove(storyPath + self.env['student'].stories[self.lstStories.GetSelection()] + '.pkl')
                self.populateList()
                self.lstStories.Select(self.findListItem(newName))
        else:
            dialog.Destroy()

    def btnDeletePressed(self, event): # wxGlade: guiStories.<event_handler>
        self.env['SoundControl'].stopPlay()
        if not self.somethingSelected():
            return
        
        dialog = wx.MessageDialog(None,'Are you sure you want to delete ' + self.env['student'].stories[self.lstStories.GetSelection()]+ '?','Sami Says',wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            selection = self.lstStories.GetSelection()
            self.deleteStory(selection)
            if len(self.env['student'].stories) != 0:
                self.lstStories.SetSelection(max(selection-1,0))
                self.loadStory()
                self.env['auiStorySelect'].playTitle()
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

    def loadStory(self):
        storyName = self.env['student'].stories[self.lstStories.GetSelection()]
        studentName = self.env['student'].getName()
        self.env['story'] = unpickleStory(storyName, studentName)
        self.env['story'].currClip = 0
        
    def newStory(self):
        storyName = '_'.join([str(time.localtime()[i]) for i in xrange(6)])
        studentName = self.env['student'].getName()
        self.env['story'] = Story(storyName, studentName)
        self.openStory()
   
    def openStory(self):
        self.env['SoundControl'].stopPlay()
        self.env['auiStoryCreation'].takeOver()
        self.env['guiWorking'].Show()
        self.env['guiWorking'].SetFocus()
        self.env['timer'].Start(100)
        self.env['guiStories'].Hide()
    
    def deleteStory(self):
        
        selection = self.lstStories.GetSelection()
        studentName = self.env['student'].getName()
        storyName = self.env['student'].stories[selection]
        os.remove(STUDENT_DIR + '/_' + studentName + '/' + storyName + '.pkl')
        self.populateList()
        
    def publishStory(self):

        dialog = wx.FileDialog(None,'Please select a filename to exort.','',self.env['story'].name,'*.mp3',wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            dialog.Destroy()
            encodeToMp3(self.env['story'].getStoryBytes(),dialog.GetPath(),64000)
        else:
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
    
    def lock(self):
        print 'lock'
        self.SetFocus()
        self.env['auiStorySelection'].takeOver()
        self.env['storiesLock'] = True
        
    def unlock(self):
        print 'unlock'
        self.env['storiesLock'] = False
        self.btnSelect.SetFocus()

        
    def handleFocus(self, event):
        if self.env['storiesLock']:
            self.SetFocus()
            
    def handleShow(self, event):
        self.populateList()
        if not self.visible:
            self.lock()
            self.visible = True
        else:
            self.visible = False
    
    def somethingSelected(self):
        if self.lstStories.GetSelection() == -1:
            msgDialog = wx.MessageDialog(self, 'You must highlight a story before using this function.', 'Error: No Story Selected', wx.ICON_ERROR)
            msgDialog.ShowModal()
            msgDialog.Destroy()
            return False
        return True
    
    def onKeyDown(self, event):
        CTRL = 308 # keyCode for CTRL
        
        keyCode = event.GetKeyCode()
        
        self.allDowns.union_update([keyCode])
        
        print self.allDowns
        
        if (self.lockStarted and len(self.allDowns) == 3 
            and CTRL in self.allDowns 
            and wx.WXK_TAB in self.allDowns
            and wx.WXK_SHIFT in self.allDowns):
            self.doLock = True
            
        if not (keyCode == CTRL or keyCode == wx.WXK_TAB or keyCode == wx.WXK_SHIFT):
            self.lockStarted = False
            
        if (len(self.allDowns) == 1 
            and (keyCode == CTRL or keyCode == wx.WXK_TAB or keyCode == wx.WXK_SHIFT)):
            self.lockStarted = True
            
        event.Skip()
        
    def onKeyUp(self, event):
        keyCode = event.GetKeyCode()
        
        self.allDowns.remove(keyCode)
        
        if self.doLock:
            if len(self.allDowns) == 0:
                self.lock()
                self.doLock = False
        else:
            event.Skip()
        
        
# end of class guiStories


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frmMain = GuiStories(None, -1, "")
    app.SetTopWindow(frmMain)
    frmMain.Show()
    app.MainLoop()
