''' Imports '''
import wx
import os
import sys
from Student import *
from Constants import *

class GuiStudents(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiStudents.__init__
        kwds['style'] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self,-1)
        self.lstStudents = wx.ListBox(self.panel, -1, choices=[])
        self.lstStudents.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnSelect = wx.Button(self.panel, -1, 'Select')
        self.btnSelect.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnCreate = wx.Button(self.panel, -1, 'Add Student')
        self.btnCreate.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnRemove = wx.Button(self.panel, -1, 'Remove Student')
        self.btnRemove.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnBack = wx.Button(self.panel, -1, 'Back')
        self.btnBack.SetFont(wx.Font(32,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.lblHead = wx.StaticText(self.panel,-1,"The Bookshelf")
        self.lblHead.SetFont(wx.Font(48,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))

        self.__set_properties()
        self.__do_layout()

        objects = [self.panel, self.lstStudents, self.btnSelect, self.btnCreate,
                   self.btnRemove, self.btnBack, self.lblHead]
        for obj in objects:
            obj.Bind(wx.EVT_KEY_UP, self.onKeyUp)
            obj.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
            
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.lstStudentsDblClick, self.lstStudents)
        self.Bind(wx.EVT_BUTTON, self.btnSelectPressed, self.btnSelect)
        self.Bind(wx.EVT_BUTTON, self.btnCreatePressed, self.btnCreate)
        self.Bind(wx.EVT_BUTTON, self.btnRemovePressed, self.btnRemove)
        self.Bind(wx.EVT_BUTTON, self.btnBackPressed, self.btnBack)
        
        # Added By Patrick
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.firstDown = -1
        self.env = {}

    def __set_properties(self):
        # begin wxGlade: guiStudents.__set_properties
        self.SetTitle("Sami Says")
        self.SetPosition((0,0))
        self.SetSize(wx.DisplaySize())
        self.btnSelect.SetDefault()
        self.btnSelect.SetFocus()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiStudents.__do_layout
        szrParent = wx.FlexGridSizer(3, 1, 0, 5)
        szrChildList = wx.FlexGridSizer(1, 5, 0, 0)
        szrChildButtons = wx.FlexGridSizer(7, 1, 0, 0)
        #szrParent.AddSpacer(20)
        szrParent.Add(self.lblHead,0,wx.ALIGN_CENTRE, 0)
        szrChildList.AddSpacer(20)
        szrChildList.Add(self.lstStudents, 0, wx.EXPAND, 0)
        szrChildList.AddSpacer(10)
        szrChildButtons.Add(self.btnSelect, 0, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(-1)
        szrChildButtons.Add(self.btnCreate, 0, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(-1)
        szrChildButtons.Add(self.btnRemove, 0, wx.EXPAND, 0)
        szrChildButtons.AddSpacer(-1)
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
        szrChildList.AddSpacer(20)
        szrChildList.AddGrowableRow(0)
        szrChildList.AddGrowableCol(1)
        szrChildList.AddGrowableCol(3)
        szrParent.Add(szrChildList, 1, wx.EXPAND, 0)
        szrParent.AddSpacer(40)
        self.panel.SetAutoLayout(True)
        self.panel.SetSizer(szrParent)
        szrParent.AddGrowableRow(1)
        szrParent.AddGrowableCol(0)
        self.panel.Layout()
        # end wxGlade

    def handleSelect(self):
        self.Hide()
        self.env['student'] = self.env['class'].students[self.lstStudents.GetSelection()]
        self.env['guiStories'].setStudent(self.lstStudents.GetSelection())
        self.env['guiStories'].Show()

    def lstStudentsDblClick(self, event): # wxGlade: guiStudents.<event_handler>
        self.handleSelect()

    def btnSelectPressed(self, event): # wxGlade: guiStudents.<event_handler>
        self.handleSelect()

    def btnCreatePressed(self, event): # wxGlade: guiStudents.<event_handler>
        dialog = wx.TextEntryDialog(None,'Please enter the student\'s name:','Sami Says','')
        if dialog.ShowModal() == wx.ID_OK:
            newName = dialog.GetValue()
            if os.path.exists('%s_%s' % (STUDENT_DIR, newName)):
                msg = 'A student named %s already exists.  Try adding an initial or full name.' % (newName)
                msgDialog = wx.MessageDialog(self, msg, 'Error: Student Already Exists', wx.ICON_ERROR)
                msgDialog.ShowModal()
                msgDialog.Destroy()
                self.btnCreatePressed(False)
            elif(newName != ''):
                self.env['class'].addStudent(Student(dialog.GetValue()))
                self.populateList()
        
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
            self.lstStudents.Select(0)
            self.btnSelect.Enable()
        else:
            self.btnSelect.Enable(False)
        
    def onKeyDown(self, event):
        
        if self.firstDown == -1:
            self.firstDown = event.GetKeyCode()
    
    def onKeyUp(self, event):
        
        keyCode = event.GetKeyCode()
        if keyCode != self.firstDown:
            event.Skip()
        
        if keyCode == wx.WXK_ESCAPE:
            self.btnBackPressed(False)
        
        self.firstDown = -1      
# end of class guiStudents


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frmMain = GuiStudents(None, -1, "")
    app.SetTopWindow(frmMain)
    frmMain.Show()
    app.MainLoop()
