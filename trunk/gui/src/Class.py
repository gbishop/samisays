# Imports
import cPickle as pickle
import os
import shutil
from Student import Student

# No magic in my code!
STUDENT_DIR = 'students\\'
BACKUP_DIR = STUDENT_DIR + 'removed\\'
FILE_EXTENSION = '.pkl'
 
class Class:
     
    def __init__(self, students = []):
        self.students = students
        
    def __str__(self):
        str = ''
        for i in range(len(self.students)):
            str += self.students[i] + ' '
    
    def addStudent(self, student = Student()):
        self.students.append(student)
        self.save()
        
    def delStudent(self,index):
        fname = self.students[index].name + FILE_EXTENSION
        self.students.pop(index)
        try:
            os.mkdir(BACKUP_DIR)
        except OSError:()
        shutil.move(STUDENT_DIR + fname, BACKUP_DIR + fname);
        
    def save(self):
        for i in range(len(self.students)):
            f = file(STUDENT_DIR + self.students[i].name + FILE_EXTENSION, 'w')
            pickle.dump(self.students[i],f)
            f.close()
            
    def load(self, path = '.\\' + STUDENT_DIR):
        directory = os.listdir(path)
        pickles = []
        for item in directory:
            if item.endswith('.pkl'):
                pickles.append(item)
        self.students = []
        for i in pickles:
            f = file(path + i,'r')
            self.students.append(pickle.load(f))
            f.close()
            
if __name__ == "__main__":
    print 'The class "Class" is not runnable.'
    