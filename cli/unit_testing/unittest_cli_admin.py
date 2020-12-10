#!/usr/bin/env python3
import unittest
import mock
import cli.cli_misc
import cli.cli_admin
import cli.reset
import os

from classes.exceptions import AlreadyInListException
from cli.exceptions import ObjectAlreadyExistantException, PasswordNotEqualException, UnknownObjectException


class TestNewStudent(unittest.TestCase):
    """Cette classe teste la methode cli.cli_admin.new_student"""
    @mock.patch('getpass.getpass', side_effect=["test", "test", "test2", "test2", "test3", "test3"])
    def test_new_student_not_existing_username(self, side_effect):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")
        cli.cli_admin.new_student("test", "test_fullname")
        test_student_instance = cli.cli_misc.pickle_get_instance("test", student=True)
        self.assertEqual("test_fullname", test_student_instance.fullname)
        self.assertEqual(True, test_student_instance.verify_pwd("test"))

        cli.cli_admin.new_student("test2", "test2_fullname")
        test_student_instance = cli.cli_misc.pickle_get_instance("test2", student=True)
        self.assertEqual("test2_fullname", test_student_instance.fullname)
        self.assertEqual(True, test_student_instance.verify_pwd("test2"))

        cli.cli_admin.new_student("test3", "test3_fullname")
        test_student_instance = cli.cli_misc.pickle_get_instance("test3", student=True)
        self.assertEqual("test3_fullname", test_student_instance.fullname)
        self.assertEqual(True, test_student_instance.verify_pwd("test3"))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    @mock.patch('getpass.getpass', side_effect=["test", "test", "test2", "test2"])
    def test_new_student_existing_username(self, side_effect):
        os.chdir("../..")
        self.assertRaises(ObjectAlreadyExistantException, cli.cli_admin.new_student, "dax", "test_fullname")
        self.assertRaises(ObjectAlreadyExistantException, cli.cli_admin.new_student, "greg", "test2_fullname")
        os.chdir("cli/unit_testing")

    @mock.patch('getpass.getpass', side_effect=["test", "test_mismatch", "test2", "test2_mismatch"])
    def test_new_student_not_existing_username_and_password_mismatch(self, side_effect):
        os.chdir("../..")
        self.assertRaises(PasswordNotEqualException, cli.cli_admin.new_student, "test", "test_fullname")
        self.assertRaises(PasswordNotEqualException, cli.cli_admin.new_student, "test2", "test2_fullname")
        os.chdir("cli/unit_testing")


class TestNewAdmin(unittest.TestCase):
    """Cette classe teste la methode cli.cli_admin.new_admin"""
    @mock.patch('getpass.getpass', side_effect=["test", "test", "test2", "test2", "test3", "test3"])
    def test_new_admin_not_existing_username(self, side_effect):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_admin("test", "test_fullname")
        test_admin_instance = cli.cli_misc.pickle_get_instance("test", admin=True)
        self.assertEqual("test_fullname", test_admin_instance.fullname)
        self.assertEqual(True, test_admin_instance.verify_pwd("test"))

        cli.cli_admin.new_admin("test2", "test2_fullname")
        test_admin_instance = cli.cli_misc.pickle_get_instance("test2", admin=True)
        self.assertEqual("test2_fullname", test_admin_instance.fullname)
        self.assertEqual(True, test_admin_instance.verify_pwd("test2"))

        cli.cli_admin.new_admin("test3", "test3_fullname")
        test_admin_instance = cli.cli_misc.pickle_get_instance("test3", admin=True)
        self.assertEqual("test3_fullname", test_admin_instance.fullname)
        self.assertEqual(True, test_admin_instance.verify_pwd("test3"))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    @mock.patch('getpass.getpass', side_effect=["test", "test", "test2", "test2"])
    def test_new_admin_existing_username(self, side_effect):
        os.chdir("../..")
        self.assertRaises(ObjectAlreadyExistantException, cli.cli_admin.new_admin, "daxxra", "test_fullname")
        self.assertRaises(ObjectAlreadyExistantException, cli.cli_admin.new_admin, "TheGregouze", "test2_fullname")
        os.chdir("cli/unit_testing")

    @mock.patch('getpass.getpass', side_effect=["test", "test_mismatch", "test2", "test2_mismatch"])
    def test_new_admin_not_existing_username_and_password_mismatch(self, side_effect):
        os.chdir("../..")
        self.assertRaises(PasswordNotEqualException, cli.cli_admin.new_admin, "test", "test_fullname")
        self.assertRaises(PasswordNotEqualException, cli.cli_admin.new_admin, "test2", "test2_fullname")
        os.chdir("cli/unit_testing")


