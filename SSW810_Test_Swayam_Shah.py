"""

@author - Swayam Shah
@CWID - 10471353

"""

import unittest
from HW09_Swayam_Shah import University


class HW09TestCase(unittest.TestCase):
    """ class to test university data repository """
    
    
    def test_students(self):
        """ Function to test student summary """

        self.r: University = University(
            "C://Users/Swayam/Documents/Downloads")

        a: dict = {'10103': ['10103', 'Baldwin, C',
                              ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10115': ['10115', 'Wyatt, X',
                              ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']],
                    '10175': ['10175', 'Erickson, D',
                              ['SSW 564', 'SSW 567', 'SSW 687']],
                    '10183': ['10183', 'Chapman, O', ['SSW 689']],
                    '11399': ['11399', 'Cordova, I', ['SSW 540']],
                    '11461': ['11461', 'Wright, U',
                              ['SYS 611', 'SYS 750', 'SYS 800']],
                    '11658': ['11658', 'Kelly, P', ['SSW 540']],
                    '11714': ['11714', 'Morton, A', ['SYS 611', 'SYS 645']],
                    '11788': ['11788', 'Fuller, E', ['SSW 540']]}

        b: dict = {cwid: student.display()
                  for cwid, student in self.r.students.items()}
        self.assertEqual(a,b)

        c: dict = {"jggjgjgjj":123}
        self.assertNotEqual(c,b)

    def test_instructor(self) -> None:
        """ Function to test instructor summary """

        self.r: University = University(
            "C://Users/Swayam/Documents/Downloads")
        a: dict = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}
        b: dict = {tuple(
            detail) for instructor in self.r.instructors.values(
        ) for detail in instructor.display()}
        self.assertEqual(a, b)

        c: dict = {}      
        self.assertNotEqual(c,b)
    
    def test_keyerrror(self) -> None:
        """ Function to test key error """

        with self.assertRaises(KeyError):
            University(
                "C://Users/Swayam/Documents/Downloads/new")


    def test_no_record(self) -> None:
        """ Function to test no records """

        with self.assertRaises(KeyError):
            University(
                "C://Users/Swayam/Documents/Downloads/new")

    def test_duplicate_values(self) -> None:
        """ Function to test duplicate values """

        with self.assertRaises(KeyError):
            University(
                "C://Users/Swayam/Documents/Downloads/new")

    

    
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)