#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Tue Feb 20 00:22:41 2007

import wx
import sys

class GuiStories(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiStories.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self)
        self.lstStories = wx.ListBox(self.panel, -1, choices=[])
        self.lstStories.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnSelect = wx.Button(self.panel, -1, "Select")
        self.btnSelect.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnCreate = wx.Button(self.panel, -1, "Create")
        self.btnCreate.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnRename = wx.Button(self.panel, -1, "Rename")
        self.btnRename.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnDelete = wx.Button(self.panel, -1, "Delete")
        self.btnDelete.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnPlay = wx.Button(self.panel, -1, "Play")
        self.btnPlay.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnPublish = wx.Button(self.panel, -1, "Publish")
        self.btnPublish.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnBack = wx.Button(self.panel, -1, "Back")
        self.btnBack.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.lstStoriesDblClick, self.lstStories)
        self.Bind(wx.EVT_BUTTON, self.btnSelectPressed, self.btnSelect)
        self.Bind(wx.EVT_BUTTON, self.btnCreatePressed, self.btnCreate)
        self.Bind(wx.EVT_BUTTON, self.btnRenamePressed, self.btnRename)
        self.Bind(wx.EVT_BUTTON, self.btnDeletePressed, self.btnDelete)
        self.Bind(wx.EVT_BUTTON, self.btnPlayPressed, self.btnPlay)
        self.Bind(wx.EVT_BUTTON, self.btnPublishPressed, self.btnPublish)
        self.Bind(wx.EVT_BUTTON, self.btnBackPressed, self.btnBack)
        
        # Added By Patrick
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.env = {}

    def __set_properties(self):
        # begin wxGlade: guiStories.__set_properties
        self.SetTitle("Sami's Stories")
        self.SetPosition((0,0))
        self.SetSize(wx.DisplaySize())
        self.btnSelect.SetDefault()
        self.btnSelect.SetFocus()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiStories.__do_layout
        szrParent = wx.FlexGridSizer(3, 1, 0, 0)
        szrChildList = wx.FlexGridSizer(1, 6, 0, 0)
        szrChildButtons = wx.FlexGridSizer(13, 1, 0, 0)
        szrParent.AddSpacer(20)
        szrChildList.AddSpacer(30)
        szrChildList.Add(self.lstStories, 1, wx.EXPAND, 0)
        szrChildList.AddSpacer(10)
        szrChildButtons.Add(self.btnSelect, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnCreate, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnRename, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnDelete, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnPlay, 1, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(10)
        szrChildButtons.Add(self.btnPublish, 1, wx.EXPAND, 0)
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
        szrParent.AddSpacer(20)
        self.panel.SetAutoLayout(True)
        self.panel.SetSizer(szrParent)
        szrParent.AddGrowableRow(1)
        szrParent.AddGrowableCol(0)
        self.panel.Layout()
        # end wxGlade

    def lstStoriesDblClick(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `lstStoriesDblClick' not implemented!"
        event.Skip()

    def btnSelectPressed(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `btnSelectPressed' not implemented!"
        event.Skip()

    def btnCreatePressed(self, event): # wxGlade: guiStories.<event_handler>
        print 'create not done'

    def btnRenamePressed(self, event): # wxGlade: guiStories.<event_handler>
        self.populateList()
        print "Event handler `btnRenamePressed' not implemented!"
        event.Skip()

    def btnDeletePressed(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `btnDeletePressed' not implemented!"
        event.Skip()

    def btnPlayPressed(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `btnPlayPressed' not implemented!"
        event.Skip()

    def btnPublishPressed(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `btnPublishPressed' not implemented!"
        event.Skip()

    def btnBackPressed(self, event): # wxGlade: guiStories.<event_handler>
        self.Hide()
        self.env['guiStudents'].Show()
    
    def setEnv(self,env): 
        self.env = env 
        
    def setStudent(self,index):
        self.student = self.env['class'].students[index]
        self.SetTitle(self.student.getName() + '\'s Stories')
        
    def onClose(self, event):
        dialog = wx.MessageDialog(None,'Are you sure you want to leave?','Sami Says',wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            sys.exit()
        else:
            dialog.Destroy()
            
    def populateList(self):
        self.lstStories.Clear()
        self.student.loadNames('students/_' + self.student.getName())
        count = 0;
        for i in self.student.stories:
            self.lstStories.Insert(i.name,count)
            count+=1
        if(self.lstStories.GetCount() > 0):
            self.lstStories.SetSelection(0)
            self.btnSelect.Enable()
        else:
            self.btnSelect.Enable(False)

# end of class guiStories


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frmMain = GuiStories(None, -1, "")
    app.SetTopWindow(frmMain)
    frmMain.Show()
    app.MainLoop()
