import cPickle as pickle

class Student:
    
    def __init__(self, name = 'Sami'):
        self.name = name
        self.stories = [];
        
    def __str__(self):
        return self.name + ' ' + str(len(self.stories))
    
    def getName(self):
        return self.name
    
    def getStories(self):
        return self.stories
    
    def setName(self, name):
        self.name = name
    
    def setStories(self, stories):
        self.stories = stories
        
    def addStory(self,story):
        self.stories.append(story)
    
    def delStory(self,index):
        self.stories.pop(index)
         
