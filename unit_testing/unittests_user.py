#!/usr/bin/env python3
import unittest

from classes.exceptions import UnknownPasswordException, AlreadyInListException, NotInListException
from unit_testing.unittest_test_user_instances import admin_test1, old_pwd1, new_pwd1, admin_test2, old_pwd2, \
    new_pwd2, admin_test3, old_pwd3, new_pwd3, course_id1, student_test1, course_id2, course_id3, student_test2, \
    course_id4, course_id5, student_test3, course_id6, file_id1, file_id2, file_id3, file_id4, file_id5, file_id6


class TestPwdAdmin(unittest.TestCase):
    """Cette classe teste la methode pwd(old_pwd, new_pwd) (et par consequent la methode verify_pwd(pwd))
        de la classe Admin (et donc de la classe Student aussi car elle en herite)"""

    def test_pwd_correct_old_pwd(self):
        """old_pwd correspond a self.__pwd"""
        admin_test1.pwd(old_pwd1, new_pwd1)
        self.assertEqual(True, admin_test1.verify_pwd(new_pwd1))

        admin_test2.pwd(old_pwd2, new_pwd2)
        self.assertEqual(True, admin_test2.verify_pwd(new_pwd2))

        admin_test3.pwd(old_pwd3, new_pwd3)
        self.assertEqual(True, admin_test3.verify_pwd(new_pwd3))

        # retablissement des valeurs par defaut :
        admin_test1.pwd(new_pwd1, old_pwd1)
        admin_test2.pwd(new_pwd2, old_pwd2)
        admin_test3.pwd(new_pwd3, old_pwd3)

    def test_pwd_incorrect_old_pwd(self):
        """old_pwd ne correspond pas a self.__pwd"""
        self.assertRaises(UnknownPasswordException, admin_test1.pwd, new_pwd1, old_pwd1)
        self.assertRaises(UnknownPasswordException, admin_test2.pwd, new_pwd2, old_pwd2)
        self.assertRaises(UnknownPasswordException, admin_test3.pwd, new_pwd3, old_pwd3)


