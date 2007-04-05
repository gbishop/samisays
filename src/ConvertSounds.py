import os
from SoundControl import *

INSTR_DIR = 'instr_sounds/'
SOUND_DIR = 'sound_library/'

w = pySonic.World()

instrList = os.listdir(INSTR_DIR)
for file in instrList:
    if file[-3:] == 'wav':
        bytes = resampleSoundFile(INSTR_DIR + file)
        bytes = normalizeSoundBytes(bytes)
        encodeToMp3(bytes,INSTR_DIR + file[0:-3] + 'mp3',128000)

catList = os.listdir(SOUND_DIR)
for cat in catList:
    soundList = os.listdir(SOUND_DIR + cat)
    for file in soundList:
        if file[-3:] == 'wav' or file[-3:] == 'mp3':
            bytes = resampleSoundFile(SOUND_DIR + cat + '/' + file)
            bytes = normalizeSoundBytes(bytes)
            encodeToMp3(bytes,SOUND_DIR + cat + '/' + file[0:-3] + 'mp3',128000)