#!/usr/bin/env python3
import unittest

from classes.exceptions import AlreadyInListException, NotInListException
from classes.test.unittest_test_course_instances import course_test1, course_test2, course_test3, teacher1, \
    teacher2, teacher3, teacher4, teacher5, teacher6, teacher7, file_id1, file_id2, file_id3, file_id4, file_id5, \
    file_id6, user_id1, user_id2, user_id3, user_id4, user_id5, user_id6


class TestTeachersCourse(unittest.TestCase):
    """Cette classe teste les methodes associees a la gestion des proffesseurs pour la classe Course
        * add_teacher(name)
        * remove_teacher(name)
        * is_in_teachers(name)"""

    def test_add_teacher_not_yet_in_list(self):
        """add_teacher(name) avec name ne se trouvant pas dans __teachers"""
        # Les ajouts course_test.add_course(course_id) sont effectues dans unittest_test_course_instances et testes ici
        self.assertEqual(True, (teacher1 in course_test1.teachers))
        self.assertEqual(True, (teacher2 in course_test1.teachers))
        self.assertEqual(True, (teacher3 in course_test1.teachers))

        self.assertEqual(True, (teacher4 in course_test2.teachers))
        self.assertEqual(True, (teacher5 in course_test2.teachers))

        self.assertEqual(True, (teacher6 in course_test3.teachers))
        self.assertEqual(True, (teacher7 in course_test3.teachers))

    def test_add_teacher_already_in_list(self):
        """add_teacher(name) avec name se trouvant deja dans __teachers"""
        self.assertRaises(AlreadyInListException, course_test1.add_teacher, teacher1)
        self.assertRaises(AlreadyInListException, course_test1.add_teacher, teacher2)
        self.assertRaises(AlreadyInListException, course_test1.add_teacher, teacher3)

        self.assertRaises(AlreadyInListException, course_test2.add_teacher, teacher4)
        self.assertRaises(AlreadyInListException, course_test2.add_teacher, teacher5)

        self.assertRaises(AlreadyInListException, course_test3.add_teacher, teacher6)
        self.assertRaises(AlreadyInListException, course_test3.add_teacher, teacher7)

    def test_is_in_teachers_with_known_name(self):
        """is_in_teachers(name) avec name se trouvant deja dans __teachers"""
        self.assertEqual(True, course_test1.is_in_teachers(teacher1))
        self.assertEqual(True, course_test1.is_in_teachers(teacher2))
        self.assertEqual(True, course_test1.is_in_teachers(teacher3))

        self.assertEqual(True, course_test2.is_in_teachers(teacher4))
        self.assertEqual(True, course_test2.is_in_teachers(teacher5))

        self.assertEqual(True, course_test3.is_in_teachers(teacher6))
        self.assertEqual(True, course_test3.is_in_teachers(teacher7))

    def test_is_in_teachers_with_unknown_name(self):
        """is_in_teachers(name) avec name ne se trouvant pas dans __teachers"""
        self.assertEqual(False, course_test1.is_in_teachers(teacher4))
        self.assertEqual(False, course_test1.is_in_teachers(teacher5))
        self.assertEqual(False, course_test1.is_in_teachers(teacher6))
        self.assertEqual(False, course_test1.is_in_teachers(teacher7))

        self.assertEqual(False, course_test2.is_in_teachers(teacher1))
        self.assertEqual(False, course_test2.is_in_teachers(teacher2))
        self.assertEqual(False, course_test2.is_in_teachers(teacher3))
        self.assertEqual(False, course_test2.is_in_teachers(teacher6))
        self.assertEqual(False, course_test2.is_in_teachers(teacher7))

        self.assertEqual(False, course_test3.is_in_teachers(teacher1))
        self.assertEqual(False, course_test3.is_in_teachers(teacher2))
        self.assertEqual(False, course_test3.is_in_teachers(teacher3))
        self.assertEqual(False, course_test3.is_in_teachers(teacher4))
        self.assertEqual(False, course_test3.is_in_teachers(teacher5))

    def test_remove_teacher_with_known_name(self):
        """remove_teacher(name) avec name se trouvant deja dans __teachers"""
        course_test1.remove_teacher(teacher1)
        course_test1.remove_teacher(teacher2)
        course_test1.remove_teacher(teacher3)
        self.assertEqual(False, (teacher1 in course_test1.teachers))
        self.assertEqual(False, (teacher2 in course_test1.teachers))
        self.assertEqual(False, (teacher3 in course_test1.teachers))

        course_test2.remove_teacher(teacher4)
        course_test2.remove_teacher(teacher5)
        self.assertEqual(False, (teacher4 in course_test2.teachers))
        self.assertEqual(False, (teacher5 in course_test2.teachers))

        course_test3.remove_teacher(teacher6)
        course_test3.remove_teacher(teacher7)
        self.assertEqual(False, (teacher6 in course_test3.teachers))
        self.assertEqual(False, (teacher7 in course_test3.teachers))

        # retablissement des valeurs par defaut :
        course_test1.add_teacher(teacher1)
        course_test1.add_teacher(teacher2)
        course_test1.add_teacher(teacher3)
        course_test2.add_teacher(teacher4)
        course_test2.add_teacher(teacher5)
        course_test3.add_teacher(teacher6)
        course_test3.add_teacher(teacher7)

    def test_remove_teacher_with_unknown_name(self):
        """remove_teacher(name) avec name ne se trouvant pas dans __teachers"""
        self.assertRaises(NotInListException, course_test1.remove_teacher, teacher4)
        self.assertRaises(NotInListException, course_test1.remove_teacher, teacher5)
        self.assertRaises(NotInListException, course_test1.remove_teacher, teacher6)
        self.assertRaises(NotInListException, course_test1.remove_teacher, teacher7)

        self.assertRaises(NotInListException, course_test2.remove_teacher, teacher1)
        self.assertRaises(NotInListException, course_test2.remove_teacher, teacher2)
        self.assertRaises(NotInListException, course_test2.remove_teacher, teacher3)
        self.assertRaises(NotInListException, course_test2.remove_teacher, teacher6)
        self.assertRaises(NotInListException, course_test2.remove_teacher, teacher7)

        self.assertRaises(NotInListException, course_test3.remove_teacher, teacher1)
        self.assertRaises(NotInListException, course_test3.remove_teacher, teacher2)
        self.assertRaises(NotInListException, course_test3.remove_teacher, teacher3)
        self.assertRaises(NotInListException, course_test3.remove_teacher, teacher4)
        self.assertRaises(NotInListException, course_test3.remove_teacher, teacher5)