class TestNewCourse(unittest.TestCase):
    """Cette classe teste la methode cli.cli_admin.new_course"""
    def test_new_course_not_existing_name(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual(True, ("test" in test_course_instance.teachers))
        self.assertEqual(True, ("test2" in test_course_instance.teachers))
        self.assertEqual(True, ("test3" in test_course_instance.teachers))
        self.assertEqual("test", test_course_instance.description)

        cli.cli_admin.new_course("test2", ["test21", "test22", "test23"], "test2")
        test_course_instance = cli.cli_misc.pickle_get_instance("test2", course=True)
        self.assertEqual(True, ("test21" in test_course_instance.teachers))
        self.assertEqual(True, ("test22" in test_course_instance.teachers))
        self.assertEqual(True, ("test23" in test_course_instance.teachers))
        self.assertEqual("test2", test_course_instance.description)

        cli.cli_admin.new_course("test3", ["test31", "test32", "test33"], "test3")
        test_course_instance = cli.cli_misc.pickle_get_instance("test3", course=True)
        self.assertEqual(True, ("test31" in test_course_instance.teachers))
        self.assertEqual(True, ("test32" in test_course_instance.teachers))
        self.assertEqual(True, ("test33" in test_course_instance.teachers))
        self.assertEqual("test3", test_course_instance.description)

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_new_course_existing_name(self):
        os.chdir("../..")
        self.assertRaises(ObjectAlreadyExistantException, cli.cli_admin.new_course, "T2011", ["test", "test2", "test3"],
                          "test")
        self.assertRaises(ObjectAlreadyExistantException, cli.cli_admin.new_course, "T2072", ["test", "test2", "test3"],
                          "test")
        os.chdir("cli/unit_testing")


class TestDeleteStudent(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_admin.delete_student"""
    @mock.patch('getpass.getpass', side_effect=["test", "test"])
    def test_delete_existant_student(self, side_effect):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_student("test", "test_fullname")
        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        test_student_instance = cli.cli_misc.pickle_get_instance("test", student=True)
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        test_student_instance.add_course(test_course_instance.course_id)
        test_course_instance.add_student(test_student_instance.user_id)

        persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
        all_students = persistent_data[0]
        all_courses = persistent_data[3]
        all_students["objects_dict"][test_student_instance.user_id] = test_student_instance
        all_courses["objects_dict"][test_course_instance.course_id] = test_course_instance
        cli.cli_misc.pickle_save(all_students=all_students, all_courses=all_courses)
        test_student_instance = cli.cli_misc.pickle_get_instance("test", student=True)
        self.assertEqual(True, test_student_instance.is_in_courses(test_course_instance.course_id))
        self.assertEqual(True, test_course_instance.is_in_students(test_student_instance.user_id))

        cli.cli_admin.delete_student("test")
        all_students = cli.cli_misc.pickle_get(students_arg=True)[0]
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual(False, ("test" in all_students["name_id_dict"]))
        self.assertEqual(False, test_course_instance.is_in_students(test_student_instance.user_id))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_delete_unknown_student(self):
        os.chdir("../..")
        self.assertRaises(UnknownObjectException, cli.cli_admin.delete_student, "test")
        os.chdir("cli/unit_testing")


class TestDeleteAdmin(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_admin.delete_admin"""
    @mock.patch('getpass.getpass', side_effect=["test", "test"])
    def test_delete_existant_admin(self, side_effect):
        os.chdir("../..")
        cli.cli_admin.new_admin("test", "test_fullname")
        cli.cli_admin.delete_admin("test")
        all_admins = cli.cli_misc.pickle_get(admins_arg=True)[1]
        self.assertEqual(False, ("test" in all_admins["name_id_dict"]))
        os.chdir("cli/unit_testing")

    def test_delete_unknown_admin(self):
        os.chdir("../..")
        self.assertRaises(UnknownObjectException, cli.cli_admin.delete_admin, "test")
        os.chdir("cli/unit_testing")


class TestDeleteCourse(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_admin.delete_course"""
    @mock.patch('getpass.getpass', side_effect=["test", "test"])
    def test_delete_existant_course(self, side_effect):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        cli.cli_admin.new_student("test", "test_fullname")
        test_student_instance = cli.cli_misc.pickle_get_instance("test", student=True)
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        test_student_instance.add_course(test_course_instance.course_id)
        test_course_instance.add_student(test_student_instance.user_id)

        persistent_data = cli.cli_misc.pickle_get(students_arg=True, courses_arg=True)
        all_students = persistent_data[0]
        all_courses = persistent_data[3]
        all_students["objects_dict"][test_student_instance.user_id] = test_student_instance
        all_courses["objects_dict"][test_course_instance.course_id] = test_course_instance
        cli.cli_misc.pickle_save(all_students=all_students, all_courses=all_courses)
        test_student_instance = cli.cli_misc.pickle_get_instance("test", student=True)
        self.assertEqual(True, test_student_instance.is_in_courses(test_course_instance.course_id))
        self.assertEqual(True, test_course_instance.is_in_students(test_student_instance.user_id))

        cli.cli_admin.delete_course("test")
        all_courses = cli.cli_misc.pickle_get(courses_arg=True)[3]
        test_student_instance = cli.cli_misc.pickle_get_instance("test", student=True)
        self.assertEqual(False, ("test" in all_courses["name_id_dict"]))
        self.assertEqual(False, test_student_instance.is_in_courses(test_course_instance.course_id))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_delete_unknown_course(self):
        os.chdir("../..")
        self.assertRaises(UnknownObjectException, cli.cli_admin.delete_course, "test")
        os.chdir("cli/unit_testing")


class TestCourseAddTeachers(unittest.TestCase):
    """Cette classe teste les fonction cli.cli_admin.course_add_teacher"""
    def test_add_unknown_teacher_to_existing_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        cli.cli_admin.course_add_teacher("test", "test4")
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual(True, ("test4" in test_course_instance.teachers))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_add_known_teacher_to_existing_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        self.assertRaises(AlreadyInListException, cli.cli_admin.course_add_teacher, "test", "test")
        self.assertRaises(AlreadyInListException, cli.cli_admin.course_add_teacher, "test", "test2")
        self.assertRaises(AlreadyInListException, cli.cli_admin.course_add_teacher, "test", "test3")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_add_teacher_to_unknown_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        self.assertRaises(UnknownObjectException, cli.cli_admin.course_add_teacher, "test2", "test")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestCourseRemoveTeacher(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_admin.course_remove_teacher"""
    def test_remove_known_teacher_from_existing_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        cli.cli_admin.course_remove_teacher("test", "test", False)
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual(False, ("test" in test_course_instance.teachers))
        self.assertEqual(True, ("test2" in test_course_instance.teachers))
        self.assertEqual(True, ("test3" in test_course_instance.teachers))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_remove_all_teachers_from_existing_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        cli.cli_admin.course_remove_teacher("test", None, True)
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual(False, ("test" in test_course_instance.teachers))
        self.assertEqual(False, ("test2" in test_course_instance.teachers))
        self.assertEqual(False, ("test3" in test_course_instance.teachers))

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_remove_teacher_from_unknown_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        self.assertRaises(UnknownObjectException, cli.cli_admin.course_remove_teacher, "test2", "test", False)
        self.assertRaises(UnknownObjectException, cli.cli_admin.course_remove_teacher, "test2", None, True)

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestCourseAddDescription(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_admin.course_add_description"""
    def test_add_description_to_existing_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual("test", test_course_instance.description)
        cli.cli_admin.course_add_description("test", "description")
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual("description", test_course_instance.description)

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_add_description_to_unknown_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        self.assertRaises(UnknownObjectException, cli.cli_admin.course_add_description, "test2", "description")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


class TestCourseRemoveDescription(unittest.TestCase):
    """Cette classe teste la fonction cli.cli_admin.course_remove_description"""
    def test_remove_description_from_existing_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual("test", test_course_instance.description)
        cli.cli_admin.course_remove_description("test")
        test_course_instance = cli.cli_misc.pickle_get_instance("test", course=True)
        self.assertEqual("", test_course_instance.description)

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")

    def test_remove_description_from_unknown_course(self):
        os.chdir("..")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("..")

        cli.cli_admin.new_course("test", ["test", "test2", "test3"], "test")
        self.assertRaises(UnknownObjectException, cli.cli_admin.course_remove_description, "test2")

        os.chdir("cli")
        students, admins, files, courses, id_dict = cli.reset.reset()
        cli.reset.pickle_save(students, admins, files, courses, id_dict)
        os.chdir("unit_testing")


if __name__ == "__main__":
    pass
