#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Tue Feb 20 00:22:41 2007

import wx

class GuiStories(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiStories.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.filler00 = wx.Panel(self, -1)
        self.filler01 = wx.Panel(self, -1)
        self.lstStories = wx.ListBox(self, -1, choices=[])
        self.filler02 = wx.Panel(self, -1)
        self.btnSelect = wx.Button(self, -1, "Select")
        self.filler03 = wx.Panel(self, -1)
        self.btnCreate = wx.Button(self, -1, "Create")
        self.filler04 = wx.Panel(self, -1)
        self.btnRename = wx.Button(self, -1, "Rename")
        self.filler05 = wx.Panel(self, -1)
        self.btnDelete = wx.Button(self, -1, "Delete")
        self.filler06 = wx.Panel(self, -1)
        self.btnPlay = wx.Button(self, -1, "Play")
        self.filler07 = wx.Panel(self, -1)
        self.btnPublish = wx.Button(self, -1, "Publish")
        self.filler08 = wx.Panel(self, -1)
        self.btnBack = wx.Button(self, -1, "Back")
        self.filler09 = wx.Panel(self, -1)
        self.filler10 = wx.Panel(self, -1)

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
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: guiStories.__set_properties
        self.SetTitle("Sami's Stories")
        self.SetSize((400, 400))
        self.btnSelect.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiStories.__do_layout
        szrParent = wx.FlexGridSizer(3, 1, 0, 0)
        szrChildList = wx.FlexGridSizer(1, 6, 0, 0)
        szrChildButtons = wx.FlexGridSizer(13, 1, 0, 0)
        szrParent.Add(self.filler00, 1, wx.EXPAND, 0)
        szrChildList.Add(self.filler01, 1, wx.EXPAND, 0)
        szrChildList.Add(self.lstStories, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildList.Add(self.filler02, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnSelect, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildButtons.Add(self.filler03, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnCreate, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildButtons.Add(self.filler04, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnRename, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildButtons.Add(self.filler05, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnDelete, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildButtons.Add(self.filler06, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnPlay, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildButtons.Add(self.filler07, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnPublish, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildButtons.Add(self.filler08, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnBack, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        szrChildButtons.AddGrowableRow(0)
        szrChildButtons.AddGrowableRow(2)
        szrChildButtons.AddGrowableRow(4)
        szrChildButtons.AddGrowableRow(6)
        szrChildButtons.AddGrowableRow(8)
        szrChildButtons.AddGrowableRow(10)
        szrChildButtons.AddGrowableRow(12)
        szrChildButtons.AddGrowableCol(0)
        szrChildList.Add(szrChildButtons, 1, wx.EXPAND, 0)
        szrChildList.Add(self.filler09, 1, wx.EXPAND, 0)
        szrChildList.AddGrowableRow(0)
        szrChildList.AddGrowableCol(1)
        szrChildList.AddGrowableCol(3)
        szrParent.Add(szrChildList, 1, wx.EXPAND, 0)
        szrParent.Add(self.filler10, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(szrParent)
        szrParent.AddGrowableRow(1)
        szrParent.AddGrowableCol(0)
        self.Layout()
        # end wxGlade

    def lstStoriesDblClick(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `lstStoriesDblClick' not implemented!"
        event.Skip()

    def btnSelectPressed(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `btnSelectPressed' not implemented!"
        event.Skip()

    def btnCreatePressed(self, event): # wxGlade: guiStories.<event_handler>
        print "Event handler `btnCreatePressed' not implemented!"
        event.Skip()

    def btnRenamePressed(self, event): # wxGlade: guiStories.<event_handler>
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
        print "Event handler `btnBackPressed' not implemented!"
        event.Skip()

# end of class guiStories


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frmMain = GuiStories(None, -1, "")
    app.SetTopWindow(frmMain)
    frmMain.Show()
    app.MainLoop()
