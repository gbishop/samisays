import os
from Constants import *

class Student:
    
    def __init__(self, name = 'Sami'):
        '''
        Constructor initializes Student object.
        '''
        self.name = name
        self.stories = [] # list of story names
        
    def __str__(self):
        '''
        Returns string version of object (student name and number of stories).
        '''
        return self.name + ' ' + str(len(self.stories))
    
    def getName(self):
        '''
        Returns student name.
        '''
        return self.name
    
    def getStories(self):
        '''
        Returns list of names of student's stories.
        '''
        return self.stories
    
    def setName(self, name):
        '''
        Sets student's name.
        '''
        self.name = name
    
    def setStories(self, stories):
        '''
        Sets student's story list.
        '''
        self.stories = stories
        
    def addStory(self,story):
        '''
        Adds a story (name) to the end of the student's story list.
        '''
        self.stories.append(story)
    
    def delStory(self,index):
        '''
        Deletes the story at position index from the list.
        '''
        self.stories.pop(index)
        
    def loadNames(self,path):
        '''
        Populates the student's list of stories with the names of the student's
        stories.  Does so by reading the names of the pickled stories in the student's
        folder.
        '''
        self.stories = []
        directory = os.listdir(path)
        for i in directory:
            if i[-3:] == 'pkl':
                self.addStory(i[:-4])
         
if __name__ == "__main__":
    print 'The class "Student" is not runnable'
