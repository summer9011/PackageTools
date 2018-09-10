#!/usr/bin/env python
import thread
import os
import re
import urllib2
import time
import wx
from PTDBManager import PTDBManager

def asyncModuleVersions(moduleList, logCallback, resultCallback):
    thread.start_new_thread(getVersion, (moduleList, logCallback, resultCallback))

def getVersion(moduleList, logCallback, resultCallback):
    for module in moduleList:
        local = getModuleLocalVersion(module, logCallback)
        remote = getModuleTagsRemoteVersion(module, logCallback)
        module.localVersion = local
        module.remoteVersion = remote
        resultCallback(module)

def getModuleLocalVersion(module, logCallback):
    return getLocalVersion(module.localPath, logCallback)

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
    return getModuleRemoteVersion(module, "trunk", logCallback)

def getModuleRemoteVersion(module, part, logCallback):
    try:
        remoteTrunkVersion = ""
        podspecName = "%s/%s.podspec" % (part, module.name)
        res = getRemoteContent(module, "%s/"+podspecName)
        if res != None:
            trunkSpecPath = res[0]
            ret = res[1]
            wx.CallAfter(logCallback, "\nGet remote version -- url: %s\n" % trunkSpecPath)
            line = ret.readline()
            while line:
                match = re.match(r'.*s.version.*=.*\'(.*)\'', line, re.M | re.I)
                if match:
                    remoteTrunkVersion = match.group(1)
                    wx.CallAfter(logCallback, "\nGet remote version -- version %s\n" % remoteTrunkVersion)
                    break
                line = ret.readline()

            return remoteTrunkVersion
        else:
            wx.CallAfter(logCallback, "\nGet remote version -- Can't find module's code repo\n")
            return ""
    except Exception as e:
        wx.CallAfter(logCallback, "\nGet remote version -- %s\n" % e)
        return ""

def getRemoteContent(module, pathPattern):
    codeRepo = PTDBManager().getCodeRepo(module.codeRepoId)
    if codeRepo != None:
        moduelRemotePath = "%s/%s" % (codeRepo.remotePath, module.name)
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

def getModuleRemoteBranches(module, logCallback, resultCallback):
    thread.start_new_thread(getBranches, (module, logCallback, resultCallback))

def getBranches(module, logCallback, resultCallback):
    branchList = None
    try:
        res = getRemoteContent(module, "%s/branches")
        if res != None:
            tagPath = res[0]
            ret = res[1]
            wx.CallAfter(logCallback, "\nGet remote branches -- url: %s\n" % tagPath)
            branchList = []
            branchNames = []
            line = ret.readline()
            while line:
                match = re.match(r'.*<a.*>(.*)/</a>.*', line, re.M | re.I)
                if match:
                    moduleBranch = PTRemoteModuleBranch()
                    moduleBranch.remoteName = match.group(1)
                    moduleBranch.version = getModuleRemoteVersion(module, "branches/%s" % moduleBranch.remoteName, logCallback)
                    branchList.append(moduleBranch)
                    branchNames.append(moduleBranch.remoteName)
                line = ret.readline()
            wx.CallAfter(logCallback, "\nGet remote branches -- branches %s\n" % branchNames)
            wx.CallAfter(resultCallback, branchList)
        else:
            wx.CallAfter(logCallback, "\nGet remote branches -- Can't find module's code repo\n")
            wx.CallAfter(resultCallback, branchList)
    except Exception as e:
        wx.CallAfter(logCallback, "\nGet remote branches -- %s\n" % e)
        wx.CallAfter(resultCallback, branchList)

def getBranchLocalVersion(moduleBranch, logCallback):
    return getLocalVersion(moduleBranch.localPath, logCallback)

def getLocalVersion(localPath, logCallback):
    wx.CallAfter(logCallback, "\nGet local version -- url: %s\n" % localPath)

    localVersion = ""
    fileName = None
    list = os.listdir(localPath)
    for name in list:
        if name.endswith(".podspec"):
            fileName = name
            break
    if fileName != None:
        filePath = os.path.join(localPath, fileName)
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