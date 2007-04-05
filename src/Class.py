# Imports
import os
import shutil
from Student import Student

# No magic in my code!
STUDENT_DIR = 'students/'
BACKUP_DIR = STUDENT_DIR + 'removed/'
 
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
        dname = '_' + self.students[index].name
        self.students.pop(index)
        try:
            os.mkdir(BACKUP_DIR)
        except OSError:()
        shutil.move(STUDENT_DIR + dname, BACKUP_DIR + dname);
        
    def save(self):
        for i in range(len(self.students)):
            try:
                os.mkdir(STUDENT_DIR + '_' + self.students[i].name);
            except OSError:()
            
    def load(self, path = ''):
        try:
            os.mkdir(STUDENT_DIR)
        except OSError:()
        directory = os.listdir(path + STUDENT_DIR)
        self.students = []
        for i in directory:
            if(i[0] == '_'):
                self.students.append(Student(i[1:]))
            
if __name__ == "__main__":
    print 'The class "Class" is not runnable.'
    