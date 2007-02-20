#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Mon Feb 19 22:21:25 2007

import wx

class GuiStudents(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiStudents.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.filler00 = wx.Panel(self, -1)
        self.filler01 = wx.Panel(self, -1)
        self.lstStudents = wx.ListBox(self, -1, choices=[])
        self.filler02 = wx.Panel(self, -1)
        self.btnSelect = wx.Button(self, -1, "Select")
        self.filler03 = wx.Panel(self, -1)
        self.btnCreate = wx.Button(self, -1, "Create")
        self.filler04 = wx.Panel(self, -1)
        self.btnRemove = wx.Button(self, -1, "Remove")
        self.filler05 = wx.Panel(self, -1)
        self.btnBack = wx.Button(self, -1, "Back")
        self.filler06 = wx.Panel(self, -1)
        self.filler07 = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.lstStudentsDblClick, self.lstStudents)
        self.Bind(wx.EVT_BUTTON, self.btnSelectPressed, self.btnSelect)
        self.Bind(wx.EVT_BUTTON, self.btnCreatePressed, self.btnCreate)
        self.Bind(wx.EVT_BUTTON, self.btnRemovePressed, self.btnRemove)
        self.Bind(wx.EVT_BUTTON, self.btnBackPressed, self.btnBack)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: guiStudents.__set_properties
        self.SetTitle("Student Selection")
        self.SetSize((500, 500))
        self.filler00.SetMinSize((-1, 30))
        self.filler01.SetMinSize((30, -1))
        self.filler02.SetMinSize((25, -1))
        self.btnSelect.SetDefault()
        self.filler03.SetMinSize((75, 14))
        self.filler06.SetMinSize((30, -1))
        self.filler07.SetMinSize((-1, 30))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiStudents.__do_layout
        szrParent = wx.FlexGridSizer(3, 1, 0, 5)
        szrChildList = wx.FlexGridSizer(1, 5, 0, 0)
        szrChildButtons = wx.FlexGridSizer(7, 1, 0, 0)
        szrParent.Add(self.filler00, 1, wx.EXPAND, 0)
        szrChildList.Add(self.filler01, 1, wx.EXPAND, 0)
        szrChildList.Add(self.lstStudents, 0, wx.EXPAND, 0)
        szrChildList.Add(self.filler02, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnSelect, 0, wx.EXPAND, 0)
        szrChildButtons.Add(self.filler03, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnCreate, 0, wx.EXPAND, 0)
        szrChildButtons.Add(self.filler04, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnRemove, 0, wx.EXPAND, 0)
        szrChildButtons.Add(self.filler05, 1, wx.EXPAND, 0)
        szrChildButtons.Add(self.btnBack, 0, wx.EXPAND, 0)
        szrChildButtons.AddGrowableRow(0)
        szrChildButtons.AddGrowableRow(1)
        szrChildButtons.AddGrowableRow(2)
        szrChildButtons.AddGrowableRow(3)
        szrChildButtons.AddGrowableRow(4)
        szrChildButtons.AddGrowableRow(5)
        szrChildButtons.AddGrowableRow(6)
        szrChildButtons.AddGrowableCol(0)
        szrChildList.Add(szrChildButtons, 1, wx.EXPAND, 0)
        szrChildList.Add(self.filler06, 1, wx.EXPAND, 0)
        szrChildList.AddGrowableRow(0)
        szrChildList.AddGrowableCol(1)
        szrChildList.AddGrowableCol(3)
        szrParent.Add(szrChildList, 1, wx.EXPAND, 0)
        szrParent.Add(self.filler07, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(szrParent)
        szrParent.AddGrowableRow(1)
        szrParent.AddGrowableCol(0)
        self.Layout()
        self.Centre()
        # end wxGlade

    def lstStudentsDblClick(self, event): # wxGlade: guiStudents.<event_handler>
        print "Event handler `lstStudentsDblClick' not implemented!"

    def btnSelectPressed(self, event): # wxGlade: guiStudents.<event_handler>
        print "Event handler `btnSelectPressed' not implemented!"

    def btnCreatePressed(self, event): # wxGlade: guiStudents.<event_handler>
        print "Event handler `btnCreatePressed' not implemented!"

    def btnRemovePressed(self, event): # wxGlade: guiStudents.<event_handler>
        print "Event handler `btnRemovePressed' not implemented!"

    def btnBackPressed(self, event): # wxGlade: guiStudents.<event_handler>
        print "Event handler `btnBackPressed' not implemented!"
        

# end of class guiStudents


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frmMain = GuiStudents(None, -1, "")
    app.SetTopWindow(frmMain)
    frmMain.Show()
    app.MainLoop()