class TestFilesCourse(unittest.TestCase):
    """Cette classe teste les methodes associees a la gestion des fichiers pour la classe Course
        * add_file(file_id)
        * remove_file(file_id)
        * is_in_files(file_id)"""

    def test_add_file_not_yet_in_list(self):
        """add_file(file_id) avec file_id ne se trouvant pas dans __files"""
        # Les ajouts course_test.add_file(file_id) sont effectues dans unittest_test_course_instances et testes ici
        self.assertEqual(True, (file_id1 in course_test1.files))
        self.assertEqual(True, (file_id2 in course_test1.files))

        self.assertEqual(True, (file_id3 in course_test2.files))
        self.assertEqual(True, (file_id4 in course_test2.files))

        self.assertEqual(True, (file_id5 in course_test3.files))
        self.assertEqual(True, (file_id6 in course_test3.files))

    def test_add_file_already_in_list(self):
        """add_file(file_id) avec file_id se trouvant deja dans __files"""
        self.assertRaises(AlreadyInListException, course_test1.add_file, file_id1)
        self.assertRaises(AlreadyInListException, course_test1.add_file, file_id2)

        self.assertRaises(AlreadyInListException, course_test2.add_file, file_id3)
        self.assertRaises(AlreadyInListException, course_test2.add_file, file_id4)

        self.assertRaises(AlreadyInListException, course_test3.add_file, file_id5)
        self.assertRaises(AlreadyInListException, course_test3.add_file, file_id6)

    def test_is_in_files_with_known_id(self):
        """is_in_files(file_id) avec file_id se trouvant deja dans __files"""
        self.assertEqual(True, course_test1.is_in_files(file_id1))
        self.assertEqual(True, course_test1.is_in_files(file_id2))

        self.assertEqual(True, course_test2.is_in_files(file_id3))
        self.assertEqual(True, course_test2.is_in_files(file_id4))

        self.assertEqual(True, course_test3.is_in_files(file_id5))
        self.assertEqual(True, course_test3.is_in_files(file_id6))

    def test_is_in_files_with_unknown_id(self):
        """is_in_files(file_id) avec file_id ne se trouvant pas dans __files"""
        self.assertEqual(False, course_test1.is_in_files(file_id3))
        self.assertEqual(False, course_test1.is_in_files(file_id4))
        self.assertEqual(False, course_test1.is_in_files(file_id5))
        self.assertEqual(False, course_test1.is_in_files(file_id6))

        self.assertEqual(False, course_test2.is_in_files(file_id1))
        self.assertEqual(False, course_test2.is_in_files(file_id2))
        self.assertEqual(False, course_test2.is_in_files(file_id5))
        self.assertEqual(False, course_test2.is_in_files(file_id6))

        self.assertEqual(False, course_test3.is_in_files(file_id1))
        self.assertEqual(False, course_test3.is_in_files(file_id2))
        self.assertEqual(False, course_test3.is_in_files(file_id3))
        self.assertEqual(False, course_test3.is_in_files(file_id4))

    def test_remove_file_with_known_id(self):
        """remove_file(file_id) avec file_id se trouvant deja dans __files"""
        course_test1.remove_file(file_id1)
        course_test1.remove_file(file_id2)
        self.assertEqual(False, (file_id1 in course_test1.files))
        self.assertEqual(False, (file_id2 in course_test1.files))

        course_test2.remove_file(file_id3)
        course_test2.remove_file(file_id4)
        self.assertEqual(False, (file_id3 in course_test2.files))
        self.assertEqual(False, (file_id4 in course_test2.files))

        course_test3.remove_file(file_id5)
        course_test3.remove_file(file_id6)
        self.assertEqual(False, (file_id5 in course_test3.files))
        self.assertEqual(False, (file_id6 in course_test3.files))

        # retablissement des valeurs par defaut :
        course_test1.add_file(file_id1)
        course_test1.add_file(file_id2)
        course_test2.add_file(file_id3)
        course_test2.add_file(file_id4)
        course_test3.add_file(file_id5)
        course_test3.add_file(file_id6)

    def test_remove_teacher_with_unknown_name(self):
        """remove_file(file_id) avec file_id ne se trouvant pas dans __files"""
        self.assertRaises(NotInListException, course_test1.remove_file, file_id3)
        self.assertRaises(NotInListException, course_test1.remove_file, file_id4)
        self.assertRaises(NotInListException, course_test1.remove_file, file_id5)
        self.assertRaises(NotInListException, course_test1.remove_file, file_id6)

        self.assertRaises(NotInListException, course_test2.remove_file, file_id1)
        self.assertRaises(NotInListException, course_test2.remove_file, file_id2)
        self.assertRaises(NotInListException, course_test2.remove_file, file_id5)
        self.assertRaises(NotInListException, course_test2.remove_file, file_id6)

        self.assertRaises(NotInListException, course_test3.remove_file, file_id1)
        self.assertRaises(NotInListException, course_test3.remove_file, file_id2)
        self.assertRaises(NotInListException, course_test3.remove_file, file_id3)
        self.assertRaises(NotInListException, course_test3.remove_file, file_id4)


