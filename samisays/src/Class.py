''' Imports '''
import os
import shutil
from Student import *
from Constants import *

'''
' Class Name: Class
' Description: This class represents a set of students and does the necessary file
'              I/O that they require.
'''
class Class:
     
    '''
    ' Constructor
    '''
    def __init__(self, students = []):
        self.students = students
        self.teacher = Student("Teacher")
    
    '''
    ' __str__ - For console output (system function)
    '''
    def __str__(self):
        str = ''
        for i in range(len(self.students)):
            str += self.students[i] + ' '
    
    '''
    ' __len__ - For length checking (system function)
    '''
    def __len__self(self):
        return len(self.students)
    
    '''
    ' addStudent - Adds a student to the class and saves the class to disk.
    '''
    def addStudent(self, student = Student()):
        self.students.append(student)
        self.save()
    
    '''
    ' delStudent - Removes a student from the class and moves the folder to a backup
    '              directory.
    '''
    def delStudent(self,index):
        dname = '_' + self.students[index].name
        self.students.pop(index)
        try:
            os.mkdir(BACKUP_DIR)
        except OSError:()
        shutil.move(STUDENT_DIR + dname, BACKUP_DIR + dname);
    
    '''
    ' save - Saves the class to disk.
    '''
    def save(self):
        try:
            os.mkdir(STUDENT_DIR + '_' + self.teacher.name)
        except OSError:()
        for i in range(len(self.students)):
            try:
                os.mkdir(STUDENT_DIR + '_' + self.students[i].name)
            except OSError:()
     
    '''
    ' load - Loads the class from disk.
    '''
    def load(self, path = ''):
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
    