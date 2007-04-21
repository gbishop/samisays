
# system imports
import wx

# project imports
from Class import Class
from GuiStart import GuiStart
from GuiStories import GuiStories
from GuiStudents import GuiStudents
from GuiAssign import GuiAssign
from SoundControl import SoundControl
from AuiStorySelection import *
from AuiStoryCreation import *
from GuiVisualizer import *
from Constants import *


class GuiMain(wx.App):
    
    def OnInit(self):
        currentClass = Class()
        currentClass.save()
        currentClass.load()
        wx.InitAllImageHandlers()
        self.env = {}
        start = GuiStart(None, -1, "")
        students = GuiStudents(None, -1, "")
        stories = GuiStories(None, -1, "")
        assign = GuiAssign(None, -1, "")
        self.env = {'class': currentClass, 'guiStart': start, 'guiStudents': students, 
                    'guiStories': stories, 'guiAssign': assign}
        self.env['SoundControl'] = SoundControl()
        self.env['keyDownFunct'] = None
        self.env['keyUpFunct'] = None
        self.env['guiWorking'] = GuiVisualizer(None, -1, "")
        self.env['guiWorking'].Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.env['guiWorking'].Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.env['guiStories'].Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.env['guiStories'].Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.env['auiStorySelection'] = AuiStorySelection(self.env)
        self.env['auiStoryCreation'] = AuiStoryCreation(self.env)
        self.env['auiInsertSound'] = AuiInsertSound(self.env)
        self.env['timer'] = wx.Timer(self.env['guiWorking'])
        self.env['guiWorking'].Bind(wx.EVT_TIMER, self.env['SoundControl'].onTimer)
        self.env['storiesLock'] = False
        start.setEnv(self.env)
        students.setEnv(self.env)
        stories.setEnv(self.env)
        assign.setEnv(self.env)
        self.env['guiWorking'].setEnv(self.env)
        return True

    def onKeyDown(self,event):
        self.env['keyDownFunct'](event)
    
    def onKeyUp(self,event):
        self.env['keyUpFunct'](event)
        
if __name__ == '__main__':
    app = GuiMain(0)
    app.SetTopWindow(app.env['guiStart'])
    app.env['guiStart'].Show()
    app.MainLoop()
