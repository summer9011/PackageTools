#!/usr/bin/env python
import commands
import thread
import wx
import os
from PTDBManager import PTDBManager

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
        codeRepoInfo = PTDBManager().getCodeRepo(module.codeRepoId)
        specRepoInfo = PTDBManager().getSpecRepo(module.specRepoId)
        if codeRepoInfo != None and specRepoInfo != None:
            moduelRemotePath = os.path.join(codeRepoInfo.remotePath, module.name)
            svnCopyToTag = "svn copy %s/trunk %s/tags/%s -m \"release to %s\"" % (moduelRemotePath, moduelRemotePath, module.localVersion, module.localVersion)
            self.logCommand(svnCopyToTag, logCallback)
            copyRet, copyOutput = commands.getstatusoutput(svnCopyToTag)
            self.logOutput(copyRet, copyOutput, logCallback)
            if copyRet == 0:
                podPush = "cd %s; /usr/local/bin/pod repo-svn push %s %s.podspec" % (
                    module.localPath, specRepoInfo.name, module.name)
                self.logCommand(podPush, logCallback)
                pushRet, pushOutput = commands.getstatusoutput(podPush)
                self.logOutput(pushRet, pushOutput, logCallback)

                if pushRet == 0:
                    wx.CallAfter(logCallback, "publish module %s successfully!!!\n" % module.name)
                    wx.CallAfter(completeCallback, True, module)
                else:
                    wx.CallAfter(logCallback, "push %s's podspec to repo failed!!!\n" % module.name)
                    wx.CallAfter(completeCallback, False, module)
            else:
                wx.CallAfter(logCallback, "copy module %s trunk to tags error!!!\n" % module.name)
                wx.CallAfter(completeCallback, False, module)
        else:
            wx.CallAfter(logCallback, "podspec repo not exist!!!\n")
            wx.CallAfter(completeCallback, False, module)

    def addSpecRepo(self, specRepo, logCallback, completeCallback):
        thread.start_new_thread(self.addSpecRepoWithShell, (specRepo, logCallback, completeCallback))

    def addSpecRepoWithShell(self, specRepo, logCallback, completeCallback):
        addSpecRepo = "/usr/local/bin/pod repo-svn add %s %s" % (specRepo.name, specRepo.remotePath)
        self.logCommand(addSpecRepo, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(addSpecRepo)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, specRepo)

    # Check pod command
    def checkPodCommand(self, logCallback, completeCallback):
        thread.start_new_thread(self.checkPodCommandWithShell, (logCallback, completeCallback))

    def checkPodCommandWithShell(self, logCallback, completeCallback):
        testPod = "cd $HOME; /usr/local/bin/pod --version"
        self.logCommand(testPod, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(testPod)
        self.logOutput(copyRet, copyOutput, logCallback)
        wx.CallAfter(completeCallback, True)

    # log caller
    def logCommand(self, command, callback):
        wx.CallAfter(callback, "%s\n" % command)

    def logOutput(self, stats, output, callback):
        wx.CallAfter(callback, "status : %s\n" % stats)
        if len(output) > 0:
            wx.CallAfter(callback, "%s\n" % output)