import cPickle
import zlib
import numpy
import threading
from Constants import *


class Story:
    '''
    Contains data structures and methods for a single
    story made up of a title and multiple sound clips.
    Sound clips are strings of bytes in wave format
    with the properties (bits, sample rate, etc.)
    defined in Contants.  Mutual exclusion is sometimes
    required due to save threading (see PickleThread class).
    '''
    
    def __init__(self, name='', student='', titleBytes = ''):
        '''
        Constructor initializes Story object.  Current clip is title.
        '''
        self.name = name # text name of story
        self.student = student # name of student
        self.zipClips = [zlib.compress(titleBytes)] # Holds compressed soundbytes of story clips
        self.types = [NON] # Holds type of each story clip
        self.currClip = 0
        self.trash = [] # Deleted clips since opened
        self.justTitle = False # Flag for .ttl file
        
    
    def initializeLocks(self):
        '''
        Initializes the locks and semaphore to be used for save threading (see PickleThread class).
        '''
        
        self.pickleMutex = threading.Lock()
        self.storyMutex = threading.Lock()
        self.threadSem = threading.Semaphore(2)
    
       
    def __len__(self):
        '''
        Returns the number of clips currently in the story (including the title).
        '''
        
        return len(self.zipClips)
    

    def insertClip(self, soundBytes, type):
        '''
        Inserts clip after current clip and makes new clip the current clip. Requires mutual exclusion.
        '''
        
        self.storyMutex.acquire()
        self.currClip += 1
        self.zipClips.insert(self.currClip, zlib.compress(soundBytes))
        self.types.insert(self.currClip, type)
        self.storyMutex.release()
        self.pickleMe()

  
    def replaceTitle(self, titleBytes):
        '''
        Replaces the first clip (the title) with new bytes. Requires mutual exclusion.
        '''

        self.storyMutex.acquire()
        self.zipClips[0] = zlib.compress(titleBytes)
        self.storyMutex.release()
        self.pickleMe()
        self.pickleTitle()
    
 
    def deleteClip(self):
        '''' 
        Deletes the current clip, makes clip before deleted clip the current clip,
        and returns current clip. Requires mutual exclusion.
        '''
        
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
        '''
        Adds a sound file to the top of the trash can.
        '''
        
        if len(self.trash) == MAX_TRASH_SIZE:
            del self.trash[MAX_TRASH_SIZE-1]
        self.trash = [zipClip] + self.trash
    
    def lockStory(self):
        '''
        Locks all clips in the story. Requires mutual exclusion.
        '''
        
        self.storyMutex.acquire()
        self.types = [LCK for i in xrange(len(self))]
        self.storyMutex.release()
    
    
    def mergeBreaksAndLock(self, includeBreakClip):
        '''
        Merges all clips between breaks into single clips.  Includes break sound if
        specified.  Locks all clips in newly merged story (otherwise, would need to handle
        conditions for when some clips between a break are locked and some aren't).
        '''
        
        mergedClips = []
        lastBreak = 0
        clips = self.decompressStory()
        mergedClips = [self.getTitleBytes()]
        for i in xrange(1, len(self)):
            if self.types[i] == BRK or i == len(self)-1:
                if includeBreakClip: # include beeps
                    mergedClips += [''.join(clips[lastBreak+1:i+1])]
                else: # exclude beeps
                    mergedClips += [''.join(clips[lastBreak+1:i])]
                lastBreak = i
        
        self.zipClips = [compress(clip) for clip in mergedClips]
        self.lockStory()
    
    def getCurrClip(self):
        ''' 
        Returns the current clip.
        '''
        
        return decompress(self.zipClips[self.currClip])
    
    
    def getNextClip(self):
        ''' 
        If not on the last clip, makes the next clip the current clip and returns it.  
        If on the last clip, returns the current clip.
        '''
        
        if self.currClip < len(self)-1:
            self.currClip += 1
        return self.getCurrClip()
    
  
    def getPreviousClip(self):
        ''' 
        If not on the first clip, makes the previous clip the current clip and returns it.
        If on the first clip, returns the current clip.
        '''
        
        if self.currClip > 0:
            self.currClip -= 1
        return self.getCurrClip()
    
   
    def getTitleBytes(self):
        ''' 
        Returns the first clip (title).
        '''
        
        #return self.clips[0]
        return decompress(self.zipClips[0])
    
    
    def getStoryBytes(self):
        '''
        Joins the story into a single byte string and returns it.
        '''
        
        clips = self.decompressStory()
        return ''.join(clips)
    

    def getCopy(self, student):
        ''' 
        Creates and returns a copy of this story object using the specified name and student.
        '''
        
        copy = Story(self.name, student, '')
        copy.zipClips = [z for z in self.zipClips]
        copy.types = [t for t in self.types]
        return copy
        
    def getTrash(self):
        '''
        Returns a decompressed version of the trash list.
        '''
        
        trash = []
        for t in self.trash:
            trash += [decompress(t)]
        return trash
    
    def getStats(self):
        '''
        Returns an array with the counts of each clip type in the story.
        '''
        
        stats = numpy.zeros(6)
        for t in self.types[1:]:
            stats[t] += 1
        return stats
    

    def needsTitle(self):
        ''' 
        Returns True if the title is empty.  Otherwise, returns False.
        '''
        
        return zlib.decompress(self.zipClips[0]) == ''
    
    def hasTrash(self):
        '''
        Returns True if trash is not empty (i.e. a clip has been deleted since the story was opened).
        '''
        
        return self.trash != []
    
    def clipIsLocked(self):
        '''
        Returns True if the current clip is locked.
        '''
        
        return self.types[self.currClip] == LCK
    
    def clipIsBreak(self):
        '''
        Returns true if the current clip is a break.
        '''
        
        return self.types[self.currClip] == BRK
    
    def clipIsTitle(self):
        '''
        Returns true if the current clip is the title (first clip).
        '''
        
        return self.currClip == 0
    
    def decompressStory(self):
        '''
        Returns a decompressed version of the clip list.
        '''
        
        clips = []
        for clip in self.zipClips:
            clips += [decompress(clip)]
        return clips
    
    def pickleTitle(self):
        '''
        Pickles the title of the story for quick access (blocking only).
        '''
        
        title = Story(self.name, self.student)
        title.zipClips[0] = self.zipClips[0] # Copy title
        title.types[0] = self.types[0] # Copy title type
        title.justTitle = True
        filepath = '%s_%s/%s.ttl' % (STUDENT_DIR, self.student, self.name)
        f = file(filepath,'w')
        p = cPickle.Pickler(f)
        p.dump(title)
        f.close()
    
    def pickleMe(self, blocking = False):
        '''
        Pickles the story object.  If blocking == False, and there is not already a PickleThread waiting to
        begin pickling, spawns a PickleThread.  Otherwise, does nothing.  If blocking==True, makes a copy
        of the story and pickles it.
        '''
        
        if blocking:
            copy = self.getCopy(self.student)
            pickleStory(copy)
        elif self.threadSem.acquire(blocking = False): # check if less than two threads are spawned
            ps = PickleStory(self)
            ps.start()
        
            
    def loadFullStory(self):
        '''
        If self is the full story returns self.  If self only has the title, loads (unpickles) 
        the full story and returns the full story.  In either case, initializes mutex locks before
        returning.
        '''
        
        if self.justTitle:
            story = unpickleStory(self.name, self.student)
        else:
            story = self
        story.initializeLocks()
        return story

            
        
