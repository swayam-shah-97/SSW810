"""

@author - Swayam Shah
@CWID - 10471353

"""

from collections import  defaultdict
from prettytable import PrettyTable
import os
import sqlite3
from typing import Dict, List, DefaultDict, Set
from HW08_Swayam_Shah import file_reader

class Student:
    """ Class to store student records """

    def __init__(self,cwid: str,name: str,major: str,required: List[str],electives: List[str]) -> None:
        """ Function to Initiaize class Student """

        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: Dict[str, str] = DefaultDict(int)
        self.courses_fail: Dict[str, str] = dict()
        self.remaining_required: List[str] = required
        self.remaining_electives: List[str] = electives
        self.fail: List[str] = ["C-", "D+", "D", "D-", "F"]
        self.grade: Dict[str, float] = {"A": 4.0, "A-": 3.75, "B+": 3.25,
                                         "B": 3.0, "B-": 2.75, "C+": 2.25,
                                         "C": 2.0, "C-": 0.0, "D+": 0.0,
                                         "D": 0.0, "D-": 0.0, "F": 0.0}

    def stu_add(self, course: str, grade: str) -> None:
        """ Function to add course and grade to Student record """

        if grade not in self.fail:
            self.courses[course] = grade
        if grade in self.fail:
            self.courses_fail[course] = grade
            return
        if course in self.remaining_required:
            self.remaining_required.remove(course)
        if course in self.remaining_electives:
            self.remaining_electives.clear()

    def gpa(self) -> float:
       
        g: List[float] = list()
        for i in self.courses.values():
            if i in self.grade:
                g.append(self.grade[i])
            else:
                print("Invalid grade")
        for i in self.courses_fail.values():
            if i in self.grade:
                g.append(self.grade[i])
            else:
                print("Invalid grade")
        if len(g) == 0:
            return 0.0
        else:
            gpa: float = sum(g)/len(g)
        return format(gpa, '.2f')

    def display(self) -> List[str]:
        """ Function to return values to the student summary table """
        return [self.cwid, self.name, self.major,
                sorted(self.courses.keys()),
                sorted(self.remaining_required),
                sorted(self.remaining_electives),
                self.gpa()]   

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

class Major:
    """In this class, we will be creating an instance of Major.
    """
    #__slots__ = ['_major', '_required', '_electives']
    

    def __init__(self, major: str) -> None:
        """Here we will be initializing the variables.
        Args:
            major (str)
        """
        self.major: str = major
        self.required: List[str] = list()
        self.electives: List[str] = list()

    def major_add(self, type: str, course: str) -> None:
        """In this method, we will add course based on type (Required/Elective).
        Args:
            type (str): Course type (Required / Elective)
            course (str)
        """
        if type == "R":
            self.required.append(course)
        elif type == "E":
            self.electives.append(course)
        else:
            pass

    def req(self) -> List[str]:
        """In this functions, we will return the required courses.
        """
        return list(self.required)

    def elec(self) -> List[str]:
        """In this functions, we will return the elective courses.
        """
        return list(self.electives)

    def display(self) -> List[str]:
        """
        In this function, we will be returning the outputs.
        """
        return [self.major, self.required, self.electives]

    



class University:
    """ Class to store student,instructor and grade records """

    def __init__(self,path:str,dbpath: str) -> None:
        """ Function to Initiaize class University """

        self.students: defaultdict =defaultdict(list)
        self.instructors: dict =dict()             
        self.path: str = path
        self.dbpath: str = dbpath
        self.majors: Dict[str, Major] = dict()
        self.insert_major()
        self.insert_student()
        self.insert_instructor()
        self.insert_grade()
        self.stu_summary()
        self.ins_summary()
        self.major_summary()
        self.student_grades_table_db()

    def insert_student(self) -> None:
        """ Function to add student records """
        try:
            for cwid, name, major in file_reader(os.path.join(
                    self.path, "students.txt"), fields=3, sep='\t', header=True):
                if cwid in self.students:

                    print("Student with CWID is already in the file")
                required: List[str] = self.majors[major].req()
                electives: List[str] = self.majors[major].elec()
                self.students[cwid] = Student(
                    cwid, name, major,required,electives)
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
                    os.path.join(self.path, "grades.txt"), fields=4, sep='\t', header=True):
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

    def insert_major(self) -> None:
        """ Function to add major records """
        try:
            for major, type, course in file_reader(os.path.join(self.path,
                                                                "majors.txt"),
                                                   3, sep='\t', header=True):
                if major not in self.majors:
                    self.majors[major] = Major(major)
                self.majors[major].major_add(type, course)
        except FileNotFoundError:
            print(f"Cannot open file at {self.path}")

    def stu_summary(self):
        """ Function to print student records """

        pt: PrettyTable = PrettyTable(
            field_names=[
                'CWID',
                'Name',
                'Major',
                'Completed Courses',
                'Remaining Required',
                'Remaining Elective',
                'GPA'])    
        
        for s in self.students.values():
            pt.add_row(s.display())
        
        print(pt)
        return pt
         

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
        return pt
       

    def major_summary(self) -> PrettyTable:
        """ Function to print major records """
        pt: PrettyTable = PrettyTable()
        pt.field_names = (["Major", "Required Courses", "Elective Courses"])
        for s in self.majors.values():
            pt.add_row(s.display())

        print(pt)
        return pt
        
    def student_grades_table_db(self):

        pt: PrettyTable = PrettyTable()
        db: Connection = sqlite3.connect(self.dbpath)
        pt.field_names= (["Name","CWID","Course","Grade","Instructor"])
        for row in db.execute("select a.name,a.cwid,course,b.grade,c.name from students a join grades b on a.CWID = b.StudentCWID join instructors c on b.InstructorCWID = c.CWID order by a.name"):
            pt.add_row(row)
        print(pt)
        return pt
        
def main():
    """ Main Menu """
    
    University("C://Users/Swayam/Documents/Downloads","C://Users/Swayam/Documents/Downloads/810_startup.db")    

if __name__ == '__main__':
    main()  


    
