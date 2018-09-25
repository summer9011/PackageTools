#!/usr/bin/env python
import wx
import wx.lib.progressindicator as LibProgress
from tools.PTCommand import PTCommand
from tools.PTCommand import PTCommandPathConfig
from PTSVNCommitFrame import PTSVNCommitFrame

class PTPublishDialog (wx.Dialog):
    progressTip = None
    progress = None

    module = None
    logCallback = None
    chooseRepoCallback = None
    callback = None

    def __init__(self, parent, module, logCallback, chooseRepoCallback, callback):
        super(PTPublishDialog, self).__init__(parent, size=(500,160))

        self.module = module
        self.logCallback = logCallback
        self.chooseRepoCallback = chooseRepoCallback
        self.callback = callback

        sizer = wx.BoxSizer(wx.VERTICAL)

        gridSizer = wx.FlexGridSizer(2, 1, 10, 10)

        self.progressTip = wx.StaticText(self, wx.ID_ANY, u"Ready to publish")
        gridSizer.Add(self.progressTip, 0)

        self.progress = LibProgress.ProgressIndicator(self, style=LibProgress.PI_PULSEMODE)
        self.progress.SetValue(0, "0%")
        gridSizer.Add(self.progress, 1, wx.EXPAND)

        gridSizer.AddGrowableCol(0)
        sizer.Add(gridSizer, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 30)

        b = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(b, 0, wx.ALIGN_RIGHT | wx.RIGHT, 30)
        sizer.Add((0, 20))

        self.SetSizer(sizer)

        self.publishModule()

    def publishModule(self):
        self.progressTip.SetLabel(u"Svn updating...")
        self.progress.SetValue(15, "15%")
        PTCommand().svnUpdateModule(self.module, self.logCallback, self.OnSvnUpdateCallback)

    def OnSvnUpdateCallback(self, success, result):
        self.OnChooseSpecRepo()
        return
        if success == 0:
            self.progressTip.SetLabel(u"Svn check conflict...")
            self.progress.SetValue(30, "30%")
            PTCommand().svnCheckConflict(self.module, self.logCallback, self.OnSvnCheckConflictCallback)
        else:
            wx.MessageBox(u"Svn update failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnSvnCheckConflictCallback(self, success, result):
        if success == 0:
            files = result[0]
            conflictFiles = result[1]
            if len(conflictFiles) == 0:
                self.progressTip.SetLabel(u"Svn choose files to commit...")
                self.progress.SetValue(40, "40%")
                PTSVNCommitFrame(self, files, self.logCallback, self.OnSvnChooseCallback)
            else:
                wx.MessageBox(u"You have %d conflict files, please solve them.\nConflict files:\n%s" % (len(conflictFiles), conflictFiles), u"Error", wx.OK | wx.ICON_INFORMATION)
                self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox(u"Svn check conflict failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnSvnChooseCallback(self, cancelCommit, commitList = None, addList = None, deleteList = None, commitMsg = None):
        if cancelCommit == True:
            self.EndModal(wx.ID_OK)
        else:
            self.progressTip.SetLabel(u"Svn committing files...")
            self.progress.SetValue(60, "60%")
            PTCommand().svnCommitFiles(self.module, commitList, addList, deleteList, commitMsg, self.logCallback, self.OnCommitFilesCallback)

    def OnCommitFilesCallback(self, result):
        if result == True:
            self.progressTip.SetLabel(u"Svn tag module...")
            self.progress.SetValue(75, "75%")
            PTCommand().tagModule(self.module, self.logCallback, self.OnTagModuleCallback)
        else:
            wx.MessageBox(u"Svn committing files failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnTagModuleCallback(self, success, result):
        if success == 0:
            if len(self.module.sepcName) > 0:
                self.OnPublishModuleCallback(0, None)
            else:
                self.progressTip.SetLabel(u"Select module podspec repo...")
                self.progress.SetValue(85, "85%")
                if PTCommandPathConfig.podspecList == None:
                    PTCommand().getSpecRepoList(self.logCallback, self.OnGetSpecListCallback)
                else:
                    self.OnChooseSpecRepo()
        else:
            wx.MessageBox(u"Svn tag module failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnGetSpecListCallback(self, specRepoList):
        PTCommandPathConfig.podspecList = specRepoList
        self.OnChooseSpecRepo()

    def OnChooseSpecRepo(self):
        self.chooseRepoCallback(self.module)

    def OnPublishModuleCallback(self, success, result):
        if success == 0:
            self.progressTip.SetLabel(u"Publish module to pod...")
            self.progress.SetValue(90, "90%")
            PTCommand().publishModule(self.module, self.logCallback, self.OnPublishModuleCallback)
        else:
            print(result)