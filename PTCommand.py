#!/usr/bin/env python
import commands
import os
import thread
import wx
from PTDBManager import PTDBManager
from PTModule import PTModule
from PTSpecRepo import PTSpecRepo

class PTCommand:
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance=object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def publishModule(self, module, logCallback, completeCallback):
        thread.start_new_thread(self.publishModuleWithShell, (module, logCallback, completeCallback))

    def publishModuleWithShell(self, module, logCallback, completeCallback):
        svnCopyToTag = "svn copy %s/trunk %s/tags/%s -m \"release to %s\"" % (module.remotePath, module.remotePath, module.localVersion, module.localVersion)
        self.logCommand(svnCopyToTag, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(svnCopyToTag)
        self.logOutput(copyRet, copyOutput, logCallback)

        if copyRet == 0:
            repoInfo = PTDBManager().getSpecRepo(module.repoId)
            if repoInfo != None:
                podPush = "cd %s; /usr/local/bin/pod repo-svn push %s %s.podspec" % (module.localPath, repoInfo.repoName, module.moduleName)
                self.logCommand(podPush, logCallback)
                pushRet, pushOutput = commands.getstatusoutput(podPush)
                self.logOutput(pushRet, pushOutput, logCallback)

                if pushRet == 0:
                    wx.CallAfter(logCallback, "\npublish module %s successfully!!!\n" % module.moduleName)
                    wx.CallAfter(completeCallback, True, module)
                else:
                    wx.CallAfter(logCallback, "\npush %s's podspec to repo failed!!!\n" % module.moduleName)
                    wx.CallAfter(completeCallback, False, module)
            else:
                wx.CallAfter(logCallback, "\npodspec repo not exist!!!\n")
                wx.CallAfter(completeCallback, False, module)
        else:
            wx.CallAfter(logCallback, "\ncopy module %s trunk to tags error!!!\n" % module.moduleName)
            wx.CallAfter(completeCallback, False, module)

    def addSpecRepo(self, specRepo, logCallback, completeCallback):
        thread.start_new_thread(self.addSpecRepoWithShell, (specRepo, logCallback, completeCallback))

    def addSpecRepoWithShell(self, specRepo, logCallback, completeCallback):
        addRepo = "/usr/local/bin/pod repo-svn add %s %s" % (specRepo.repoName, specRepo.remotePath)
        self.logCommand(addRepo, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(addRepo)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, specRepo)

    def testPodCommand(self, logCallback):
        testPod = "echo $HOME; echo `pwd`; cd $HOME; /usr/local/bin/pod --version"
        self.logCommand(testPod, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(testPod)
        self.logOutput(copyRet, copyOutput, logCallback)

    def logCommand(self, command, callback):
        wx.CallAfter(callback, "\n=====  %s  =====\n" % command)

    def logOutput(self, stats, output, callback):
        wx.CallAfter(callback, "status : %s\n" % stats)
        if len(output) > 0:
            wx.CallAfter(callback, "%s\n" % output)