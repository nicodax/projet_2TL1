#!/usr/bin/env python3
import unittest
import cli.cli_misc
import cli.cli_student
import cli.reset
import os

from classes.exceptions import AlreadyInListException, NotInListException


class TestNewStudent(unittest.TestCase):
    """Cette classe teste la methode cli.cli_student.new_file"""
    def test_new_file_existing_pathname(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)

        cli.cli_student.new_file("files/test.txt", False, None, None, student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        all_students = cli.cli_misc.pickle_get(students_arg=True)[0]
        self.assertEqual("files/test.txt", test_file_instance.pathname)
        self.assertEqual(False, test_file_instance.script)
        self.assertEqual(None, test_file_instance.course_id)
        self.assertEqual([], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test3.txt", True, None, None, student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test3.txt", file=True)
        all_students = cli.cli_misc.pickle_get(students_arg=True)[0]
        self.assertEqual("files/test3.txt", test_file_instance.pathname)
        self.assertEqual(True, test_file_instance.script)
        self.assertEqual(None, test_file_instance.course_id)
        self.assertEqual([], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test4.txt", False, 1, None, student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test4.txt", file=True)
        persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
        all_students = persistent_data[0]
        all_courses = persistent_data[3]
        self.assertEqual("files/test4.txt", test_file_instance.pathname)
        self.assertEqual(False, test_file_instance.script)
        self.assertEqual(1, test_file_instance.course_id)
        self.assertEqual([], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))
        self.assertEqual(True, all_courses["objects_dict"][1].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test5.txt", False, None, ["test", "test2", "test3"], student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test5.txt", file=True)
        all_students = cli.cli_misc.pickle_get(students_arg=True)[0]
        self.assertEqual("files/test5.txt", test_file_instance.pathname)
        self.assertEqual(False, test_file_instance.script)
        self.assertEqual(None, test_file_instance.course_id)
        self.assertEqual(["test", "test2", "test3"], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test6.txt", True, 2, None, student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test6.txt", file=True)
        persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
        all_students = persistent_data[0]
        all_courses = persistent_data[3]
        self.assertEqual("files/test6.txt", test_file_instance.pathname)
        self.assertEqual(True, test_file_instance.script)
        self.assertEqual(2, test_file_instance.course_id)
        self.assertEqual([], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))
        self.assertEqual(True, all_courses["objects_dict"][2].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test7.txt", False, 3, ["test15", "test2", "test8"], student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test7.txt", file=True)
        persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
        all_students = persistent_data[0]
        all_courses = persistent_data[3]
        self.assertEqual("files/test7.txt", test_file_instance.pathname)
        self.assertEqual(False, test_file_instance.script)
        self.assertEqual(3, test_file_instance.course_id)
        self.assertEqual(["test15", "test2", "test8"], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))
        self.assertEqual(True, all_courses["objects_dict"][3].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test8.txt", True, None, ["test", "test2", "test3"], student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test8.txt", file=True)
        all_students = cli.cli_misc.pickle_get(students_arg=True)[0]
        self.assertEqual("files/test8.txt", test_file_instance.pathname)
        self.assertEqual(True, test_file_instance.script)
        self.assertEqual(None, test_file_instance.course_id)
        self.assertEqual(["test", "test2", "test3"], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test9.txt", True, 6, ["test", "test26", "test3"], student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test9.txt", file=True)
        persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
        all_students = persistent_data[0]
        all_courses = persistent_data[3]
        self.assertEqual("files/test9.txt", test_file_instance.pathname)
        self.assertEqual(True, test_file_instance.script)
        self.assertEqual(6, test_file_instance.course_id)
        self.assertEqual(["test", "test26", "test3"], test_file_instance.tags)
        self.assertEqual(student_instance.user_id, test_file_instance.user_id)
        self.assertEqual(True, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))
        self.assertEqual(True, all_courses["objects_dict"][6].is_in_files(test_file_instance.file_id))

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")
        if os.path.isfile("files/test3.txt"):
            os.remove("files/test3.txt")
        if os.path.isfile("files/test4.txt"):
            os.remove("files/test4.txt")
        if os.path.isfile("files/test5.txt"):
            os.remove("files/test5.txt")
        if os.path.isfile("files/test6.txt"):
            os.remove("files/test6.txt")
        if os.path.isfile("files/test7.txt"):
            os.remove("files/test7.txt")
        if os.path.isfile("files/test8.txt"):
            os.remove("files/test8.txt")
        if os.path.isfile("files/test9.txt"):
            os.remove("files/test9.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestDeleteStudent(unittest.TestCase):
    """Cette classe teste la methode cli.cli_student.delete_file"""
    def test_new_file_existing_pathname(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)

        cli.cli_student.new_file("files/test.txt", False, None, None, student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        cli.cli_student.delete_file(test_file_instance, student_instance)
        persistent_data = cli.cli_misc.pickle_get(students_arg=True, files_arg=True)
        all_students = persistent_data[0]
        all_files = persistent_data[2]
        self.assertEqual(False, (test_file_instance.file_id in all_files["objects_dict"]))
        self.assertEqual(False, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test3.txt", False, 1, None, student_instance)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test3.txt", file=True)
        cli.cli_student.delete_file(test_file_instance, student_instance)
        persistent_data = cli.cli_misc.pickle_get(students_arg=True, files_arg=True, courses_arg=True)
        all_students = persistent_data[0]
        all_files = persistent_data[2]
        all_courses = persistent_data[3]
        self.assertEqual(False, (test_file_instance.file_id in all_files["objects_dict"]))
        self.assertEqual(False, all_students["objects_dict"][3].is_in_files(test_file_instance.file_id))
        self.assertEqual(False, all_courses["objects_dict"][1].is_in_files(test_file_instance.file_id))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestFileChangeScriptAttribute(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_student.file_change_script_attribute"""
    def test_change_script_attribute_of_file_from_script_equals_false(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.new_file("files/test.txt", False, None, None, student_instance)

        cli.cli_student.file_change_script_attribute("files/test.txt", False)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(False, test_file_instance.script)

        cli.cli_student.file_change_script_attribute("files/test.txt", True)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(True, test_file_instance.script)

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_file_change_script_attribute_of_file_from_script_equals_true(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.new_file("files/test.txt", True, None, None, student_instance)

        cli.cli_student.file_change_script_attribute("files/test.txt", True)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(True, test_file_instance.script)

        cli.cli_student.file_change_script_attribute("files/test.txt", False)
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(False, test_file_instance.script)

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestFileAddCourse(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_student.file_add_course"""
    def test_file_add_course_of_file_without_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.new_file("files/test.txt", True, None, None, student_instance)

        cli.cli_student.file_add_course("files/test.txt", "T2011")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        test_course_instance = cli.cli_misc.pickle_get_instance("T2011", course=True)

        self.assertEqual(test_course_instance.course_id, test_file_instance.course_id)

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_file_add_course_of_file_with_different_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.new_file("files/test.txt", True, 0, None, student_instance)

        cli.cli_student.file_add_course("files/test.txt", "T2012")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        test_course_instance = cli.cli_misc.pickle_get_instance("T2012", course=True)

        self.assertEqual(test_course_instance.course_id, test_file_instance.course_id)

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_file_add_course_of_file_with_same_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.new_file("files/test.txt", True, 0, None, student_instance)

        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_course, "files/test.txt", "T2011")

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestFileAddTag(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_student.file_add_tag"""
    def test_file_add_unknown_tag(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)

        cli.cli_student.new_file("files/test.txt", True, None, None, student_instance)
        cli.cli_student.file_add_tag("files/test.txt", ["tag1", "tag2", "tag3"])
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(True, test_file_instance.is_in_tags("tag1"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag2"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag3"))

        cli.cli_student.new_file("files/test3.txt", True, None, ["tag1", "tag2", "tag3"], student_instance)
        cli.cli_student.file_add_tag("files/test3.txt", ["tag4", "tag5", "tag6"])
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test3.txt", file=True)
        self.assertEqual(True, test_file_instance.is_in_tags("tag1"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag2"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag3"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag4"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag5"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag6"))

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")
        if os.path.isfile("files/test3.txt"):
            os.remove("files/test3.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_file_add_known_tag(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)

        cli.cli_student.new_file("files/test.txt", True, None, ["tag1", "tag2", "tag3"], student_instance)
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt", ["tag1"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt", ["tag2"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt", ["tag3"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt", ["tag1", "tag2"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt", ["tag1", "tag3"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt", ["tag2", "tag3"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt",
                          ["tag1", "tag2", "tag3"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt", ["tag1", "tag4"])
        self.assertRaises(AlreadyInListException, cli.cli_student.file_add_tag, "files/test.txt",
                          ["tag1", "tag6", "tag10"])

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestFileRemoveCourse(unittest.TestCase):
    """Cette classe teste la focntion cli.cli_student.file_remove_course"""
    def test_remove_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)

        cli.cli_student.new_file("files/test.txt", True, 0, None, student_instance)
        cli.cli_student.file_remove_course("files/test.txt")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        test_course_instance = cli.cli_misc.pickle_get_instance("T2011", course=True)
        self.assertEqual(None, test_file_instance.course_id)
        self.assertEqual(False, test_course_instance.is_in_files(test_file_instance.file_id))

        cli.cli_student.new_file("files/test3.txt", True, None, None, student_instance)
        cli.cli_student.file_remove_course("files/test3.txt")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test3.txt", file=True)
        self.assertEqual(None, test_file_instance.course_id)

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")
        if os.path.isfile("files/test3.txt"):
            os.remove("files/test3.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestFileRemoveTag(unittest.TestCase):
    """Cette classe teste la focntion cli.cli_student.file_remove_tag"""
    def test_remove_tag_with_known_tag(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.new_file("files/test.txt", True, None, ["tag1", "tag2", "tag3"], student_instance)

        cli.cli_student.file_remove_tag("files/test.txt", "tag1")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(False, test_file_instance.is_in_tags("tag1"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag2"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag3"))

        cli.cli_student.file_remove_tag("files/test.txt", "tag2")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(False, test_file_instance.is_in_tags("tag1"))
        self.assertEqual(False, test_file_instance.is_in_tags("tag2"))
        self.assertEqual(True, test_file_instance.is_in_tags("tag3"))

        cli.cli_student.file_remove_tag("files/test.txt", "tag3")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual(False, test_file_instance.is_in_tags("tag1"))
        self.assertEqual(False, test_file_instance.is_in_tags("tag2"))
        self.assertEqual(False, test_file_instance.is_in_tags("tag3"))

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_remove_tag_with_unknown_tag(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.new_file("files/test.txt", True, None, ["tag1", "tag2", "tag3"], student_instance)

        self.assertRaises(NotInListException, cli.cli_student.file_remove_tag, "files/test.txt", "tag4")
        self.assertRaises(NotInListException, cli.cli_student.file_remove_tag, "files/test.txt", "tag5")
        self.assertRaises(NotInListException, cli.cli_student.file_remove_tag, "files/test.txt", "tag6")

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestMoveFile(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_student.move_file"""
    def test_move_file(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)

        cli.cli_student.new_file("files/test.txt", True, None, None, student_instance)
        cli.cli_student.move_file("files/test.txt", "files/test/test.txt")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test/test.txt", file=True)
        self.assertEqual("files/test/test.txt", test_file_instance.pathname)

        cli.cli_student.move_file(test_file_instance.pathname, "files/test.txt")
        test_file_instance = cli.cli_misc.pickle_get_instance("files/test.txt", file=True)
        self.assertEqual("files/test.txt", test_file_instance.pathname)

        if os.path.isfile("files/test.txt"):
            os.remove("files/test.txt")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestSubscribeUserToCourse(unittest.TestCase):
    """Cette classe test la fonction cli.cli_student.subscribe_user_to_course"""
    def test_subscribe_student_to_not_subbed_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.subscribe_user_to_course("T2011", student_instance)
        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        course_instance = cli.cli_misc.pickle_get_instance("T2011", course=True)
        self.assertEqual(True, (course_instance.course_id in student_instance.courses))
        self.assertEqual(True, (student_instance.user_id in course_instance.students))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_subscribe_student_to_already_subbed_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.subscribe_user_to_course("T2011", student_instance)
        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        self.assertRaises(AlreadyInListException, cli.cli_student.subscribe_user_to_course, "T2011", student_instance)

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestUnsubscribeUserToCourse(unittest.TestCase):
    """Cette classe test la fonction cli.cli_student.unsubscribe_user_from_course"""
    def test_unsubscribe_student_from_already_subbed_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.subscribe_user_to_course("T2011", student_instance)
        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        cli.cli_student.unsubscribe_user_from_course("T2011", student_instance)
        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        course_instance = cli.cli_misc.pickle_get_instance("T2011", course=True)
        self.assertEqual(False, (course_instance.course_id in student_instance.courses))
        self.assertEqual(False, (student_instance.user_id in course_instance.students))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_unsubscribe_student_from_not_subbed_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        student_instance = cli.cli_misc.pickle_get_instance("dax", student=True)
        self.assertRaises(NotInListException, cli.cli_student.unsubscribe_user_from_course, "T2011", student_instance)

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


if __name__ == "__main__":
    pass
