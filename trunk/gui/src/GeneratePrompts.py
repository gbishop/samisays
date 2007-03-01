import pyTTS

PROMPT_FILE = 'prompts.txt'

tts = pyTTS.Create()

f = open(PROMPT_FILE,'r')
g = 0
names = []
text = []
for i in f.readlines():
    if g == 0:
        text.append(i)
        g = 1
    else:
        names.append(i)
        g = 0

for i in range(len(names)):
    tts.SpeakToWave(names[i][:-1],text[i][:-1])
