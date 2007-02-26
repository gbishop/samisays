import wx
from StoryCreationAUI import *
from SoundControl import *

#AUI is separate thread.  Condition variable on keydown/keyup.  Queue of keys.
# No, playback whole story is a separate thread.

class SamiSays(wx.App):
    
    def OnInit(self):
        
        self.SC = SoundControl()
        self.frame = wx.Frame(None, -1, 'Sami Says')
        self.SCA = StoryCreationAUI(self)
        self.keyDownFunct = self.SCA.onKeyDown
        self.keyUpFunct = self.SCA.onKeyUp
        self.frame.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.frame.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.frame.Show(True)
        self.frame.Bind(wx.EVT_TIMER, self.SC.onTimer)
        self.timer = wx.Timer(self.frame)
        self.timer.Start(100) # wake up every 100 milliseconds to handle audio
        
        return True
        
    
    def onKeyDown(self,event):
        self.keyDownFunct(event)
    
    def onKeyUp(self,event):
        self.keyUpFunct(event)
        
if __name__ == '__main__':
    app = SamiSays(0)
    app.MainLoop()