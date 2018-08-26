#!/usr/bin/env python
import thread
import os
import re
import urllib2
import time
import wx

asyncList = None

class PTModule:
    id = None
    moduleName = None
    localPath = None
    remotePath = None
    username = None
    password = None
    repoId = 0

    localVersion = ""
    remoteVersion = ""

    isPublishing = False

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
    def asyncModuleVersions(cls, moduleList, logCallback, resultCallback):
        if asyncList != None:
            thread.exit()

        thread.start_new_thread(PTModule.getVersion, (moduleList, logCallback, resultCallback))

    @classmethod
    def getVersion(cls, moduleList, logCallback, resultCallback):
        for module in moduleList:
            local = PTModule.getModuleLocalVersion(module, logCallback)
            remote = PTModule.getModuleTagsRemoteVersion(module, logCallback)
            module.localVersion = local
            module.remoteVersion = remote
            resultCallback(module)

    @classmethod
    def getModuleLocalVersion(cls, module, logCallback):
        wx.CallAfter(logCallback, "\nGet local version -- url: %s\n" % module.localPath)

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
                    wx.CallAfter(logCallback, "\nGet local version -- version %s\n" % localVersion)
                    break
                line = f.readline()
            f.close()
        else:
            wx.CallAfter(logCallback, "\nGet local version -- Can't find local version.\n")

        return localVersion

    @classmethod
    def getModuleTagsRemoteVersion(cls, module, logCallback):
        try:
            remoteVersion = "0"
            lastTimestamp = 0

            tagPath = "%s/tags" % module.remotePath
            wx.CallAfter(logCallback, "\nGet remote tags version -- url: %s\n" % tagPath)

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
                    lastModifiedStr = tagRet.info().getheader('Last-Modified')
                    tmpTime = time.strptime(lastModifiedStr, "%a, %d %b %Y %H:%M:%S %Z")
                    tmpTimestamp = int(time.mktime(tmpTime))

                    if tmpTimestamp > lastTimestamp:
                        lastTimestamp = tmpTimestamp
                        remoteVersion = serverVersion

                line = ret.readline()

            wx.CallAfter(logCallback, "\nGet remote tags version -- version %s\n" % remoteVersion)

            return remoteVersion
        except Exception as e:
            wx.CallAfter(logCallback, "\nGet remote tags version -- %s\n" % e)
            return ""

    @classmethod
    def getModuleTrunkRemoteVersion(cls, module, logCallback):
        try:
            remoteTrunkVersion = ""

            trunkSpecPath = "%s/trunk/%s.podspec" % (module.remotePath, module.moduleName)
            wx.CallAfter(logCallback, "\nGet remote trunk version -- url: %s\n" % trunkSpecPath)

            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, trunkSpecPath, module.username, module.password)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)

            opener = urllib2.build_opener(handler)
            opener.open(trunkSpecPath)
            urllib2.install_opener(opener)

            ret = urllib2.urlopen(trunkSpecPath)

            line = ret.readline()
            while line:
                match = re.match(r'.*s.version.*=.*\'(.*)\'', line, re.M|re.I)
                if match:
                    remoteTrunkVersion = match.group(1)
                    wx.CallAfter(logCallback, "\nGet remote trunk version -- version %s\n" % remoteTrunkVersion)
                    break
                line = ret.readline()

            return remoteTrunkVersion
        except Exception as e:
            wx.CallAfter(logCallback, "\nGet remote trunk version -- %s\n" % e)
            return ""
