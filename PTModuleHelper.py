#!/usr/bin/env python
import thread
import os
import re
import urllib2
import time
import wx
from PTDBManager import PTDBManager

asyncList = None

def asyncModuleVersions(moduleList, logCallback, resultCallback):
    if asyncList != None:
        thread.exit()

    thread.start_new_thread(getVersion, (moduleList, logCallback, resultCallback))

def getVersion(moduleList, logCallback, resultCallback):
    for module in moduleList:
        local = getModuleLocalVersion(module, logCallback)
        remote = getModuleTagsRemoteVersion(module, logCallback)
        module.localVersion = local
        module.remoteVersion = remote
        resultCallback(module)

def getModuleLocalVersion(module, logCallback):
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
            match = re.match(r'.*s.version.*=.*\'(.*)\'', line, re.M | re.I)
            if match:
                localVersion = match.group(1)
                wx.CallAfter(logCallback, "\nGet local version -- version %s\n" % localVersion)
                break
            line = f.readline()
        f.close()
    else:
        wx.CallAfter(logCallback, "\nGet local version -- Can't find local version.\n")

    return localVersion

def getModuleTagsRemoteVersion(module, logCallback):
    try:
        remoteVersion = "0"
        lastTimestamp = 0
        res = getRemoteContent(module, "%s/tags")
        if res != None:
            tagPath = res[0]
            ret = res[1]
            wx.CallAfter(logCallback, "\nGet remote tags version -- url: %s\n" % tagPath)
            line = ret.readline()
            while line:
                match = re.match(r'.*<a.*>(.*)/</a>.*', line, re.M | re.I)
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
        else:
            wx.CallAfter(logCallback, "\nGet remote tags version -- Can't find module's code repo\n")
            return ""
    except Exception as e:
        wx.CallAfter(logCallback, "\nGet remote tags version -- %s\n" % e)
        return ""

def getModuleTrunkRemoteVersion(module, logCallback):
    try:
        remoteTrunkVersion = ""
        podspecName = "/trunk/%s.podspec" % module.name
        res = getRemoteContent(module, "%s/"+podspecName)
        if res != None:
            trunkSpecPath = res[0]
            ret = res[1]
            wx.CallAfter(logCallback, "\nGet remote trunk version -- url: %s\n" % trunkSpecPath)
            line = ret.readline()
            while line:
                match = re.match(r'.*s.version.*=.*\'(.*)\'', line, re.M | re.I)
                if match:
                    remoteTrunkVersion = match.group(1)
                    wx.CallAfter(logCallback, "\nGet remote trunk version -- version %s\n" % remoteTrunkVersion)
                    break
                line = ret.readline()

            return remoteTrunkVersion
        else:
            wx.CallAfter(logCallback, "\nGet remote trunk version -- Can't find module's code repo\n")
            return ""
    except Exception as e:
        wx.CallAfter(logCallback, "\nGet remote trunk version -- %s\n" % e)
        return ""

def getRemoteContent(module, pathPattern):
    codeRepo = PTDBManager().getCodeRepo(module.codeRepoId)
    if codeRepo != None:
        moduelRemotePath = os.path.join(codeRepo.remotePath, module.name)
        path = pathPattern % moduelRemotePath
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, path, codeRepo.username, codeRepo.password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        opener.open(path)
        urllib2.install_opener(opener)
        return (path, urllib2.urlopen(path))
    else:
        return None