import pyTTS

tts = pyTTS.Create()

#write to a wave file
tts.SpeakToWave('spain.wav', 'The rain in Spain falls mainly on the plain.')
