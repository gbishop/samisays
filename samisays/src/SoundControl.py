import pySonic
import pymedia.audio.sound as sound
import pymedia.audio.acodec as acodec
import pyTTS
from numpy import *
from Constants import *



class SoundControl:
    '''
    This object controls all aspects of sound playback, recording, modification,
    and exporting.  A single SoundControl object should be used for each instance
    of Sami Says so that only one sound will be played or recorded at a time.  
    
    Dependencies: pySonic - for recording and playback
                  pymedia - for resampling, converting, and exporting
                  numpy - for normalizing
    '''

    def __init__(self):
        '''
        Constructor initializes object variables and dependencies.
        '''
        
        # initialize pyTTS
        self.tts = pyTTS.Create()
        self.tts.SetOutputFormat(RATE/1000,BITS,CHANNELS)
        
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
        
        
    def grabAudio(self):
        '''
        Grabs last chunk of recorded audio and appends it to the current recording.
        '''

        pos = self.rec.CurrentSample

        N = pos - self.lastPos
        if N < 0:
            N += BUFF_DURATION * RATE
        self.recData.append(self.sample.GetBytes(self.lastPos, N))
        self.lastPos = pos
    

    def startRecord(self):  
        '''
        Starts recording sound.  If already recording, does nothing.
        '''
        
        if self.isRecording:
            return
        
        self.recData = []
        self.lastPos = 0
        self.rec.Start(self.sample, loopit=True)
        self.isRecording = True

    def stopRecord(self):
        '''
        Stops recording and returns sound bytes.  If not recording, does nothing.
        '''
        
        if not self.isRecording:
            return
        
        self.rec.Stop()
        self.isRecording = False
        self.grabAudio()
        soundBytes = ''.join(self.recData) # join all the chunks together into one string
        return soundBytes
    

    def playSoundFile(self, filePath, blocking = False):
        '''
        Plays specified file (wav, aiff, mp3, ogg, etc.) with or without blocking.
        '''
        
        self.src.Sound = pySonic.FileSample(filePath)
        self.src.Play()
        
        if not blocking:
            return
        
        while self.src.IsPlaying():
            pass
    
    def playSoundBytes(self, soundBytes, blocking = False, rate = RATE):
        '''
        Plays sound given in byte string with or without blocking at specified rate.
        '''
        
        self.src.Sound = pySonic.MemorySample(soundBytes, CHANNELS, BITS, rate)
        self.src.Play()
        
        if not blocking:
            return
        
        while self.src.IsPlaying():
            pass
    

    def stopPlay(self):
        '''
        Stops whatever sound is playing. If not playing, does nothing.
        '''
        
        if self.src.IsPlaying():
            self.src.Stop()
    
    def isPlaying(self):
        '''
        Returns True if a sound is being played.  Otherwise, False.
        '''
        
        return self.src.IsPlaying()
    

    def onTimer(self, event):
        '''
        Called every 1000 seconds.  If recording, this is when the buffer should be full.
        Audio in buffer is grabbed to make room for more.
        '''

        if self.isRecording:
            self.grabAudio()
        event.Skip()
        
    def speakText(self, text, blocking = False):
        '''
        Uses TTS to speak given text with or without blocking.
        '''
        
        soundBytes = self.speakTextToBytes(text)
        self.playSoundBytes(soundBytes, blocking)
        
    def speakTextFile(self, filepath, blocking = False):
        '''
        Uses TTS to speak text in given text file with or without blocking.
        '''
        
        text = file(filepath,'r').read()
        self.speakText(text, blocking)
    
    def speakTextFileToBytes(self, filepath):
        '''
        Uses TTS to get sound bytes of spoken text in given text file.
        '''
        
        text = file(filepath,'r').read()
        return self.speakTextToBytes(text)
    
    def speakTextToBytes(self, text):
        '''
        Uses TTS to get sound bytes of spoken text in given string.
        '''
        
        for word, phon in PRONUNCIATIONS:
            text = text.replace(word, phon)
        m = self.tts.SpeakToMemory(text)
        soundBytes = ''.join(m.GetData())
        return soundBytes
        

def soundFileToBytes(filePath):
    '''
    Resamples and normalizes sound file and returns bytes.
    '''
    
    soundBytes = resampleSoundFile(filePath)
    soundBytes = normalizeSoundBytes(soundBytes)
    return soundBytes


def normalizeSoundBytes(soundBytes):
    '''
    Normalizes sound bytes by finding the peak and scaling everything by it up to 
    the maximum amplitude.
    '''
    
    soundArray = fromstring(soundBytes, int16)
    m = max(abs(soundArray))
    soundArray = soundArray/float(m)*20000
    soundArray = array(soundArray,int16)
    return soundArray.tostring()

   
def resampleSoundFile(filePath):
    '''
    Resamples the sound file into the default sound properties specified in Constant
    and returns as bytes. Uses pymedia's built-in resampler.
    '''
           
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


def resampleSoundBytes(soundBytes, newRate, newChannels):
    '''
    Resamples a sound byte stream with the bitrate and num of channels specified.
    Uses pymedia's built-in resampler.
    '''
    
    resampler = sound.Resampler((RATE, CHANNELS),(newRate, newChannels))
    newBytes = resampler.resample(soundBytes)
    return newBytes


def encodeToMp3(soundBytes, fileName, bitRate = MP3_RATE):
    '''
    Encodes sound bytes into mp3 format using pymedia's built-in encoder.  
    The sound is expected to have the default sound properties specified in Constants.
    '''
    
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
    '''
    Finds duration (in min,sec) of sound bytes assuming properties in Constants (except
    assumes single channel).
    '''
    
    BITS_PER_BYTE = 8
    numBytes = len(soundBytes)
    numSamples = BITS_PER_BYTE * numBytes/BITS
    sec = numSamples/float(RATE)   
    min = int(sec/60)
    sec = sec%60
    return min,sec
        