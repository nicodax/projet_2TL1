#! usr/bin/env python3

from classes.classes import *

if __name__ == "__main__":
    Dax = Students("dax", "Nicolas Daxhelet", "user123")
    Daxxra = Admins("daxxra", "Nicolas Daxhelet", "user111")
    Greg = Students("greg", "Gregoire Delannoit", "user123")
    TheGregouze = Admins("TheGregouze", "Gregoire Delannoit", "user111")

    All_students.add_object("dax", Dax)
    All_students.add_object("greg", Greg)
    All_admins.add_object("daxxra", Daxxra)
    All_admins.add_object("TheGregouze", TheGregouze)
