#!/usr/bin/env python

import tools.PTModuleHelper as Helper

class PTModuleRepo:
    id = 0
    url = ""
    user = ""
    pwd = ""

    def __init__(self):
        self.id = 0
        self.url = ""
        self.user = ""
        self.pwd = ""

    def full(self, user):
        if len(self.url) > 0 and len(self.user) and len(self.pwd):
            if user != None:
                if self.user == user:
                    return True
            else:
                return True
        return False

class PTModule:
    id = 0
    name = ""
    path = ""
    sepcName = ""
    trunkId = 0
    trunkName = ""

    repo = None

    localVersion = ""
    remoteVersion = ""

    isPublishing = False

    def __init__(self):
        self.id = 0
        self.name = ""
        self.path = ""
        self.sepcName = ""
        self.trunkId = 0
        self.trunkName = ""

        self.repo = None

        self.localVersion = ""
        self.remoteVersion = ""

        self.isPublishing = False

    def isNewer(self):
        newer = False
        if len(self.localVersion) > 0 and len(self.remoteVersion) > 0:
            newer = Helper.checkVersionBigger(self.localVersion, self.remoteVersion)
        return newer

    def isOlder(self):
        older = False
        if len(self.localVersion) > 0 and len(self.remoteVersion) > 0:
            older = Helper.checkVersionBigger(self.remoteVersion, self.localVersion)
        return older