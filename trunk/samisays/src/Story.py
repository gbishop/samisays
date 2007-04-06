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
    def __init__(self, name='', student='', titleBytes = '', lockedTitle = False):
        self.name = name
        self.student = student
        self.clips = [titleBytes]
        self.locks = [lockedTitle]
        self.breaks = [True]
        self.currClip = 0
        self.lastDelete = ''
        self.pickleMe()
        
    '''
    ' Returns the number of clips currently in the story (including the title).
    '''   
    def __len__(self):
        return len(self.clips)
    
    '''
    ' Inserts clip after current clip and makes new clip the current clip.
    '''
    def insertClip(self, soundBytes, isBreak = False, locked = False):
        self.currClip += 1
        self.clips.insert(self.currClip, soundBytes)
        self.locks.insert(self.currClip, locked)
        self.breaks.insert(self.currClip, isBreak)
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
        if self.locks[self.currClip]:
            return
        if self.currClip > 0:
            self.lastDelete = self.clips[self.currClip]
            del self.clips[self.currClip]
            del self.locks[self.currClip]
            del self.breaks[self.currClip]
        self.currClip -= 1
        self.pickleMe()
        return self.getCurrClip()
    
    '''
    ' Locks all clips in the story.
    '''
    def lockStory(self):
        self.locks = [True for i in xrange(len(self))]
    
    '''
    ' Merges all clips between breaks into single clips.  Includes break sound if
    ' specified.  Locks all clips in newly merged story (otherwise, would need to handle
    ' conditions for when some clips between a break are locked and some aren't).
    '''
    def mergeAndLockBreaks(self, includeBreakClip):
        mergedClips = []
        lastBreak = 0
        mergedClips = [self.getTitleBytes()]
        for i in xrange(1, len(self)):
            if self.breaks[i] or i == len(self)-1:
                if includeBreakClip:
                    mergedClips += [''.join(self.clips[lastBreak+1:i+1])]
                else:
                    mergedClips += [''.join(self.clips[lastBreak+1:i])]
                lastBreak = i
        
        self.clips = mergedClips
        self.lockStory()
    
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
    def getTitleBytes(self):
        return self.clips[0]
    
    '''
    ' Joins the story into a single byte string and returns it.
    '''
    def getStoryBytes(self):
        return ''.join(self.clips)
    
    '''
    ' Creates and returns a copy of this story object using the specified name and student.
    '''
    def getCopy(self, student):
        copy = Story(self.name, student)
        copy.clips = [c for c in self.clips]
        copy.locks = [l for l in self.locks]
        copy.breaks = [b for b in self.breaks]
        return copy
        
    
    '''
    ' Returns True if the title is empty.  Otherwise, returns False.
    '''
    def needsTitle(self):
        return self.clips[0] == ''
    
    def clipIsLocked(self):
        return self.locks[self.currClip]
    
    def clipIsBreak(self):
        return self.breaks[self.currClip]
    
    def pickleMe(self):
        filepath = '%s/_%s/%s.pkl' % (STUDENT_DIR, self.student, self.name)
        f = file(filepath,'w')
        p = cPickle.Pickler(f)
        p.dump(self)
        f.close()
        
def unpickleStory(name, student):
    filepath = '%s/_%s/%s.pkl' % (STUDENT_DIR, student, name)
    f = file(filepath,'r')
    return cPickle.load(f)
        