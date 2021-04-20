"""

@author - Swayam Shah
@CWID - 10471353

"""

from collections import  defaultdict
from prettytable import PrettyTable
import os
from typing import Dict, List, DefaultDict, Set
from HW08_Swayam_Shah import file_reader

class Student:
    """ Class to store student records """

    def __init__(self,cwid: str,name: str,major: str) -> None:
        """ Function to Initiaize class Student """

        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: Dict[str, str] = DefaultDict(int)
    
    def stu_add(self, course: str, grade: str) -> None:
        """ Function to add course and grade to Student record """

        self.courses[course] = grade

    def display(self) -> List[str]:
        """ Function to return values to the student summary table """
        
        return [self.cwid, self.name, sorted(self.courses.keys())]

class Instructor:
    """ Class to store instructor records """

    def __init__(self,cwid: str,name: str,dept: str) -> None:
        """ Function to Initiaize class Instructor """

        self.cwid: str = cwid
        self.name: str = name 
        self.dept: str = dept
        self.setcourse: Set = set()
        self.courses: defaultdict = defaultdict(int)

    def instruc_add(self, course: str) -> None:
        """ Function to add course to the Instructor record """
    
        self.setcourse.add(course)
        self.courses[course] += 1

    def display(self) -> List[str]:
        """ Function to return values to the instructor summary table """
        
        for course, count in self.courses.items():
            yield [self.cwid, self.name, self.dept, course, count]

class University:
    """ Class to store student,instructor and grade records """

    def __init__(self,path:str) -> None:
        """ Function to Initiaize class University """

        self.students: defaultdict =defaultdict(list)
        self.instructors: dict =dict()             
        self.path: str = path
        self.insert_student()
        self.insert_instructor()
        self.insert_grade()
        self.stu_summary()
        self.ins_summary()

    def insert_student(self) -> None:
        """ Function to add student records """
        try:
            for cwid, name, major in file_reader(os.path.join(
                    self.path, "students.txt"), fields=3, sep='\t', header=False):
                if cwid in self.students:
                    raise KeyError("Student with CWID is already in the file")
                self.students[cwid] = Student(
                    cwid, name, major)
        except FileNotFoundError:
                print(f"Cannot open file at {self.path}")
        except ValueError:
                print("Missing field")
            
    

    def insert_instructor(self) -> None:    
        """ Function to add instructor records """

        try:
            for cwid, name, dept in file_reader(os.path.join(
                    self.path, "instructors.txt"), fields=3, sep='\t', header=False):
                if cwid in self.instructors:
                    raise KeyError(
                        "Instructor with CWID is already in the file")
                self.instructors[cwid] = Instructor(cwid, name, dept)
        except (FileNotFoundError, ValueError) as e:
            print(f"Cannot open file at {self.path}")
        except ValueError:
            print("Missing field")
                   
                
    def insert_grade(self) -> None:
        """ Function to add grade records """

        try:
            for a, b, c, d in file_reader(
                    os.path.join(self.path, "grades.txt"), fields=4, sep='\t', header=False):
                if a in self.students:
                    
                    s: Student = self.students[a]
                    s.stu_add(course=b, grade=c)

                else:
                    raise KeyError(f"No such Student with {a}")
                if d in self.instructors:
                    
                    p: Instructor = self.instructors[d]
                    p.instruc_add(b)
                else:
                    raise KeyError(f"No such Student with {d}")

        except FileNotFoundError:
            print(f"Cannot open file at {self.path}")
        except ValueError:
            print("Wrong input")
        
    def stu_summary(self):
        """ Function to print student records """

        pt: PrettyTable = PrettyTable(
            field_names=[
                'CWID',
                'Name',
                'Courses',])    
        
        for s in self.students.values():
            pt.add_row(s.display())
              
        print(pt) 

    def ins_summary(self):
        """ Function to print instructor records """

        pt: PrettyTable = PrettyTable(
            field_names=[
                'CWID',
                'Name',
                'Department',
                'Course',
                'Students'])    
        
        for s in self.instructors.values():
            for row in s.display():
                pt.add_row(row) 
                
        print(pt) 

def main():
    University("C://Users/Swayam/Documents/Downloads")    

if __name__ == '__main__':
    main()  


    
