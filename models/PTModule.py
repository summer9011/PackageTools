#!/usr/bin/env python

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

    @classmethod
    def checkVersionBigger(cls, str1, str2):
        bigger = False

        str1List = str1.split('.')
        str2List = str2.split('.')

        if len(str1List) > len(str2List):
            f = len(str1List)
        else:
            f = len(str2List)
        for i in range(f):
            try:
                if int(str1List[i]) > int(str2List[i]):
                    bigger = True
                    break
                elif int(str1List[i]) == int(str2List[i]):
                    continue
                else:
                    break
            except IndexError as e:
                if len(str1List) > len(str2List):
                    bigger = True
                    break
                else:
                    break
        return bigger

    def isNewer(self):
        newer = False
        if len(self.localVersion) > 0 and len(self.remoteVersion) > 0:
            newer = PTModule.checkVersionBigger(self.localVersion, self.remoteVersion)
        return newer

    def isOlder(self):
        older = False
        if len(self.localVersion) > 0 and len(self.remoteVersion) > 0:
            older = PTModule.checkVersionBigger(self.remoteVersion, self.localVersion)
        return older