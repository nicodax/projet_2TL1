#!/usr/bin/env python3
from classes.file import File

user_id1 = 1
user_id2 = 2
user_id3 = 3

pathname1 = "../../files/unittests_files/pathname1"
pathname2 = "../../files/unittests_files/pathname2"
pathname3 = "../../files/unittests_files/pathname3"

course_id = None
tags = None

script1 = False
script2 = True


file_test1 = File(user_id1, pathname1, course_id, 1, script1, tags)
file_test2 = File(user_id2, pathname2, course_id, 2, script1, tags)
file_test3 = File(user_id3, pathname3, course_id, 3, script2, tags)

tag1 = "tag1"
tag2 = "tag2"
tag3 = "tag3"
tag4 = "tag4"
tag5 = "tag5"
tag6 = "tag6"

file_test1.add_tag(tag1)
file_test1.add_tag(tag2)

file_test2.add_tag(tag3)
file_test2.add_tag(tag4)

file_test3.add_tag(tag5)
file_test3.add_tag(tag6)
