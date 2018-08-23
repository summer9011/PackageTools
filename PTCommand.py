#!/usr/bin/env python
import commands
import os
import thread
import wx
from PTDBManager import PTDBManager
from PTModule import PTModule

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
        os.chdir(module.localPath)

        svnCopyToTag = "svn copy %s/trunk %s/tags/%s -m \"release to %s\"" % (module.remotePath, module.remotePath, module.localVersion, module.localVersion)
        self.logCommand(svnCopyToTag, logCallback)
        copyRet, copyOutput = commands.getstatusoutput(svnCopyToTag)
        self.logOutput(copyRet, copyOutput, logCallback)

        if copyRet == 0:
            spec = PTDBManager().getSpec(module.specId)
            if spec != None:
                podPush = "pod repo-svn push %s %s.podspec" % (spec.specName, module.moduleName)
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

    def logCommand(self, command, callback):
        wx.CallAfter(callback, "\n=====  %s  =====\n" % command)

    def logOutput(self, stats, output, callback):
        wx.CallAfter(callback, "status : %s\n" % stats)
        if len(output) > 0:
            wx.CallAfter(callback, "%s\n" % output)