class TestCoursesStudent(unittest.TestCase):
    """Cette classe teste les methodes associees a des instances de classes Course de la classe Student
        * add_course(course_id)
        * remove_course(course_id)
        * is_in_courses(course_id)"""

    def test_add_course_not_yet_in_list(self):
        """add_course(course_id) avec course_id ne se trouvant pas dans __courses"""
        # Les ajouts student_test.add_course(course_id) sont effectues dans unittest_test_user_instances et testes ici
        self.assertEqual(True, (course_id1 in student_test1.courses))
        self.assertEqual(True, (course_id2 in student_test1.courses))

        self.assertEqual(True, (course_id3 in student_test2.courses))
        self.assertEqual(True, (course_id4 in student_test2.courses))

        self.assertEqual(True, (course_id5 in student_test3.courses))
        self.assertEqual(True, (course_id6 in student_test3.courses))

    def test_add_course_already_in_list(self):
        """add_course(course_id) avec course_id se trouvant deja dans __courses"""
        self.assertRaises(AlreadyInListException, student_test1.add_course, course_id1)
        self.assertRaises(AlreadyInListException, student_test1.add_course, course_id2)

        self.assertRaises(AlreadyInListException, student_test2.add_course, course_id3)
        self.assertRaises(AlreadyInListException, student_test2.add_course, course_id4)

        self.assertRaises(AlreadyInListException, student_test3.add_course, course_id5)
        self.assertRaises(AlreadyInListException, student_test3.add_course, course_id6)

    def test_is_in_courses_id_with_known_id(self):
        """is_in_course(course_id) avec course_id se trouvant deja dans __courses"""
        self.assertEqual(True, student_test1.is_in_courses(course_id1))
        self.assertEqual(True, student_test1.is_in_courses(course_id2))

        self.assertEqual(True, student_test2.is_in_courses(course_id3))
        self.assertEqual(True, student_test2.is_in_courses(course_id4))

        self.assertEqual(True, student_test3.is_in_courses(course_id5))
        self.assertEqual(True, student_test3.is_in_courses(course_id6))

    def test_is_in_courses_id_with_unknown_id(self):
        """is_in_course(course_id) avec course_id ne se trouvant pas dans __courses"""
        self.assertEqual(False, student_test1.is_in_courses(course_id3))
        self.assertEqual(False, student_test1.is_in_courses(course_id4))
        self.assertEqual(False, student_test1.is_in_courses(course_id5))
        self.assertEqual(False, student_test1.is_in_courses(course_id6))

        self.assertEqual(False, student_test2.is_in_courses(course_id1))
        self.assertEqual(False, student_test2.is_in_courses(course_id2))
        self.assertEqual(False, student_test2.is_in_courses(course_id5))
        self.assertEqual(False, student_test2.is_in_courses(course_id6))

        self.assertEqual(False, student_test3.is_in_courses(course_id1))
        self.assertEqual(False, student_test3.is_in_courses(course_id2))
        self.assertEqual(False, student_test3.is_in_courses(course_id3))
        self.assertEqual(False, student_test3.is_in_courses(course_id4))

    def test_remove_course_with_known_id(self):
        """remove_course(course_id) avec course_id se trouvant deja dans __courses"""
        student_test1.remove_course(course_id1)
        student_test1.remove_course(course_id2)
        self.assertEqual(False, (course_id1 in student_test1.courses))
        self.assertEqual(False, (course_id2 in student_test1.courses))

        student_test2.remove_course(course_id3)
        student_test2.remove_course(course_id4)
        self.assertEqual(False, (course_id3 in student_test2.courses))
        self.assertEqual(False, (course_id4 in student_test2.courses))

        student_test3.remove_course(course_id5)
        student_test3.remove_course(course_id6)
        self.assertEqual(False, (course_id5 in student_test3.courses))
        self.assertEqual(False, (course_id6 in student_test3.courses))

        # retablissement des valeurs par defaut :
        student_test1.add_course(course_id1)
        student_test1.add_course(course_id2)
        student_test2.add_course(course_id3)
        student_test2.add_course(course_id4)
        student_test3.add_course(course_id5)
        student_test3.add_course(course_id6)

    def test_remove_course_with_unknown_id(self):
        """remove_course(course_id) avec course_id ne se trouvant pas dans __courses"""
        self.assertRaises(NotInListException, student_test1.remove_course, course_id3)
        self.assertRaises(NotInListException, student_test1.remove_course, course_id4)
        self.assertRaises(NotInListException, student_test1.remove_course, course_id5)
        self.assertRaises(NotInListException, student_test1.remove_course, course_id6)

        self.assertRaises(NotInListException, student_test2.remove_course, course_id1)
        self.assertRaises(NotInListException, student_test2.remove_course, course_id2)
        self.assertRaises(NotInListException, student_test2.remove_course, course_id5)
        self.assertRaises(NotInListException, student_test2.remove_course, course_id6)

        self.assertRaises(NotInListException, student_test3.remove_course, course_id1)
        self.assertRaises(NotInListException, student_test3.remove_course, course_id2)
        self.assertRaises(NotInListException, student_test3.remove_course, course_id3)
        self.assertRaises(NotInListException, student_test3.remove_course, course_id4)


