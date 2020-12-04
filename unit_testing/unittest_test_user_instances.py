#!/usr/bin/env python3
from classes.user import Admin, Student
admin_test1 = Admin("admin_test1", "Admin Test1", "user123", 1)
admin_test2 = Admin("admin_test2", "Admin Test2", "user321", 2)
admin_test3 = Admin("admin_test3", "Admin Test3", "user111", 3)

old_pwd1 = "user123"
new_pwd1 = "user321"
old_pwd2 = "user321"
new_pwd2 = "user123"
old_pwd3 = "user111"
new_pwd3 = "user333"

student_test1 = Student("student_test1", "Student Test1", "user123", 4)
student_test2 = Student("student_test2", "Student Test2", "user321", 4)
student_test3 = Student("student_test3", "Student Test3", "user111", 4)

course_id1 = 0
course_id2 = 1
course_id3 = 20
course_id4 = 100
course_id5 = 45
course_id6 = 17

student_test1.add_course(course_id1)
student_test1.add_course(course_id2)
student_test2.add_course(course_id3)
student_test2.add_course(course_id4)
student_test3.add_course(course_id5)
student_test3.add_course(course_id6)

file_id1 = 2
file_id2 = 5
file_id3 = 18
file_id4 = 111
file_id5 = 66
file_id6 = 43

student_test1.add_file(file_id1)
student_test1.add_file(file_id2)
student_test2.add_file(file_id3)
student_test2.add_file(file_id4)
student_test3.add_file(file_id5)
student_test3.add_file(file_id6)
