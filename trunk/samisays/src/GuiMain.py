
# system imports
import wx

# project imports
from Class import Class
from GuiStart import GuiStart
from GuiStories import GuiStories
from GuiStudents import GuiStudents
from SoundControl import SoundControl

class GuiMain(wx.App):
    
    def OnInit(self):
        currentClass = Class()
        currentClass.load()
        wx.InitAllImageHandlers()
        self.env = {}
        start = GuiStart(None, -1, "")
        students = GuiStudents(None, -1, "")
        stories = GuiStories(None, -1,"")
        self.env = {'class': currentClass, 'guiStart': start, 'guiStudents': students, 'guiStories': stories}
        self.env['SoundControl'] = SoundControl()
        self.env['keyDownFunct'] = None
        self.env['keyUpFunct'] = None
        self.env['guiWorking'] = wx.Frame(None, -1, 'Recording a Story')
        self.env['guiWorking'].Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.env['guiWorking'].Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.env['timer'] = wx.Timer(self.env['guiWorking'])
        self.env['guiWorking'].Bind(wx.EVT_TIMER, self.env['SoundControl'].onTimer)
        start.setEnv(self.env)
        students.setEnv(self.env)
        stories.setEnv(self.env)
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
