#!/usr/bin/env python3
import unittest

from classes.exceptions import AlreadyInListException, NotInListException
from classes.unit_testing.unittest_test_file_instances import tag1, file_test1, tag2, tag3, tag4, tag5, tag6, \
    file_test2, file_test3


class TestTagsFile(unittest.TestCase):
    """Cette classe teste les methodes associees a la gestion des tags pour la classe File
        * add_tag(tag)
        * delete_tag(tag)
        * is_in_tags(tag)"""

    def test_add_tag_not_yet_in_list(self):
        """add_tag(new_tag) avec new_tag ne se trouvant pas dans __tags"""
        # Les ajouts file_test.add_tag(new_tag) sont effectues dans unittest_test_file_instances et testes ici
        self.assertEqual(True, (tag1 in file_test1.tags))
        self.assertEqual(True, (tag2 in file_test1.tags))

        self.assertEqual(True, (tag3 in file_test2.tags))
        self.assertEqual(True, (tag4 in file_test2.tags))

        self.assertEqual(True, (tag5 in file_test3.tags))
        self.assertEqual(True, (tag6 in file_test3.tags))

    def test_add_tag_already_in_list(self):
        """add_tag(new_tag) avec new_tag se trouvant deja dans __tags"""
        self.assertRaises(AlreadyInListException, file_test1.add_tag, tag1)
        self.assertRaises(AlreadyInListException, file_test1.add_tag, tag2)

        self.assertRaises(AlreadyInListException, file_test2.add_tag, tag3)
        self.assertRaises(AlreadyInListException, file_test2.add_tag, tag4)

        self.assertRaises(AlreadyInListException, file_test3.add_tag, tag5)
        self.assertRaises(AlreadyInListException, file_test3.add_tag, tag6)

    def test_is_in_tags_with_known_tag(self):
        """is_in_tags(tag) avec tag se trouvant deja dans __tags"""
        self.assertEqual(True, file_test1.is_in_tags(tag1))
        self.assertEqual(True, file_test1.is_in_tags(tag2))

        self.assertEqual(True, file_test2.is_in_tags(tag3))
        self.assertEqual(True, file_test2.is_in_tags(tag4))

        self.assertEqual(True, file_test3.is_in_tags(tag5))
        self.assertEqual(True, file_test3.is_in_tags(tag6))

    def test_is_in_tags_with_unknown_tag(self):
        """is_in_tags(tag) avec tag ne se trouvant pas dans __teachers"""
        self.assertEqual(False, file_test1.is_in_tags(tag3))
        self.assertEqual(False, file_test1.is_in_tags(tag4))
        self.assertEqual(False, file_test1.is_in_tags(tag5))
        self.assertEqual(False, file_test1.is_in_tags(tag6))

        self.assertEqual(False, file_test2.is_in_tags(tag1))
        self.assertEqual(False, file_test2.is_in_tags(tag2))
        self.assertEqual(False, file_test2.is_in_tags(tag5))
        self.assertEqual(False, file_test2.is_in_tags(tag6))

        self.assertEqual(False, file_test3.is_in_tags(tag1))
        self.assertEqual(False, file_test3.is_in_tags(tag2))
        self.assertEqual(False, file_test3.is_in_tags(tag3))
        self.assertEqual(False, file_test3.is_in_tags(tag4))

    def test_delete_tag_with_known_tag(self):
        """delete_tag(tag) avec tag se trouvant deja dans __tags"""
        file_test1.delete_tag(tag1)
        file_test1.delete_tag(tag2)
        self.assertEqual(False, (tag1 in file_test1.tags))
        self.assertEqual(False, (tag2 in file_test1.tags))

        file_test2.delete_tag(tag3)
        file_test2.delete_tag(tag4)
        self.assertEqual(False, (tag3 in file_test2.tags))
        self.assertEqual(False, (tag4 in file_test2.tags))

        file_test3.delete_tag(tag5)
        file_test3.delete_tag(tag6)
        self.assertEqual(False, (tag5 in file_test3.tags))
        self.assertEqual(False, (tag6 in file_test3.tags))

        # retablissement des valeurs par defaut :
        file_test1.add_tag(tag1)
        file_test1.add_tag(tag2)
        file_test2.add_tag(tag3)
        file_test2.add_tag(tag4)
        file_test3.add_tag(tag5)
        file_test3.add_tag(tag6)

    def test_delete_tag_with_unknown_tag(self):
        """remove_teacher(name) avec name ne se trouvant pas dans __teachers"""
        self.assertRaises(NotInListException, file_test1.delete_tag, tag3)
        self.assertRaises(NotInListException, file_test1.delete_tag, tag4)
        self.assertRaises(NotInListException, file_test1.delete_tag, tag5)
        self.assertRaises(NotInListException, file_test1.delete_tag, tag6)

        self.assertRaises(NotInListException, file_test2.delete_tag, tag1)
        self.assertRaises(NotInListException, file_test2.delete_tag, tag2)
        self.assertRaises(NotInListException, file_test2.delete_tag, tag5)
        self.assertRaises(NotInListException, file_test2.delete_tag, tag6)

        self.assertRaises(NotInListException, file_test3.delete_tag, tag1)
        self.assertRaises(NotInListException, file_test3.delete_tag, tag2)
        self.assertRaises(NotInListException, file_test3.delete_tag, tag3)
        self.assertRaises(NotInListException, file_test3.delete_tag, tag4)


if __name__ == "__main__":
    pass
