import cPickle
import zlib
import numpy
import threading
from Constants import *


class Story:
    '''Contains data structures and methods for a single
    story made up of a title and multiple sound clips.
    Sound clips are strings of bytes in wave format
    with the properties (bits, sample rate, etc.)
    defined in the SoundControl class.'''
    
    def __init__(self, name='', student='', titleBytes = ''):
        '''Constructor initializes Story object.  Current clip is title.'''
        self.name = name
        self.student = student
        self.zipClips = [zlib.compress(titleBytes)]
        self.types = [NON]
        self.currClip = 0
        self.trash = []
        self.justTitle = False
        
    
    def initializeLocks(self):
        self.pickleMutex = threading.Lock()
        self.storyMutex = threading.Lock()
        self.threadSem = threading.Semaphore(2)
    
       
    def __len__(self):
        ''' Returns the number of clips currently in the story (including the title).'''
        return len(self.zipClips)
    

    def insertClip(self, soundBytes, type):
        '''Inserts clip after current clip and makes new clip the current clip.'''
        self.storyMutex.acquire()
        self.currClip += 1
        self.zipClips.insert(self.currClip, zlib.compress(soundBytes))
        self.types.insert(self.currClip, type)
        self.storyMutex.release()
        self.pickleMe()

  
    def replaceTitle(self, titleBytes):
        '''Replaces the first clip (the title) with new bytes.'''
        #self.clips[0] = titleBytes
        self.storyMutex.acquire()
        self.zipClips[0] = zlib.compress(titleBytes)
        self.storyMutex.release()
        self.pickleMe()
        self.pickleTitle()
    
 
    def deleteClip(self):
        '''' Deletes the current clip, makes clip before deleted clip the current clip,
        and returns current clip.'''
        
        if self.types[self.currClip] == LCK:
            return
        self.storyMutex.acquire()
        if self.currClip > 0:
            self.addToTrash(self.zipClips[self.currClip])
            del self.zipClips[self.currClip]
            del self.types[self.currClip]
        self.currClip -= 1
        self.storyMutex.release()
        self.pickleMe()
        return self.getCurrClip()
    
    
    def addToTrash(self, zipClip):
        '''Adds a sound file to the trash can'''
        if len(self.trash) == MAX_TRASH_SIZE:
            del self.trash[MAX_TRASH_SIZE-1]
        self.trash = [zipClip] + self.trash
    
    def lockStory(self):
        ''' Locks all clips in the story.'''
        self.types = [LCK for i in xrange(len(self))]
    
    
    def mergeAndLockBreaks(self, includeBreakClip):
        '''' Merges all clips between breaks into single clips.  Includes break sound if
        specified.  Locks all clips in newly merged story (otherwise, would need to handle
        conditions for when some clips between a break are locked and some aren't)'''
        
        mergedClips = []
        lastBreak = 0
        clips = self.decompressStory()
        mergedClips = [self.getTitleBytes()]
        for i in xrange(1, len(self)):
            if self.types[i] == BRK or i == len(self)-1:
                if includeBreakClip:
                    mergedClips += [''.join(clips[lastBreak+1:i+1])]
                else:
                    mergedClips += [''.join(clips[lastBreak+1:i])]
                lastBreak = i
        
        #self.clips = mergedClips
        self.zipClips = [compress(clip) for clip in mergedClips]
        self.lockStory()
    
    def getCurrClip(self):
        ''' Returns the current clip.'''
        return decompress(self.zipClips[self.currClip])
    
    
    def getNextClip(self):
        ''' If not on the last clip, makes the next clip the current clip and returns it.  
        If on the last clip, returns the current clip.'''
        if self.currClip < len(self)-1:
            self.currClip += 1
        return self.getCurrClip()
    
  
    def getPreviousClip(self):
        ''' If not on the first clip, makes the previous clip the current clip and returns it.
        If on the first clip, returns the current clip.'''
        if self.currClip > 0:
            self.currClip -= 1
        return self.getCurrClip()
    
   
    def getTitleBytes(self):
        ''' Returns the first clip (title).'''
        #return self.clips[0]
        return decompress(self.zipClips[0])
    
    
    def getStoryBytes(self):
        '''Joins the story into a single byte string and returns it.'''
        clips = self.decompressStory()
        return ''.join(clips)
    

    def getCopy(self, student):
        ''' Creates and returns a copy of this story object using the specified name and student.'''
        copy = Story(self.name, student, '')
        #copy.clips = [c for c in self.clips]
        copy.zipClips = [z for z in self.zipClips]
        copy.types = [t for t in self.types]
        return copy
        
    def getTrash(self):
        trash = []
        for t in self.trash:
            trash += [decompress(t)]
        return trash
    
    def getStats(self):
        stats = numpy.zeros(6)
        for t in self.types[1:]:
            stats[t] += 1
        return stats
    

    def needsTitle(self):
        ''' Returns True if the title is empty.  Otherwise, returns False.'''
        return zlib.decompress(self.zipClips[0]) == ''
    
    def hasTrash(self):
        return self.trash != []
    
    def clipIsLocked(self):
        return self.types[self.currClip] == LCK
    
    def clipIsBreak(self):
        return self.types[self.currClip] == BRK
    
    def clipIsTitle(self):
        return self.currClip == 0
    
    def decompressStory(self):
        clips = []
        for clip in self.zipClips:
            clips += [decompress(clip)]
        return clips
    
    def pickleTitle(self):
        title = Story(self.name, self.student)
        title.zipClips[0] = self.zipClips[0]
        title.types[0] = self.types[0]
        title.justTitle = True
        filepath = '%s_%s/%s.ttl' % (STUDENT_DIR, self.student, self.name)
        f = file(filepath,'w')
        p = cPickle.Pickler(f)
        p.dump(title)
        f.close()
    
    def pickleMe(self, blocking = False):
        if blocking:
            copy = self.getCopy(self.student)
            pickleStory(copy)
        elif self.threadSem.acquire(blocking = False):
            ps = PickleStory(self)
            ps.start()
        
            
    def loadFullStory(self):
        if self.justTitle:
            story = unpickleStory(self.name, self.student)
        else:
            story = self
        story.initializeLocks()
        return story

            
        
def unpickleTitle(name, student):
    filepath = '%s/_%s/%s.ttl' % (STUDENT_DIR, student, name)
    f = file(filepath,'r')
    return cPickle.load(f)
    
def pickleStory(story):
    filepath = '%s/_%s/%s.pkl' % (STUDENT_DIR, story.student, story.name)
    f = file(filepath,'w')
    p = cPickle.Pickler(f)
    p.dump(story)
    f.close()

def unpickleStory(name, student):
    filepath = '%s_%s/%s.pkl' % (STUDENT_DIR, student, name)
    f = file(filepath,'r')
    return cPickle.load(f)

def compress(byteString):
    return zlib.compress(byteString, COMPRESS_RATE)

def decompress(byteString):
    return zlib.decompress(byteString)


class PickleStory(threading.Thread):
    
    def __init__(self, story):
        ''' Constructor initializes thread.'''
        self.story = story
        threading.Thread.__init__(self)
    

    def run(self):
        story = self.story
        story.pickleMutex.acquire()
        story.storyMutex.acquire()
        copy = story.getCopy(story.student)
        story.storyMutex.release()
        pickleStory(copy)
        story.threadSem.release()
        story.pickleMutex.release()

         
        