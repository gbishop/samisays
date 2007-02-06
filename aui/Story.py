class Story:
    
    def __init__(self, titleBytes = ''):
        self.clips = [titleBytes]
        self.currClip = 0
    
    def insertClip(self, soundBytes):
        self.currClip += 1
        self.clips.insert(self.currClip,soundBytes)
    
    def replaceTitle(self, titleBytes):
        self.clips[0] = titleBytes
    
    def deleteClip(self):
        if self.currClip > 0:
            del self.clips[self.currClip]
        self.currClip -= 1
        return self.getCurrClip()
    
    def getCurrClip(self):
        return self.clips[self.currClip]
    
    def getNextClip(self):
        if self.currClip < len(self.clips)-1:
            self.currClip += 1
        return self.getCurrClip()
        
    def getPreviousClip(self):
        if self.currClip > 0:
            self.currClip -= 1
        return self.getCurrClip()
    
    def getTitle(self):
        return self.clips[0]
    
    def getStory(self):
        return ''.join(self.clips)
    
    def getNumClips(self):
        return len(self.clips)
    
    def needsTitle(self):
        return self.clips[0] == ''