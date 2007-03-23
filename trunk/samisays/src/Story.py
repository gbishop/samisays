import cPickle

'''
' Class Name:  Story
' Description: Contains data structures and methods for a single
'              story made up of a title and multiple sound clips.
'              Sound clips are strings of bytes in wave format
'              witht the properties (bits, sample rate, etc.)
'              defined in the SoundControl class.
'''

STUDENT_DIR = 'students'
class Story:
    
    '''
    ' Constructor initializes Story object.  Current clip is title.
    '''
    def __init__(self, name='',student='',titleBytes = ''):
        self.name = name
        self.student = student
        self.clips = [titleBytes]
        self.currClip = 0
        self.pickleMe()
        
    '''
    ' Returns the number of clips currently in the story (including the title).
    '''   
    def __len__(self):
        return len(self.clips)
    
    '''
    ' Inserts clip after current clip and makes new clip the current clip.
    '''
    def insertClip(self, soundBytes):
        self.currClip += 1
        self.clips.insert(self.currClip,soundBytes)
        self.pickleMe()
    
    '''
    ' Replaces the first clip (the title) with new bytes.
    '''
    def replaceTitle(self, titleBytes):
        self.clips[0] = titleBytes
        self.pickleMe()
    
    '''
    ' Deletes the current clip, makes clip before deleted clip the current clip,
    ' and returns current clip.
    '''
    def deleteClip(self):
        if self.currClip > 0:
            del self.clips[self.currClip]
        self.currClip -= 1
        self.pickleMe()
        return self.getCurrClip()
    
    '''
    ' Returns the current clip.
    '''
    def getCurrClip(self):
        return self.clips[self.currClip]
    
    '''
    ' If not on the last clip, makes the next clip the current clip and returns it.  
    ' If on the last clip, returns the current clip.
    '''
    def getNextClip(self):
        if self.currClip < len(self.clips)-1:
            self.currClip += 1
        return self.getCurrClip()
    
    '''
    ' If not on the first clip, makes the previous clip the current clip and returns it.
    ' If on the first clip, returns the current clip.
    '''
    def getPreviousClip(self):
        if self.currClip > 0:
            self.currClip -= 1
        return self.getCurrClip()
    
    '''
    ' Returns the first clip (title).
    '''
    def getTitle(self):
        return self.clips[0]
    
    '''
    ' Joins the story into a single byte string and returns it.
    '''
    def getStory(self):
        return ''.join(self.clips)
    
    '''
    ' Returns True if the title is empty.  Otherwise, returns False.
    '''
    def needsTitle(self):
        return self.clips[0] == ''
    
    def pickleMe(self):
        fileName = '%s/_%s/%s.pkl' % (STUDENT_DIR,self.student,self.name)
        f = file(fileName,'w')
        p = cPickle.Pickler(f)
        p.dump(self)
        f.close()
        