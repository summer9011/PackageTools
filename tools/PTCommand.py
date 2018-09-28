#!/usr/bin/env python
import commands
import thread
import wx
import re
import os
import sqlite3
import enchant
from PTDBManager import PTDBManager
from PTCommandPathConfig import PTCommandPathConfig

class PTCommand:
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance=object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def svnUpdateModule(self, module, logCallback, resultCallback):
        thread.start_new_thread(self.svnUpdateModuleInThread, (module, logCallback, resultCallback))

    def svnUpdateModuleInThread(self, module, logCallback, resultCallback):
        testSvn = "cd %s; %s up" % (module.path, PTCommandPathConfig().command("svn"))
        self.logCommand(testSvn, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(testSvn)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(resultCallback, copyRet, copyOutput)

    def svnCheckConflict(self, module, logCallback, resultCallback):
        thread.start_new_thread(self.svnCheckConflictInThread, (module, logCallback, resultCallback))

    def svnCheckConflictInThread(self, module, logCallback, resultCallback):
        d = enchant.Dict("en_US")
        testSvn = "cd %s; %s st" % (module.path, PTCommandPathConfig().command("svn"))
        self.logCommand(testSvn, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(testSvn)
        self.logOutput(copyRet, copyOutput, logCallback)

        if copyRet == 0:
            files = []
            conflictFiles = []
            if len(copyOutput) > 0:
                for line in copyOutput.split('\n'):
                    str = line[0:8].strip()
                    if len(str) > 1 and d.check(str) == True:
                        break
                    else:
                        if line[0] == "A" or line[0] == "D" or line[0] == "M" or line[0] == "R" or line[0] == "?" or line[0] == "!":
                            files.append((line[0], line[8:]))
                        elif line[0] == "C":
                            conflictFiles.append((line[0], line[8:]))
            wx.CallAfter(resultCallback, copyRet, (files, conflictFiles))
        else:
            wx.CallAfter(resultCallback, copyRet, copyOutput)

    def svnCommitFiles(self, module, commitFiles, addFiles, deleteFiles, message, logCallback, resultCallback):
        thread.start_new_thread(self.svnCommitFilesInThread, (module, commitFiles, addFiles, deleteFiles, message, logCallback, resultCallback))

    def svnCommitFilesInThread(self, module, commitFiles, addFiles, deleteFiles, message, logCallback, resultCallback):
        addFileSuccess = True
        if len(addFiles) > 0:
            testSvn = "cd %s; %s add %s" % (module.path, PTCommandPathConfig().command("svn"), " ".join(addFiles))
            self.logCommand(testSvn, logCallback)
            copyRet, copyOutput = commands.getstatusoutput(testSvn)
            self.logOutput(copyRet, copyOutput, logCallback)
            addFileSuccess = (copyRet == 0)

        deleteFileSuccess = True
        if len(deleteFiles) > 0:
            testSvn = "cd %s; %s del %s" % (module.path, PTCommandPathConfig().command("svn"), " ".join(deleteFiles))
            self.logCommand(testSvn, logCallback)
            copyRet, copyOutput = commands.getstatusoutput(testSvn)
            self.logOutput(copyRet, copyOutput, logCallback)
            deleteFileSuccess = (copyRet == 0)

        commitFileSuccess = True
        if len(addFiles) > 0 or len(deleteFiles) > 0 or len(commitFiles) > 0:
            needCommitFiles = addFiles+deleteFiles+commitFiles
            testSvn = "cd %s; %s ci %s -m \"%s\"" % (module.path, PTCommandPathConfig().command("svn"), " ".join(needCommitFiles), message)
            self.logCommand(testSvn, logCallback)
            copyRet, copyOutput = commands.getstatusoutput(testSvn)
            self.logOutput(copyRet, copyOutput, logCallback)
            commitFileSuccess = (copyRet == 0)

        wx.CallAfter(resultCallback, (addFileSuccess and deleteFileSuccess and commitFileSuccess))

    def tagModule(self, module, logCallback, completeCallback):
        thread.start_new_thread(self.tagModuleInThread, (module, logCallback, completeCallback))

    def tagModuleInThread(self, module, logCallback, completeCallback):
        modulePath = module.repo.url+"/"+module.name
        tagPath = modulePath+"/tags/"+module.localVersion
        if module.isTrunk() == True:
            fromPath = modulePath+"/trunk"
        else:
            fromPath = modulePath+"/branches/"+module.name
        tagCopy = "%s copy %s %s -m \"release to %s\"" % (PTCommandPathConfig().command("svn"), fromPath, tagPath, module.localVersion)
        self.logCommand(tagCopy, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(tagCopy)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, copyRet, copyOutput)

    def publishModule(self, module, logCallback, completeCallback):
        thread.start_new_thread(self.publishModuleInThread, (module, logCallback, completeCallback))

    def publishModuleInThread(self, module, logCallback, completeCallback):
        podPush = "cd %s; %s repo-svn push %s %s.podspec" % (module.path, PTCommandPathConfig().command("pod"), module.sepcName, module.trunkName)
        self.logCommand(podPush, logCallback)
        pushRet, pushOutput = commands.getstatusoutput(podPush)
        self.logOutput(pushRet, pushOutput, logCallback)

        if pushRet == 0:
            wx.CallAfter(logCallback, "publish module %s successfully!!!\n" % module.name)
            wx.CallAfter(completeCallback, True, module)
        else:
            wx.CallAfter(logCallback, "push %s's podspec to repo failed!!!\n" % module.name)
            wx.CallAfter(completeCallback, False, module)

    # Pod manager
    def getSpecRepoList(self, logCallback, completeCallback):
        thread.start_new_thread(self.getSpecRepoListWithShell, (logCallback, completeCallback))

    def getSpecRepoListWithShell(self, logCallback, completeCallback):
        testPod = "cd $HOME; %s repo list" % PTCommandPathConfig().command("pod")
        self.logCommand(testPod, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(testPod)
        self.logOutput(copyRet, copyOutput, logCallback)

        specRepoList = []
        typeStr = None
        for line in copyOutput.split('\n'):
            match = re.match(r'.*Type: (.*)', line, re.M | re.I)
            if match:
                str = match.group(1)
                wx.CallAfter(logCallback, "\nGet spec repo type -- type %s\n" % str)
                if str == "local":
                    typeStr = str
            if typeStr != None:
                match = re.match(r'.*Path: (.*)', line, re.M | re.I)
                if match:
                    localPath = match.group(1)
                    wx.CallAfter(logCallback, "\nGet spec repo local path -- path %s\n" % localPath)

                    dbPath = os.path.join(localPath, ".svn", "wc.db")
                    if os.path.exists(dbPath):
                        conn = sqlite3.connect(dbPath)
                        cursor = conn.cursor()
                        cursor.execute("select * from REPOSITORY;")
                        result = cursor.fetchone()
                        if result != None:
                            remoteRoot = result[1]
                            name = os.path.basename(localPath)
                            remotePath = "%s/%s" % (remoteRoot, name)
                            wx.CallAfter(logCallback, "\nGet spec repo remote path -- path %s\n" % remotePath)
                            specRepoList.append((name, remotePath))
                        cursor.close()
                        conn.close()
                    typeStr = None
        wx.CallAfter(completeCallback, specRepoList)

    def addSpecRepo(self, name, remotePath, logCallback, completeCallback):
        thread.start_new_thread(self.addSpecRepoWithShell, (name, remotePath, logCallback, completeCallback))

    def addSpecRepoWithShell(self, name, remotePath, logCallback, completeCallback):
        addSpecRepo = "%s repo-svn add %s %s" % (PTCommandPathConfig().command("pod"), name, remotePath)
        self.logCommand(addSpecRepo, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(addSpecRepo)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, name, remotePath)

    def removeSpecRepo(self, name, logCallback, completeCallback):
        thread.start_new_thread(self.removeSpecRepoWithShell, (name, logCallback, completeCallback))

    def removeSpecRepoWithShell(self, name, logCallback, completeCallback):
        addSpecRepo = "%s repo remove %s" % (PTCommandPathConfig().command("pod"), name)
        self.logCommand(addSpecRepo, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(addSpecRepo)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, name)

    # Check pod command
    def checkPodCommand(self, logCallback, completeCallback):
        thread.start_new_thread(self.checkPodCommandWithShell, (logCallback, completeCallback))

    def checkPodCommandWithShell(self, logCallback, completeCallback):
        testPod = "cd $HOME; %s --version" % PTCommandPathConfig().command("pod")
        self.logCommand(testPod, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(testPod)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, True)

    # Check svn command
    def checkSvnCommand(self, logCallback, completeCallback):
        thread.start_new_thread(self.checkSvnCommandWithShell, (logCallback, completeCallback))

    def checkSvnCommandWithShell(self, logCallback, completeCallback):
        testSvn = "cd $HOME; %s --version" % PTCommandPathConfig().command("svn")
        self.logCommand(testSvn, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(testSvn)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, True)

    # log caller
    def logCommand(self, command, callback):
        wx.CallAfter(callback, "%s\n" % command)

    def logOutput(self, stats, output, callback):
        wx.CallAfter(callback, "status : %s\n" % stats)
        if len(output) > 0:
            wx.CallAfter(callback, "%s\n" % output)