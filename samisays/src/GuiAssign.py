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
        self.panel.SetFont(wx.Font(16,wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.sizer_2_staticbox = wx.StaticBox(self.panel, -1, "Students")
        self.chkLstStudents = wx.CheckListBox(self.panel, -1, choices=[])
        self.btnAssign = wx.Button(self.panel, -1, "Assign")
        self.btnCancel = wx.Button(self.panel, -1, "Cancel")


        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SHOW, self.handleShow, self)
        self.Bind(wx.EVT_BUTTON, self.btnAssignPressed, self.btnAssign)
        self.Bind(wx.EVT_BUTTON, self.btnCancelPressed, self.btnCancel)
        self.Bind(wx.EVT_CLOSE, self.close)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: guiAssign.__set_properties
        self.SetTitle("Sami Says")
        self.SetSize((400, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiAssign.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(3, 3, 0, 0)
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
        grid_sizer_2.AddSpacer(-1)
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
                cStory.mergeAndLockBreaks(True)
                cStory.pickleMe()
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


# end of class guiAssign


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    test = guiAssign(None, -1, "")
    app.SetTopWindow(test)
    test.Show()
    app.MainLoop()
    test.Refresh()
