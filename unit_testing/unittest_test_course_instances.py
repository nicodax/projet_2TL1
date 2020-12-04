#!/usr/bin/env python3
from classes.course import Course
course_test1 = Course("T201", [], 1)
course_test2 = Course("T203", [], 2)
course_test3 = Course("T207", [], 3)

teacher1 = "VVDS"
teacher2 = "XD"
teacher3 = "JN"
teacher4 = "LS"
teacher5 = "MNV"
teacher6 = "YB"
teacher7 = "AD"

course_test1.add_teacher(teacher1)
course_test1.add_teacher(teacher2)
course_test1.add_teacher(teacher3)

course_test2.add_teacher(teacher4)
course_test2.add_teacher(teacher5)

course_test3.add_teacher(teacher6)
course_test3.add_teacher(teacher7)

file_id1 = 2
file_id2 = 5
file_id3 = 18
file_id4 = 111
file_id5 = 66
file_id6 = 43

course_test1.add_file(file_id1)
course_test1.add_file(file_id2)
course_test2.add_file(file_id3)
course_test2.add_file(file_id4)
course_test3.add_file(file_id5)
course_test3.add_file(file_id6)

user_id1 = 1
user_id2 = 2
user_id3 = 3
user_id4 = 4
user_id5 = 5
user_id6 = 6

course_test1.add_student(user_id1)
course_test1.add_student(user_id2)
course_test2.add_student(user_id3)
course_test2.add_student(user_id4)
course_test3.add_student(user_id5)
course_test3.add_student(user_id6)
