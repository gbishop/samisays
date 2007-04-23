import pymedia.audio.sound as sound
import os
from Story import *

directory = 'e:/documents/sami story backup/'
resampler = sound.Resampler((44100, 2),(16000, 2))

for student in os.listdir(directory):
    studentName = student[1:]
    print studentName
    for story in os.listdir(directory+student):
        s = cPickle.load(file('%s%s/%s' %(directory, student, story),'r'))
        n = Story(s.name, s.student)
        n.types = s.types
        n.initializeLocks()
        n.zipClips = []
        for clip in s.clips:
            n.zipClips += [compress(resampler.resample(clip))]
        n.pickleTitle()
        n.pickleMe(True)