class TestFilesStudent(unittest.TestCase):
    """Cette classe teste les methodes associees a des instances de classes File de la classe Student
        * add_file(file_id)
        * remove_file(file_id)
        * is_in_files(file_id)"""

    def test_add_file_not_yet_in_list(self):
        """add_file(file_id) avec file_id ne se trouvant pas dans __files"""
        # Les ajouts student_test.add_file(file_id) sont effectues dans unittest_test_user_instances et testes ici
        self.assertEqual(True, (file_id1 in student_test1.files))
        self.assertEqual(True, (file_id2 in student_test1.files))

        self.assertEqual(True, (file_id3 in student_test2.files))
        self.assertEqual(True, (file_id4 in student_test2.files))

        self.assertEqual(True, (file_id5 in student_test3.files))
        self.assertEqual(True, (file_id6 in student_test3.files))

    def test_add_file_already_in_list(self):
        """add_file(file_id) avec file_id se trouvant deja dans __files"""
        self.assertRaises(AlreadyInListException, student_test1.add_file, file_id1)
        self.assertRaises(AlreadyInListException, student_test1.add_file, file_id2)

        self.assertRaises(AlreadyInListException, student_test2.add_file, file_id3)
        self.assertRaises(AlreadyInListException, student_test2.add_file, file_id4)

        self.assertRaises(AlreadyInListException, student_test3.add_file, file_id5)
        self.assertRaises(AlreadyInListException, student_test3.add_file, file_id6)

    def test_is_in_file_id_with_known_id(self):
        """is_in_files(file_id) avec file_id se trouvant deja dans __files"""
        self.assertEqual(True, student_test1.is_in_files(file_id1))
        self.assertEqual(True, student_test1.is_in_files(file_id2))

        self.assertEqual(True, student_test2.is_in_files(file_id3))
        self.assertEqual(True, student_test2.is_in_files(file_id4))

        self.assertEqual(True, student_test3.is_in_files(file_id5))
        self.assertEqual(True, student_test3.is_in_files(file_id6))

    def test_is_in_files_id_with_unknown_id(self):
        """is_in_files(file_id) avec file_id ne se trouvant pas dans __files"""
        self.assertEqual(False, student_test1.is_in_files(file_id3))
        self.assertEqual(False, student_test1.is_in_files(file_id4))
        self.assertEqual(False, student_test1.is_in_files(file_id5))
        self.assertEqual(False, student_test1.is_in_files(file_id6))

        self.assertEqual(False, student_test2.is_in_files(file_id1))
        self.assertEqual(False, student_test2.is_in_files(file_id2))
        self.assertEqual(False, student_test2.is_in_files(file_id5))
        self.assertEqual(False, student_test2.is_in_files(file_id6))

        self.assertEqual(False, student_test3.is_in_files(file_id1))
        self.assertEqual(False, student_test3.is_in_files(file_id2))
        self.assertEqual(False, student_test3.is_in_files(file_id3))
        self.assertEqual(False, student_test3.is_in_files(file_id4))

    def test_remove_file_with_known_id(self):
        """remove_file(file_id) avec file_id se trouvant deja dans __files"""
        student_test1.remove_file(file_id1)
        student_test1.remove_file(file_id2)
        self.assertEqual(False, (file_id1 in student_test1.files))
        self.assertEqual(False, (file_id2 in student_test1.files))

        student_test2.remove_file(file_id3)
        student_test2.remove_file(file_id4)
        self.assertEqual(False, (file_id3 in student_test2.files))
        self.assertEqual(False, (file_id4 in student_test2.files))

        student_test3.remove_file(file_id5)
        student_test3.remove_file(file_id6)
        self.assertEqual(False, (file_id5 in student_test3.files))
        self.assertEqual(False, (file_id6 in student_test3.files))

        # retablissement des valeurs par defaut :
        student_test1.add_file(file_id1)
        student_test1.add_file(file_id2)
        student_test2.add_file(file_id3)
        student_test2.add_file(file_id4)
        student_test3.add_file(file_id5)
        student_test3.add_file(file_id6)

    def test_remove_file_with_unknown_id(self):
        """remove_file(file_id) avec file_id ne se trouvant pas dans __files"""
        self.assertRaises(NotInListException, student_test1.remove_file, file_id3)
        self.assertRaises(NotInListException, student_test1.remove_file, file_id4)
        self.assertRaises(NotInListException, student_test1.remove_file, file_id5)
        self.assertRaises(NotInListException, student_test1.remove_file, file_id6)

        self.assertRaises(NotInListException, student_test2.remove_file, file_id1)
        self.assertRaises(NotInListException, student_test2.remove_file, file_id2)
        self.assertRaises(NotInListException, student_test2.remove_file, file_id5)
        self.assertRaises(NotInListException, student_test2.remove_file, file_id6)

        self.assertRaises(NotInListException, student_test3.remove_file, file_id1)
        self.assertRaises(NotInListException, student_test3.remove_file, file_id2)
        self.assertRaises(NotInListException, student_test3.remove_file, file_id3)
        self.assertRaises(NotInListException, student_test3.remove_file, file_id4)


if __name__ == "__main__":
    pass
