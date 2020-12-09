#!/usr/bin/env python3
import getpass
import unittest
import mock


class TestClass:
    def __init__(self):
        self.__pwd = ""

    @property
    def pwd(self):
        return self.__pwd

    @pwd.setter
    def pwd(self, pwd):
        self.__pwd = pwd


Test = TestClass()


class ErrorException(Exception):
    pass


def test_function():
    test1 = getpass.getpass()
    test2 = getpass.getpass()
    if test1 == test2:
        Test.pwd = test1
    else:
        raise ErrorException


class TestTest(unittest.TestCase):
    @mock.patch('getpass.getpass', side_effect=["test", "test"])
    def test_test_function(self, side_effect):
        test_function()
        test_class_pwd = Test.pwd
        self.assertEqual("test", test_class_pwd)
