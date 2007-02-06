import wx
import pySonic
import pymedia.audio.sound as sound
import pymedia.audio.acodec as acodec


# recording characteristics
RATE = 44100    # samples per second
BITS = 16       # BITS per sample
CHANNELS = 1    # 1 is mono, 2 is stereo
BUFF_DURATION = 1# showing off that the buffer can be shorter so we can record long segments



class SoundControl:

    def __init__(self):
        # initialize pySonic
        self.w = pySonic.World(44100,32)
        
        # get a recorder object
        self.rec = pySonic.Recorder()
        
        # get a source for playback
        self.src = pySonic.Source()
        
        # allocate an EmptySample to hold buffduration seconds of the incoming audio
        self.sample = pySonic.EmptySample(BUFF_DURATION*RATE, CHANNELS, BITS, RATE)
        
        # store audio as it is recorded here
        self.recData = []
        self.lastPos = 0  # keep track of the last sample recorded
        self.isRecording = False
        
        '''Grab last chunk of recorded audio'''
    def grabAudio(self):
        pos = self.rec.CurrentSample
        #print pos
        N = pos - self.lastPos
        if N < 0:
            N += BUFF_DURATION * RATE
        self.recData.append(self.sample.GetBytes(self.lastPos, N))
        self.lastPos = pos
    
    '''Start recording sound.  If already recording, do nothing.'''
    def startRecord(self):  
        if self.isRecording:
            return
        
        self.recData = []
        self.lastPos = 0
        self.rec.Start(self.sample, loopit=True)
        self.isRecording = True
        
    '''Stop recording and return sound bytes.  If not recording, do nothing.'''
    def stopRecord(self):
        if not self.isRecording:
            return
        
        self.rec.Stop()
        self.isRecording = False
        self.grabAudio()
        soundBytes = ''.join(self.recData) # join all the chunks together into one long string
        return soundBytes
    
    def playSoundFile(self, filePath, blocking = False):
        self.src.Sound = pySonic.FileSample(filePath)
        self.src.Play()
        
        if not blocking:
            return
        
        while self.src.IsPlaying():
            pass
        
    def playSoundBytes(self, soundBytes, blocking = False):
        self.src.Sound = pySonic.MemorySample(soundBytes, CHANNELS, BITS, RATE)
        self.src.Play()
        
        if not blocking:
            return
        
        while self.src.IsPlaying():
            pass
        
    def stopPlay(self):
        if self.src.IsPlaying():
            self.src.Stop()
        
    def isPlaying(self):
        return self.src.IsPlaying()
        
    def onTimer(self, event):
        '''Grab recorded audio'''
        if self.isRecording:
            self.grabAudio()
        event.Skip()
    
def resamplePySonic(oldSample):
    oRate = oldSample.Frequency
    oSampleSize = oldSample.SampleSize
    oNumSamples = oldSample.NumSamples
    oChannels = oldSample.Channels
    
    if oSampleSize == 8:
        oSoundBytes = oldSample.GetBytes(0, oNumSamples)
        soundBytes = ''
        for byte in oSoundBytes:
            soundBytes += '\x00' + byte
    else:
        soundBytes = oldSample.GetBytes(0, oNumSamples*2)
    
    resampler = sound.Resampler((oRate,oChannels),(RATE,CHANNELS))
    soundBytes = resampler.resample(soundBytes)

    return soundBytes
    
def encodeToMp3(soundBytes, fileName):
    params= {'id': acodec.getCodecID('mp3'),
            'bitrate': BITS,
            'sample_rate': RATE,
            'ext': 'mp3',
            'channels': CHANNELS } 
    enc = acodec.Encoder(params)
    frames = enc.encode(soundBytes)
    f = file(fileName,'wb')
    for frame in frames:
        f.write(frame)
    f.close()
        