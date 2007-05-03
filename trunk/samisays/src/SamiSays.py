''' Imports '''
import wx
from Class import *
from GuiStart import *
from GuiStories import *
from GuiStudents import *
from GuiAssign import *
from SoundControl import *
from AuiStorySelection import *
from AuiStoryCreation import *
from GuiVisualizer import *
from GuiPrioritize import *
from Constants import *

class SamiSays(wx.App):
    '''
    This is the Launchpad for the application. All initializations and 
    instantiation goes here.
    '''
    

    def OnInit(self):
        '''
        Does Everything!
        '''
        currentClass = Class()
        currentClass.save()
        currentClass.load()
        wx.InitAllImageHandlers()
        self.env = {}
        start = GuiStart(None, -1, "")
        students = GuiStudents(None, -1, "")
        stories = GuiStories(None, -1, "")
        assign = GuiAssign(None, -1, "")
        prior = GuiPrioritize(None, -1, "")
        self.env = {'class': currentClass, 'guiStart': start, 'guiStudents': students, 
                    'guiStories': stories, 'guiAssign': assign, 'guiPrioritize': prior}
        self.env['SoundControl'] = SoundControl()
        self.env['keyDownFunct'] = None
        self.env['keyUpFunct'] = None
        self.env['guiVisualizer'] = GuiVisualizer(None, -1, "")
        self.env['guiVisualizer'].Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.env['guiVisualizer'].Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.env['guiStories'].Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.env['guiStories'].Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.env['soundLibrary'] = SoundLibrary(self.env)
        self.env['auiStorySelection'] = AuiStorySelection(self.env)
        self.env['auiStoryCreation'] = AuiStoryCreation(self.env)
        self.env['auiInsertSound'] = AuiInsertSound(self.env)
        self.env['timer'] = wx.Timer(self.env['guiVisualizer'])
        self.env['guiVisualizer'].Bind(wx.EVT_TIMER, self.env['SoundControl'].onTimer)
        self.env['storiesLock'] = False
        start.setEnv(self.env)
        students.setEnv(self.env)
        stories.setEnv(self.env)
        assign.setEnv(self.env)
        prior.setEnv(self.env)
        self.env['guiVisualizer'].setEnv(self.env)
        return True


    def onKeyDown(self,event):
        '''
        Placeholder for key down bindings.
        '''
        self.env['keyDownFunct'](event)
    

    def onKeyUp(self,event):
        '''
        Placeholder for key up bindings.
        '''
        self.env['keyUpFunct'](event)

''' Execute at Runtime '''
if __name__ == '__main__':
    app = SamiSays(0)
    app.SetTopWindow(app.env['guiStart'])
    app.env['guiStart'].Show()
    app.MainLoop()
