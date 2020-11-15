#! usr/bin/env python3

class Users:
    def __init__(self, username, fullname, pwd):
        self.__username = username
        self.__fullname = fullname
        self.__pwd = pwd

    @property
    def username(self):
        return self.__username

    @property
    def fullname(self):
        return self.__fullname

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

    def create_file(self, object_name, file_name, script, tag=None):
        pass


class Admins(Users):
    def __init__(self, username, fullname, pwd):
        super().__init__(username, fullname, pwd)

    def create_student(self, object_name, username, fullname, pwd):
        pass

    def create_admin(self, object_name, username, fullname, pwd):
        pass

    def create_course(self, object_name, name, teachers):
        pass


class Students(Users):
    def __init__(self, username, fullname, pwd):
        super().__init__(username, fullname, pwd)
        self.__student_id = StudentIdGenerator.generate_new_id()
        self.__courses = []
        self.__files = []

    @property
    def student_id(self):
        return self.__student_id

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

    def delete_file(self, file_id):
        self.__files.pop(file_id)
        pass


class Files:
    def __init__(self, name, student_id, pathname, script="false", tag=None):
        self.__name = name
        self.__script = script
        self.__file_id = FilesIdGenerator.generate_new_id()
        self.__student_id = student_id
        self.__tag = tag
        self.__pathname = pathname

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
    def student_id(self):
        return self.__student_id

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @tag.setter
    def tag(self, new_tag):
        self.__tag = new_tag

    @pathname.setter
    def pathname(self, new_pathname):
        self.__pathname = new_pathname


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


StudentIdGenerator = IdGenerator()
FilesIdGenerator = IdGenerator()
CoursesIdGenerator = IdGenerator()

if __name__ == '__main__':
    Dax = Users("dax", "Nicolas Daxhelet", "user123")
    Daxxra = Admins("daxxra", "Nicolas Daxhelet", "user124")
