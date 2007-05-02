''' Imports '''
import os
import shutil
from Student import *
from Constants import *

class Class:
    '''
    This class represents a set of <i>Students</i> and does the necessary file I/O that 
    they require.
    '''
     
    def __init__(self, students = []):
        '''
        Constructor
        '''
        self.students = students
        self.teacher = Student("Teacher")
    
    def __str__(self):
        '''
        For console output (system function)
        '''
        str = ''
        for i in range(len(self.students)):
            str += self.students[i] + ' '
    
    def __len__self(self):
        '''
        For length checking (system function)
        '''
        return len(self.students)
    
    def addStudent(self, student = Student()):
        '''
        Adds a student to the class and saves the class to disk.
        '''
        self.students.append(student)
        self.save()
    
    def delStudent(self,index):
        '''
        Removes a student from the class and moves the folder to a backup directory.
        '''
        dname = '_' + self.students[index].name
        self.students.pop(index)
        try:
            os.mkdir(BACKUP_DIR)
        except OSError:()
        
        i = 1
        while True:
            if not os.path.exists('%s%s_%d' % (BACKUP_DIR, dname, i)):
                break
            i += 1
            
        shutil.move(STUDENT_DIR + dname, '%s%s_%d' % (BACKUP_DIR, dname, i))
    
    def save(self):
        '''
        Saves the class to disk.
        '''
        try:
            os.mkdir(STUDENT_DIR + '_' + self.teacher.name)
        except OSError:()
        for i in range(len(self.students)):
            try:
                os.mkdir(STUDENT_DIR + '_' + self.students[i].name)
            except OSError:()
 
    def load(self, path = ''):
        '''
        Loads the class from disk.
        '''
        try:
            os.mkdir(STUDENT_DIR)
        except OSError:()
        directory = os.listdir(path + STUDENT_DIR)
        self.students = []
        for i in directory:
            if(i[0] == '_'):
                if i == '_Teacher':
                    self.teacher = Student(i[1:])
                else:
                    self.students.append(Student(i[1:]))

''' Handling an attempt at standalone running '''           
if __name__ == "__main__":
    print 'The class "Class" is not runnable.'
    