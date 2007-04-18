#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import os

STUDENT_DIR = 'students/'

class GuiAssign(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiAssign.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, -1)
        self.sizer_2_staticbox = wx.StaticBox(self.panel, -1, "Students")
        self.sizer_2_staticbox.SetFont(wx.Font(16,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.chkLstStudents = wx.CheckListBox(self.panel, -1, choices=[])
        self.btnAssign = wx.Button(self.panel, -1, "Assign")
        self.btnAssign.SetFont(wx.Font(16,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnCancel = wx.Button(self.panel, -1, "Cancel")
        self.btnCancel.SetFont(wx.Font(16,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.chkBoxBeeps = wx.CheckBox(self.panel, -1, "Insert Beep")
        self.chkBoxBeeps.SetFont(wx.Font(16,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.chkBoxBeeps.SetValue(True)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SHOW, self.handleShow, self)
        self.panel.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.btnAssign.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.btnAssign.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.btnCancel.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.btnCancel.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.chkLstStudents.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.chkLstStudents.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_BUTTON, self.btnAssignPressed, self.btnAssign)
        self.Bind(wx.EVT_BUTTON, self.btnCancelPressed, self.btnCancel)
        self.Bind(wx.EVT_CLOSE, self.close)
        # end wxGlade
        
        self.firstDown = -1

    def __set_properties(self):
        # begin wxGlade: guiAssign.__set_properties
        self.SetTitle("Sami Says")
        self.SetSize((400, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiAssign.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(4, 3, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(3, 5, 0, 0)
        sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.HORIZONTAL)
        grid_sizer_1.AddSpacer(10)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_1.AddSpacer(10)
        sizer_2.Add(self.chkLstStudents, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_2, 1, wx.EXPAND, 1)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_2.AddSpacer(10)
        #grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.Add(self.chkBoxBeeps, 0, 0, 0)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.Add(self.btnAssign, 0, wx.EXPAND, 0)
        grid_sizer_2.AddSpacer(10)
        grid_sizer_2.Add(self.btnCancel, 0, wx.EXPAND, 0)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(10)
        grid_sizer_2.AddGrowableRow(1)
        grid_sizer_2.AddGrowableCol(1)
        grid_sizer_2.AddGrowableCol(3)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.AddSpacer(10)
        self.panel.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(1)
        self.panel.SetSizer(grid_sizer_1)
        self.panel.Layout()
        self.Layout()
        # end wxGlade
    
    def setEnv(self,env): 
        self.env = env 
        
    def handleShow(self, event):
        self.populateList()
        
    def btnCancelPressed(self, event):
        self.close()
        
    def btnAssignPressed(self, event):
        checkedStudents = self.getCheckedStudents()
        story = self.env['story']
        succStudents = []
        for studentName in checkedStudents:
            if os.path.exists('%s_%s/%s.pkl' % (STUDENT_DIR, studentName, story.name)):
                msg = '%s already has a story by this name.  The story will not be added to %s\'s StoryBook.' % (studentName, studentName)
                msgDialog = wx.MessageDialog(self, msg, 'Error: Story Already Exists', wx.ICON_ERROR)
                msgDialog.ShowModal()
                msgDialog.Destroy()
            else:
                cStory = story.getCopy(studentName)
                cStory.mergeAndLockBreaks(includeBreakClip = self.chkBoxBeeps.IsChecked())
                cStory.pickleMe(True)
                cStory.pickleTitle()
                succStudents += [studentName]
        
        msg = ''
        if len(succStudents) > 1:
            msg = 'Assignment succesfully added to %s, and %s\'s StoryBooks.' % (', '.join(succStudents[:-1]), succStudents[-1]) 
        elif len(succStudents) == 1:
            msg = 'Assignment succesfully added to %s\'s StoryBook.' % succStudents[0]
        
        if msg != '':
            msgDialog = wx.MessageDialog(self, msg, 'Success!', wx.ICON_INFORMATION)
            msgDialog.ShowModal()
            msgDialog.Destroy()
        
        self.close()
        
    def populateList(self):
        self.chkLstStudents.Clear()
        count = 0
        for i in self.env['class'].students:
            self.chkLstStudents.Insert(i.name,count)
            count+=1
        self.chkLstStudents.SetSelection(0)
                   
    def close(self, event=None):
        self.Hide()
        self.env['guiStories'].Enable()
        self.env['guiStories'].Raise()
        
    def getCheckedStudents(self):
        students = self.env['class'].students
        checkedStudents = []
        for i in xrange(len(students)):
            if self.chkLstStudents.IsChecked(i):
                checkedStudents += [students[i].getName()]
                
            
        return checkedStudents

    def onKeyDown(self, event):
        
        if self.firstDown == -1:
            self.firstDown = event.GetKeyCode()
    
    def onKeyUp(self, event):
        
        keyCode = event.GetKeyCode()
        if keyCode != self.firstDown:
            event.Skip()
        
        if keyCode == wx.WXK_ESCAPE:
            self.btnCancelPressed(False)
        
        self.firstDown = -1        
        
# end of class guiAssign


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    test = GuiAssign(None, -1, "")
    app.SetTopWindow(test)
    test.Show()
    app.MainLoop()
    test.Refresh()
