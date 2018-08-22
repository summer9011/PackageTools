#!/usr/bin/env python
import thread
import os
import re
import urllib2
import time

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

    def isNewer(self):
        newer = False
        if len(self.localVersion) > 0 and len(self.remoteVersion) > 0:
            localList = self.localVersion.split('.')
            remoteList = self.remoteVersion.split('.')

            if len(localList) > len(remoteList):
                f = len(localList)
            else:
                f = len(remoteList)
            for i in range(f):
                try:
                    if int(localList[i]) > int(remoteList[i]):
                        newer = True
                        break
                    elif int(localList[i]) == int(remoteList[i]):
                        continue
                    else:
                        break
                except IndexError as e:
                    if len(localList) > len(remoteList):
                        newer = True
                        break
                    else:
                        break

        return newer

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
        localVersion = ""
        fileName = None
        list = os.listdir(module.localPath)
        for name in list:
            if name.endswith(".podspec"):
                fileName = name
                break
        if fileName != None:
            filePath = os.path.join(module.localPath, fileName)
            f = open(filePath)
            line = f.readline()
            while line:
                match = re.match(r'.*s.version.*=.*\'(.*)\'', line, re.M|re.I)
                if match:
                    localVersion = match.group(1)
                    break
                line = f.readline()
            f.close()
        return localVersion

    @classmethod
    def getModuleRemoteVersion(cls, module):
        try:
            remoteVersion = ""
            lastTimestamp = 0

            tagPath = "%s/tags" % module.remotePath
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, tagPath, module.username, module.password)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)

            opener = urllib2.build_opener(handler)
            opener.open(tagPath)
            urllib2.install_opener(opener)

            ret = urllib2.urlopen(tagPath)

            line = ret.readline()
            while line:
                match = re.match(r'.*<a.*>(.*)/</a>.*', line, re.M|re.I)
                if match:
                    serverVersion = match.group(1)
                    onePath = "%s/%s" % (tagPath, serverVersion)
                    tagRet = urllib2.urlopen(onePath)

                    print onePath

                    lastModifiedStr = tagRet.info().getheader('Last-Modified')
                    tmpTime = time.strptime(lastModifiedStr, "%a, %d %b %Y %H:%M:%S %Z")
                    tmpTimestamp = int(time.mktime(tmpTime))

                    if tmpTimestamp > lastTimestamp:
                        lastTimestamp = tmpTimestamp
                        remoteVersion = serverVersion

                line = ret.readline()
            return remoteVersion
        except:
            return ""