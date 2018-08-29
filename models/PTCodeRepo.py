#!/usr/bin/env python

class PTCodeRepo:
    id = None
    name = None
    remotePath = None
    username = None
    password = None
    type = None

    def typeName(self):
        if self.type == 1:
            return "Svn"
        elif self.type == 2:
            return "Git"
        else:
            return "Unkown"