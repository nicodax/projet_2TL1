#! usr/bin/env python3

import os


class Users:
    def __init__(self, username, fullname, pwd):
        self.__username = username
        self.__fullname = fullname
        self.__pwd = pwd
        self.__user_id = UserIdGenerator.generate_new_id()

    @property
    def username(self):
        return self.__username

    @property
    def fullname(self):
        return self.__fullname

    @property
    def user_id(self):
        return self.__user_id

    @username.setter
    def username(self, username):
        self.__username = username

    @fullname.setter
    def fullname(self, fullname):
        self.__fullname = fullname

    def pwd(self, old_pwd, new_pwd):
        if self.verify_pwd(old_pwd):
            self.__pwd = new_pwd

    def verify_pwd(self, pwd):
        return self.__pwd == pwd


class Admins(Users):
    def __init__(self, username, fullname, pwd):
        super().__init__(username, fullname, pwd)

    @staticmethod
    def create_student(username, fullname, pwd):
        All_students.add_object(username, Students(username, fullname, pwd))

    @staticmethod
    def delete_student(username):
        All_students.delete_object(username)

    @staticmethod
    def create_admin(username, fullname, pwd):
        All_admins.add_object(username, Admins(username, fullname, pwd))

    @staticmethod
    def delete_admin(username):
        All_admins.delete_object(username)

    @staticmethod
    def create_course(name, teachers):
        All_courses.add_object(name, Courses(name, teachers))

    @staticmethod
    def delete_course(name):
        All_courses.delete_object(name)


class Students(Users):
    def __init__(self, username, fullname, pwd):
        super().__init__(username, fullname, pwd)
        self.__courses = []
        self.__files = []

    @property
    def courses(self):
        return self.__courses

    @property
    def files(self):
        return self.__files

    def add_course(self, course_id):
        self.__courses.append(course_id)

    def delete_course(self, course_id):
        self.__courses.pop(course_id)

    def create_file(self, pathname, file_name, script, tag=None):
        All_files.add_object(file_name, Files(file_name, self.user_id, pathname, script, tag))
        self.__files.append(All_files.get_object(file_name).file_id)

    def delete_file(self, name):
        file_id = All_files.get_object(name).file_id
        self.__files.remove(file_id)
        pathname = All_files.get_object(name).pathname
        if os.path.exists(pathname):
            os.remove(pathname)
        All_files.delete_object(name)


class Files:
    def __init__(self, name, user_id, pathname, script=False, tag=None):
        self.__name = name
        self.__script = script
        self.__file_id = FilesIdGenerator.generate_new_id()
        self.__user_id = user_id
        self.__tag = tag
        self.__pathname = pathname
        try:
            with open(self.__pathname, 'x'):
                pass
        except FileExistsError:
            print(f'Le fichier : {self.__name} existe déjà')

    @property
    def file_id(self):
        return self.__file_id

    @property
    def name(self):
        return self.__name

    @property
    def script(self):
        return self.__script

    @property
    def tag(self):
        return self.__tag

    @property
    def pathname(self):
        return self.__pathname

    @property
    def user_id(self):
        return self.__user_id

    @tag.setter
    def tag(self, new_tag):
        self.__tag = new_tag

    def rename(self, new_name):
        self.__name = new_name
        new_pathname = os.path.dirname(self.__pathname) + "/" + new_name
        os.rename(self.__pathname, new_pathname)
        self.__pathname = new_pathname

    def move_file(self, new_pathname):
        os.rename(self.__pathname, new_pathname)
        self.__pathname = new_pathname

    def read_file(self):
        try:
            with open(self.__pathname, 'r') as file:
                for line in file:
                    print(line.rstrip())
        except FileNotFoundError:
            print(f'Le fichier {self.__name} est introuvable.')
        except IOError:
            print('Erreur IO.')

    def write_file(self, content_to_write):
        try:
            with open(self.__pathname, 'w+') as file:
                file.write(content_to_write)
        except IOError:
            print('Erreur IO.')

    def append_file(self, content_to_append):
        try:
            with open(self.__pathname, 'a+') as file:
                file.write(content_to_append)
        except IOError:
            print('Erreur IO.')


class Courses:
    def __init__(self, name, teachers):
        self.__name = name
        self.__teachers = teachers
        self.__course_id = CoursesIdGenerator.generate_new_id()
        self.__description = ""

    @property
    def name(self):
        return self.__name

    @property
    def teachers(self):
        return self.__teachers

    @property
    def course_id(self):
        return self.__course_id

    def __str__(self):
        return self.__description

    def add_teacher(self, name):
        self.__teachers.append(name)

    def delete_teacher(self, name):
        self.__teachers.pop(name)


class IdGenerator:
    def __init__(self):
        self.__id = 0

    def generate_new_id(self):
        self.__id += 1
        return self.__id


class Container:
    def __init__(self):
        self.__object_container = {}

    def add_object(self, name, obj):
        self.__object_container[name] = obj

    def get_object(self, name):
        return self.__object_container[name]

    def delete_object(self, name):
        del self.__object_container[name]


if __name__ == '__main__':
    # A METTRE DANS LE MAIN.PY PAR LA SUITE

    All_files = Container()
    All_users = Container()
    All_admins = Container()
    All_courses = Container()
    All_students = Container()

    UserIdGenerator = IdGenerator()
    FilesIdGenerator = IdGenerator()
    CoursesIdGenerator = IdGenerator()

    # TESTS

    Dax = Students("dax", "Nicolas Daxhelet", "user123")
    Daxxra = Admins("daxxra", "Nicolas Daxhelet", "user124")

    # ATTENTION : pathnames valables uniquement sur la machine de Nicolas Daxhelet
    Dax.create_file("//wsl$/Ubuntu-20.04/home/daxxramass/EPHEC/BLOC2/T2012/projet_2TL1/README.md", "README.md", False)
    All_files.get_object("README.md").read_file()

    Dax.create_file("//wsl$/Ubuntu-20.04/home/daxxramass/EPHEC/BLOC2/T2012/hello_world.txt", "hello_world.txt", False)
    All_files.get_object("hello_world.txt").write_file("Hello World !\nNew line here")
    All_files.get_object("hello_world.txt").append_file("\nAnd again...")
    All_files.get_object("hello_world.txt").read_file()
    Dax.delete_file("hello_world.txt")
