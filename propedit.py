"""
 Property editor
"""
import os, sys, tempfile, subprocess

class PropertyEditor(object):
    def __init__(self, properties):
        self.properties = properties

    def __create_propfile(self):
        propfile = \
"""\
# Please type the following fields
# Line following to # will be ignored
#
# For example, when you type 'name' field, you will type like:
#
#    # name ######
#    My Project Name
#
#    # Other property ######
#    ...

"""
        for p in self.properties:
            propfile += "# {} #######".format(p['name'])
            propfile += "\n\n"
        return propfile

    def edit(self):
        print self.__create_propfile()


if __name__ == "__main__":
    # Test code
    p = PropertyEditor([{'name':'p1'}, {'name':'p2'}])
    p.edit()
