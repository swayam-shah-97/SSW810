"""

@author - Swayam Shah
@CWID - 10471353

"""

from flask import Flask,render_template
import sqlite3
from typing import Dict

app: Flask = Flask(__name__)
@app.route('/students')
def student_grade_table() -> str:
    DB_File: str = "C://Users/Swayam/Documents/Downloads/810_startup.db"
    query: str = """select a.name,a.CWID,course,b.grade,c.name
                from students a join grades b on a.CWID = b.StudentCWID
                join instructors c on b.InstructorCWID = c.CWID
                order by a.name"""
    db: Connection = sqlite3.connect(DB_File) 
    data: Dict[str,str] = [{'student':student,'cwid':cwid,'course':course,'grade':grade,'instructor':instructor}
                for student,cwid,course,grade,instructor in db.execute(query)]

    db.close()

    return render_template('student_grade_table.html',
                            title = 'Stevens Repository',
                            table_title = 'Student,Course,Grade and Instructor',
                            students= data)

app.run(debug=True)
