#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Mon Feb 19 22:21:25 2007

import wx
import sys
from Student import Student

class GuiStudents(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiStudents.__init__
        kwds['style'] = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        wx.Frame.__init__(self, *args, **kwds)
        self.filler00 = wx.Panel(self, -1)
        self.filler01 = wx.Panel(self, -1)
        self.lstStudents = wx.ListBox(self, -1, choices=[])
        self.lstStudents.SetFont(wx.Font(16,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.filler02 = wx.Panel(self, -1)
        self.btnSelect = wx.Button(self, -1, 'Select')
        self.btnSelect.SetFont(wx.Font(14,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.filler03 = wx.Panel(self, -1)
        self.btnCreate = wx.Button(self, -1, 'Add')
        self.btnCreate.SetFont(wx.Font(14,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.filler04 = wx.Panel(self, -1)
        self.btnRemove = wx.Button(self, -1, 'Remove')
        self.btnRemove.SetFont(wx.Font(14,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.filler05 = wx.Panel(self, -1)
        self.btnBack = wx.Button(self, -1, 'Back')
        self.btnBack.SetFont(wx.Font(14,wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.filler06 = wx.Panel(self, -1)
        self.filler07 = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.lstStudentsDblClick, self.lstStudents)
        self.Bind(wx.EVT_BUTTON, self.btnSelectPressed, self.btnSelect)
        self.Bind(wx.EVT_BUTTON, self.btnCreatePressed, self.btnCreate)
        self.Bind(wx.EVT_BUTTON, self.btnRemovePressed, self.btnRemove)
        self.Bind(wx.EVT_BUTTON, self.btnBackPressed, self.btnBack)
        
        # Added By Patrick
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.env = []

    def __set_properties(self):
        # begin wxGlade: guiStudents.__set_properties
        self.SetTitle("Student Selection")
        self.SetPosition((0,0))
        self.SetSize(wx.DisplaySize())
        self.filler00.SetMinSize((-1, 30))
        self.filler01.SetMinSize((30, -1))
        self.filler02.SetMinSize((25, -1))
        self.btnSelect.SetDefault()
        self.btnSelect.SetFocus()
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

    def handleSelect(self):
        self.Hide()
        self.env['guiStories'].setStudent(self.lstStudents.GetSelection());
        self.env['guiStories'].Show()

    def lstStudentsDblClick(self, event): # wxGlade: guiStudents.<event_handler>
        self.handleSelect()

    def btnSelectPressed(self, event): # wxGlade: guiStudents.<event_handler>
        self.handleSelect()

    def btnCreatePressed(self, event): # wxGlade: guiStudents.<event_handler>
        dialog = wx.TextEntryDialog(None,'Please enter the student\'s name:','Sami Says','')
        if dialog.ShowModal() == wx.ID_OK:
            newName = dialog.GetValue()
            if(newName != ''):
                self.env['class'].addStudent(Student(dialog.GetValue()))
                self.populateList()
        else:
            dialog.Destroy()

    def btnRemovePressed(self, event): # wxGlade: guiStudents.<event_handler>
        dialog = wx.MessageDialog(None,'Are you sure you want delete ' + 
                                  self.env['class'].students[self.lstStudents.GetSelection()].getName() + 
                                  ' from the class?','Sami Says',wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            self.env['class'].delStudent(self.lstStudents.GetSelection())
            self.populateList()
        else:
            dialog.Destroy()

    def btnBackPressed(self, event): # wxGlade: guiStudents.<event_handler>
        self.Hide()
        self.env['guiStart'].Show()
        
    def setEnv(self,env): 
        self.env = env
        self.populateList()
        
    def onClose(self, event):
        dialog = wx.MessageDialog(None,'Are you sure you want to leave?','Sami Says',wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            sys.exit()
        else:
            dialog.Destroy()
            
    def populateList(self):
        self.lstStudents.Clear()
        count = 0;
        for i in self.env['class'].students:
            self.lstStudents.Insert(i.name,count)
            count+=1
        if(self.lstStudents.GetCount() > 0):
            self.lstStudents.SetSelection(0)
            self.btnSelect.Enable()
        else:
            self.btnSelect.Enable(False)
        

# end of class guiStudents


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frmMain = GuiStudents(None, -1, "")
    app.SetTopWindow(frmMain)
    frmMain.Show()
    app.MainLoop()