class TestStudentsCourse(unittest.TestCase):
    """Cette classe teste les methodes associees a la gestion des etudiants inscrits pour la classe Course
        * add_student(user_id)
        * remove_student(user_id)
        * is_in_students(user_id)"""

    def test_add_student_not_yet_in_list(self):
        """add_student(user_id) avec user_id ne se trouvant pas dans __students"""
        # Les ajouts course_test.add_student(user_id) sont effectues dans unittest_test_course_instances et testes ici
        self.assertEqual(True, (user_id1 in course_test1.students))
        self.assertEqual(True, (user_id2 in course_test1.students))

        self.assertEqual(True, (user_id3 in course_test2.students))
        self.assertEqual(True, (user_id4 in course_test2.students))

        self.assertEqual(True, (user_id5 in course_test3.students))
        self.assertEqual(True, (user_id6 in course_test3.students))

    def test_add_student_already_in_list(self):
        """add_student(user_id) avec user_id se trouvant deja dans __students"""
        self.assertRaises(AlreadyInListException, course_test1.add_student, user_id1)
        self.assertRaises(AlreadyInListException, course_test1.add_student, user_id2)

        self.assertRaises(AlreadyInListException, course_test2.add_student, user_id3)
        self.assertRaises(AlreadyInListException, course_test2.add_student, user_id4)

        self.assertRaises(AlreadyInListException, course_test3.add_student, user_id5)
        self.assertRaises(AlreadyInListException, course_test3.add_student, user_id6)

    def test_is_in_students_with_known_id(self):
        """is_in_students(user_id) avec user_id se trouvant deja dans __students"""
        self.assertEqual(True, course_test1.is_in_students(user_id1))
        self.assertEqual(True, course_test1.is_in_students(user_id2))

        self.assertEqual(True, course_test2.is_in_students(user_id3))
        self.assertEqual(True, course_test2.is_in_students(user_id4))

        self.assertEqual(True, course_test3.is_in_students(user_id5))
        self.assertEqual(True, course_test3.is_in_students(user_id6))

    def test_is_in_students_with_unknown_id(self):
        """is_in_students(user_id) avec user_id ne se trouvant pas dans __students"""
        self.assertEqual(False, course_test1.is_in_students(user_id3))
        self.assertEqual(False, course_test1.is_in_students(user_id4))
        self.assertEqual(False, course_test1.is_in_students(user_id5))
        self.assertEqual(False, course_test1.is_in_students(user_id6))

        self.assertEqual(False, course_test2.is_in_students(user_id1))
        self.assertEqual(False, course_test2.is_in_students(user_id2))
        self.assertEqual(False, course_test2.is_in_students(user_id5))
        self.assertEqual(False, course_test2.is_in_students(user_id6))

        self.assertEqual(False, course_test3.is_in_students(user_id1))
        self.assertEqual(False, course_test3.is_in_students(user_id2))
        self.assertEqual(False, course_test3.is_in_students(user_id3))
        self.assertEqual(False, course_test3.is_in_students(user_id4))

    def test_remove_student_with_known_id(self):
        """remove_student(user_id) avec user_id se trouvant deja dans __students"""
        course_test1.remove_student(user_id1)
        course_test1.remove_student(user_id2)
        self.assertEqual(False, (user_id1 in course_test1.students))
        self.assertEqual(False, (user_id2 in course_test1.students))

        course_test2.remove_student(user_id3)
        course_test2.remove_student(user_id4)
        self.assertEqual(False, (user_id3 in course_test2.students))
        self.assertEqual(False, (user_id4 in course_test2.students))

        course_test3.remove_student(user_id5)
        course_test3.remove_student(user_id6)
        self.assertEqual(False, (user_id5 in course_test3.students))
        self.assertEqual(False, (user_id6 in course_test3.students))

        # retablissement des valeurs par defaut :
        course_test1.add_student(user_id1)
        course_test1.add_student(user_id2)
        course_test2.add_student(user_id3)
        course_test2.add_student(user_id4)
        course_test3.add_student(user_id5)
        course_test3.add_student(user_id6)

    def test_remove_teacher_with_unknown_name(self):
        """remove_student(user_id) avec user_id ne se trouvant pas dans __students"""
        self.assertRaises(NotInListException, course_test1.remove_student, user_id3)
        self.assertRaises(NotInListException, course_test1.remove_student, user_id4)
        self.assertRaises(NotInListException, course_test1.remove_student, user_id5)
        self.assertRaises(NotInListException, course_test1.remove_student, user_id6)

        self.assertRaises(NotInListException, course_test2.remove_student, user_id1)
        self.assertRaises(NotInListException, course_test2.remove_student, user_id2)
        self.assertRaises(NotInListException, course_test2.remove_student, user_id5)
        self.assertRaises(NotInListException, course_test2.remove_student, user_id6)

        self.assertRaises(NotInListException, course_test3.remove_student, user_id1)
        self.assertRaises(NotInListException, course_test3.remove_student, user_id2)
        self.assertRaises(NotInListException, course_test3.remove_student, user_id3)
        self.assertRaises(NotInListException, course_test3.remove_student, user_id4)


if __name__ == "__main__":
    pass
