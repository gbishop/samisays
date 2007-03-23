import wx
from AuiStoryCreation import *
from SoundControl import *

#AUI is separate thread.  Condition variable on keydown/keyup.  Queue of keys.
# No, playback whole story is a separate thread.

class SamiSays(wx.App):
    
    def OnInit(self):
        
        self.env = dict()
        self.env['SoundControl'] = SoundControl()
        self.frame = wx.Frame(None, -1, 'Sami Says')
        self.env['auiStoryCreation'] = AuiStoryCreation(self.env)
        self.env['keyDownFunct'] = self.env['auiStoryCreation'].onKeyDown
        self.env['keyUpFunct'] = self.env['auiStoryCreation'].onKeyUp
        self.frame.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.frame.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.frame.Show(True)
        self.frame.Bind(wx.EVT_TIMER, self.env['SoundControl'].onTimer)
        self.timer = wx.Timer(self.frame)
        self.timer.Start(100) # wake up every 100 milliseconds to handle audio
        
        return True
        
    
    def onKeyDown(self,event):
        self.env['keyDownFunct'](event)
    
    def onKeyUp(self,event):
        self.env['keyUpFunct'](event)
        
if __name__ == '__main__':
    app = SamiSays(0)
    app.MainLoop()