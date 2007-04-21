import pySonic
import pymedia.audio.sound as sound
import pymedia.audio.acodec as acodec
import pyTTS
from numpy import *
from Constants import *

'''
' Class Name:  SoundControl
' Description: This object controls all aspects of sound playback, recording, modification,
'              and exporting.  A single SoundControl object should be used for each instance
'              of Sami Says so that only one sound will be played or recorded at a time.  
' Dependencies: pySonic - for recording and playback
'               pymedia - for resampling, converting, and exporting
'               numpy - for normalizing
'''
class SoundControl:

    '''
    ' Constructor initializes object.
    '''
    def __init__(self):
        
        self.tts = pyTTS.Create()
        self.tts.SetOutputFormat(TTS_RATE/1000,BITS,CHANNELS)
        
        # initialize pySonic
        self.w = pySonic.World()
        
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
        
        
    ''' 
    ' Grabs last chunk of recorded audio and appends it to the current recording. 
    '''
    def grabAudio(self):

        pos = self.rec.CurrentSample

        N = pos - self.lastPos
        if N < 0:
            N += BUFF_DURATION * RATE
        self.recData.append(self.sample.GetBytes(self.lastPos, N))
        self.lastPos = pos
    
    ''' 
    ' Start recording sound.  If already recording, do nothing. 
    '''
    def startRecord(self):  
        if self.isRecording:
            return
        
        self.recData = []
        self.lastPos = 0
        self.rec.Start(self.sample, loopit=True)
        self.isRecording = True
        
    ''' 
    ' Stop recording and return sound bytes.  If not recording, do nothing. 
    '''
    def stopRecord(self):
        
        if not self.isRecording:
            return
        
        self.rec.Stop()
        self.isRecording = False
        self.grabAudio()
        soundBytes = ''.join(self.recData) # join all the chunks together into one string
        return soundBytes
    
    ''' 
    ' Plays specified file (wav, aiff, mp3, ogg, etc.) with or without blocking. 
    '''
    def playSoundFile(self, filePath, blocking = False):
        self.src.Sound = pySonic.FileSample(filePath)
        self.src.Play()
        
        if not blocking:
            return
        
        while self.src.IsPlaying():
            pass
    
    ''' 
    ' Plays sound given in byte string with or without blocking. 
    '''
    def playSoundBytes(self, soundBytes, blocking = False, rate = RATE):
        self.src.Sound = pySonic.MemorySample(soundBytes, CHANNELS, BITS, rate)
        self.src.Play()
        
        if not blocking:
            return
        
        while self.src.IsPlaying():
            pass
    
    ''' 
    ' Stops whatever is playing. If not playing, does nothing. 
    '''
    def stopPlay(self):
        if self.src.IsPlaying():
            self.src.Stop()
    
    ''' Returns True if a sound is being played.  Otherwise, returns False. '''
    def isPlaying(self):
        return self.src.IsPlaying()
    
    ''' 
    ' Called every 1000 seconds.  If recording, this is when the buffer should be full.
    ' Audio in buffer is grabbed to make room for more. 
    '''
    def onTimer(self, event):

        if self.isRecording:
            self.grabAudio()
        event.Skip()
        
    def speakText(self, text, blocking = False):
        m = self.tts.SpeakToMemory(text)
        format = m.Format.GetWaveFormatEx()
        soundBytes = m.GetData()
        self.playSoundBytes(soundBytes, blocking, TTS_RATE)
        
    def speakTextFile(self, filepath, blocking = False):
        text = file(filepath,'r').read()
        self.speakText(text, blocking)

def soundFileToBytes(filePath):
    soundBytes = resampleSoundFile(filePath)
    soundBytes = normalizeSoundBytes(soundBytes)
    return soundBytes

'''
' Normalizes sound bytes by finding the peak and scaling everything by it up to the maximum amplitude.
'''
def normalizeSoundBytes(soundBytes):
    soundArray = fromstring(soundBytes, int16)
    m = max(abs(soundArray))
    soundArray = soundArray/float(m)*20000
    soundArray = array(soundArray,int16)
    return soundArray.tostring()

'''
' Resamples the sound file into the default sound properties specified above and returns as bytes.
' Uses pymedia's built-in resampler.
'''      
def resampleSoundFile(filePath):
    
    oldSample = pySonic.FileSample(filePath)
    oRate = oldSample.Frequency
    oSampleSize = oldSample.SampleSize
    oNumSamples = oldSample.NumSamples
    oChannels = oldSample.Channels
    
    
    if oSampleSize == 8:
        oSoundBytes = oldSample.GetBytes(0, oNumSamples)
        oSoundArray = fromstring(oSoundBytes, int8)
        soundArray = array(oSoundArray, int16)
        soundBytes = oSoundArray.tostring()
    else:
        soundBytes = oldSample.GetBytes(0, oNumSamples*2)
    
    resampler = sound.Resampler((oRate,oChannels),(RATE,CHANNELS))
    soundBytes = resampler.resample(soundBytes)

    return soundBytes

'''
' Resamples a sound byte stream with the bitrate and # of channels specified.
' Uses pymedia's built-in resampler.
'''
def resampleSoundBytes(soundBytes, newRate, newChannels):
    
    resampler = sound.Resampler((RATE, CHANNELS),(newRate, newChannels))
    newBytes = resampler.resample(soundBytes)
    return newBytes

'''
' Encodes sound bytes into mp3 format using pymedia's built-in encoder.  
' The sound is expected to have the default sound properties specified above.
'''
def encodeToMp3(soundBytes, fileName, bitRate = MP3_RATE):
    params= {'id': acodec.getCodecID('mp3'),
            'bitrate': bitRate,
            'sample_rate': RATE,
            'ext': 'mp3',
            'channels': CHANNELS } 
    for i in xrange(100000):
        soundBytes += '\x00'
    enc = acodec.Encoder(params)
    
    frames = enc.encode(soundBytes)
    f = file(fileName,'wb')
    for frame in frames:
        f.write(frame)
    f.close()
    
def getDuration(soundBytes):
    BITS_PER_BYTE = 8
    numBytes = len(soundBytes)
    numSamples = BITS_PER_BYTE * numBytes/BITS
    sec = numSamples/float(RATE)   
    min = int(sec/60)
    sec = sec%60
    return min,sec
        