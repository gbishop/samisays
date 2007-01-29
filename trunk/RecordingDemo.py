'''An example of a keyboard driven program in Python with wxPython

Records while the space bar is pressed, plays when it is released
r plays the audio reversed


'''

import wx
import pySonic
import numpy

# initialize pySonic
w = pySonic.World(44100,32,None,None,0)

# get a recorder object
rec = pySonic.Recorder()
rec.Driver = 0
# recording characteristics
rate = 16000    # samples per second
bits = 16       # bits per sample
channels = 1    # 1 is mono, 2 is stereo
buffduration = 1# showing off that the buffer can be shorter so we can record long segments

def ReverseSample(samp):
    '''Demonstrate signal processing on a sample'''
    N = samp.NumSamples
    bytes = samp.GetBytes(0, N)
    audio = numpy.fromstring(bytes, numpy.int16)
    audio = audio[::-1] # reverse it
    nsamp = pySonic.MemorySample(audio.tostring(), channels, bits, rate)
    return nsamp

class myApp(wx.App):

    def OnInit(self):
        '''Initialize the Application object here.'''
        self.frame = wx.Frame(None, -1, 'Keyboard Demo')
        self.frame.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.frame.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.frame.Show(True)

        # get a source for playback
        self.src = pySonic.Source()
        self.asound = None
    
        # get a recorder object
        self.rec = pySonic.Recorder()

        # allocate an EmptySample to hold buffduration seconds of the incoming audio
        self.sample = pySonic.EmptySample(buffduration*rate, channels, bits, rate)

        # store audio as it is recorded here
        self.data = []
        self.lastpos = 0  # keep track of the last sample recorded
        self.recording = False
        self.keyDown = False

        # menu
        self.menuNames = ['Record_Clip.wav','Delete_Clip.wav','Play_Clip.wav','Play_Story.wav']
        self.menuItem = 0
        self.clips = []
        self.currentClip = -1

        self.frame.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self.frame)
        self.timer.Start(100) # wake up every 100 milliseconds to handle audio

        self.src.Sound = pySonic.FileSample('opening.wav')
        self.src.Play()
        return True

    def GrabAudio(self):
        '''Grab a chunk of recorded audio'''
        pos = self.rec.CurrentSample
        #print pos
        N = pos - self.lastpos
        if N < 0:
            N += buffduration * rate
        self.data.append(self.sample.GetBytes(self.lastpos, N))
        self.lastpos = pos

    def OnTimer(self, event):
        '''Grab recorded audio'''
        if self.recording:
            self.GrabAudio()
        event.Skip()
    
    def OnKeyDown(self, event):
        '''This gets called on when a key is pressed.'''
        
        if self.keyDown:
            return

        keycode = event.GetKeyCode()        
        self.keyDown = True
        self.keyDownCode = keycode
        self.src.Stop()
        if keycode == wx.WXK_SPACE:
            self.data = []
            self.lastpos = 0
            self.rec.Start(self.sample, loopit=True)
            self.recording = True

       # elif self.menuItem ==2:            
       #     if not self.src.IsPaused():
       #         self.src.Sound = self.clips[self.currentClip]
       #     self.src.Play()     

        event.Skip()

    def OnKeyUp(self, event):
        '''This gets called when a key is released.'''
        keycode = event.GetKeyCode()
        print 'up', keycode
        if self.keyDownCode != keycode:
            return
        self.keyDown = False
        if keycode == wx.WXK_SPACE:
            self.rec.Stop()
            self.recording = False
            self.GrabAudio()
            bytes = ''.join(self.data) # join all the chunks together into one long string
            self.currentClip += 1
            self.clips.insert(self.currentClip,pySonic.MemorySample(bytes, channels, bits, rate))
            self.src.Sound = self.clips[self.currentClip]
            self.src.Play()

        elif keycode == 308: #CTRL
            for clip in self.clips:
                self.src.Sound = clip
                self.src.Play()
                while (self.src.IsPlaying()):
                    pass
                
        elif keycode == ord('R') and self.asound:
            self.src.Sound = ReverseSample(self.asound)
            self.src.Play()
        elif keycode == wx.WXK_UP:
            del self.clips[self.currentClip]
            self.currentClip -= 1
            if self.currentClip == -1:
                self.src.Sound = pySonic.FileSample('delete_title.wav')
            else:
                self.src.Sound = self.clips[self.currentClip]
            self.src.Play()
        elif keycode == wx.WXK_DOWN:
            pass
        elif keycode == wx.WXK_LEFT:
            if self.currentClip > 0:
                self.currentClip -= 1
            self.src.Sound = self.clips[self.currentClip]
            self.src.Play()
        elif keycode == wx.WXK_RIGHT:
            if self.currentClip < len(self.clips)-1:
                self.currentClip += 1
            self.src.Sound = self.clips[self.currentClip]
            self.src.Play()

        event.Skip()

if __name__ == '__main__':
    app = myApp(0)
    app.MainLoop()