def unpickleTitle(name, student):
    '''
    Unpickles and returns the justTitle version of the story specified by the text story name and student name.
    '''
    
    filepath = '%s/_%s/%s.ttl' % (STUDENT_DIR, student, name)
    f = file(filepath,'r')
    return cPickle.load(f)
    
def pickleStory(story):
    '''
    Pickles the given (full) story in the student's directory.
    '''
    
    filepath = '%s/_%s/%s.pkl' % (STUDENT_DIR, story.student, story.name)
    f = file(filepath,'w')
    p = cPickle.Pickler(f)
    p.dump(story)
    f.close()

def unpickleStory(name, student):
    '''
    Unpickles and returns the (full) story specified by the text story name and student name.
    '''
    
    filepath = '%s_%s/%s.pkl' % (STUDENT_DIR, student, name)
    f = file(filepath,'r')
    return cPickle.load(f)

def compress(byteString):
    '''
    Returns zlib compressed version of bytestring.
    '''
    
    return zlib.compress(byteString, COMPRESS_RATE)

def decompress(byteString):
    '''
    Returns decompressed version of bytestring (using zlib).
    '''
    
    return zlib.decompress(byteString)


class PickleStory(threading.Thread):
    '''
    This threaded class is used to allow for nonblocking pickles (saves) of a story.  A maximum
    of two of these treads are necessary at any one time (as is ensured in pickleMe).  One thread
    may be pickling at a time and possibly another waiting.  The thread waits to copy the story
    until it is about to pickle so any save requested after a waiting thread is spawned and 
    before it acquires the pickling lock will be covered by that thread.
    '''
    
    def __init__(self, story):
        ''' Constructor initializes thread.'''
        self.story = story
        threading.Thread.__init__(self)
    

    def run(self):
        '''
        Once the pickling lock is acquired, a copy is made of the story, the story is pickled, and
        the lock released.  Before a copy occurs, the story lock must be acquired.  It is released
        after to allow story creation to continue.
        '''
        story = self.story
        story.pickleMutex.acquire()
        story.storyMutex.acquire()
        copy = story.getCopy(story.student)
        story.storyMutex.release()
        pickleStory(copy)
        story.threadSem.release()
        story.pickleMutex.release()

         
        