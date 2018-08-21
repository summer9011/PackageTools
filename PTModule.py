#!/usr/bin/env python
import thread

asyncList = None

class PTModule:
    id = None
    moduleName = None
    localPath = None
    remotePath = None
    username = None
    password = None

    localVersion = ""
    remoteVersion = ""

    @classmethod
    def asyncModuleVersions(cls, moduleList, callback):
        if asyncList != None:
            thread.exit()

        thread.start_new_thread(PTModule.getVersion, (moduleList, callback))

    @classmethod
    def getVersion(cls, moduleList, callback):
        for module in moduleList:
            local = PTModule.getModuleLocalVersion(module)
            remote = PTModule.getModuleRemoteVersion(module)
            module.localVersion = local
            module.remoteVersion = remote
            callback(module)

    @classmethod
    def getModuleLocalVersion(cls, module):
        print "456"

    @classmethod
    def getModuleRemoteVersion(cls, module):
        print "123"

