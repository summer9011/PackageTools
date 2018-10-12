#!/usr/bin/env python
import wx
import wx.lib.progressindicator as LibProgress
import wx.adv
import resources.PTResourcePath as Res
from tools.PTCommand import PTCommand
from tools.PTCommand import PTCommandPathConfig
from PTSVNCommitFrame import PTSVNCommitFrame

class PTPublishDialog (wx.Dialog):
    progressTip = None
    progress = None
    loadingCtrl = None

    successImage = None
    successText = None
    successBtn = None

    h1Box = None

    v1Box = None
    v2Box = None

    module = None
    logCallback = None
    chooseRepoCallback = None
    callback = None

    def __init__(self, parent, module, logCallback, chooseRepoCallback, callback):
        super(PTPublishDialog, self).__init__(parent, size=(500,180))

        self.module = module
        self.logCallback = logCallback
        self.chooseRepoCallback = chooseRepoCallback
        self.callback = callback

        self.progressTip = wx.StaticText(self, wx.ID_ANY, u"Ready to publish")

        self.progress = LibProgress.ProgressIndicator(self, style=LibProgress.PI_PULSEMODE)
        self.progress.SetValue(0, "0%")

        animation = wx.adv.Animation(Res.getSmallLoadingGif())
        self.loadingCtrl = wx.adv.AnimationCtrl(self, wx.ID_ANY, animation, size=(22, 22))
        self.loadingCtrl.Play()

        self.h1Box = wx.BoxSizer(wx.HORIZONTAL)
        self.h1Box.Add(self.progress, 1, wx.EXPAND|wx.RIGHT, 10)
        self.h1Box.Add(self.loadingCtrl, 0, wx.RIGHT, 20)

        image = wx.Image(Res.getSuccessPng()).ConvertToBitmap()
        self.successImage = wx.StaticBitmap(self, wx.ID_ANY, image)
        self.successText = wx.StaticText(self, wx.ID_ANY, u"Publish module successfully!!!")
        self.successBtn = wx.Button(self, wx.ID_ANY, u"Done")
        self.successBtn.Bind(wx.EVT_BUTTON, self.OnSuccessPublish)

        self.v1Box = wx.BoxSizer(wx.VERTICAL)
        self.v1Box.Add((0, 10))
        self.v1Box.Add(self.progressTip, 0, wx.LEFT|wx.TOP, 20)
        self.v1Box.Add((0, 10))
        self.v1Box.Add(self.h1Box, 0, wx.EXPAND|wx.LEFT, 20)

        self.v2Box = wx.BoxSizer(wx.VERTICAL)
        self.v2Box.Add(self.successImage, 0, wx.CENTER|wx.TOP, 20)
        self.v2Box.Add((0, 2))
        self.v2Box.Add(self.successText, 0, wx.CENTER|wx.TOP, 10)
        self.v2Box.Add((0, 10))
        self.v2Box.Add(self.successBtn, 0, wx.CENTER|wx.TOP, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.v1Box, 1, wx.EXPAND)
        sizer.Add(self.v2Box, 1, wx.EXPAND)
        sizer.Hide(self.v2Box)
        self.SetSizer(sizer)

        self.publishModule()

    def publishModule(self):
        self.UpdateProgress(15, u"Svn updating...")
        PTCommand().svnUpdateModule(self.module, self.logCallback, self.OnSvnUpdateCallback)

    def OnSvnUpdateCallback(self, success, result):
        if success == 0:
            self.UpdateProgress(30, u"Svn check conflict...")
            PTCommand().svnCheckConflict(self.module, self.logCallback, self.OnSvnCheckConflictCallback)
        else:
            wx.MessageBox(u"Svn update failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnSvnCheckConflictCallback(self, success, result):
        if success == 0:
            files = result[0]
            conflictFiles = result[1]
            if len(conflictFiles) == 0:
                self.UpdateProgress(40, u"Svn choose files to commit...")
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
            self.UpdateProgress(60, u"Svn committing files...")
            PTCommand().svnCommitFiles(self.module, commitList, addList, deleteList, commitMsg, self.logCallback, self.OnCommitFilesCallback)

    def OnCommitFilesCallback(self, result):
        if result == True:
            self.UpdateProgress(70, u"Svn tag module...")
            PTCommand().tagModule(self.module, self.logCallback, self.OnTagModuleCallback)
        else:
            wx.MessageBox(u"Svn committing files failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnTagModuleCallback(self, success, result):
        if success == 0:
            if len(self.module.sepcName) > 0:
                self.ContinueToPublish()
            else:
                if PTCommandPathConfig.podspecList == None:
                    self.UpdateProgress(75, u"Fetch podspec repo list...")
                    PTCommand().getSpecRepoList(self.logCallback, self.OnGetSpecListCallback)
                else:
                    self.UpdateProgress(85, u"Select module podspec repo...")
                    self.OnChooseSpecRepo()
        else:
            wx.MessageBox(u"Svn tag module failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnGetSpecListCallback(self, specRepoList):
        self.UpdateProgress(85, u"Select module podspec repo...")
        PTCommandPathConfig.podspecList = specRepoList
        self.OnChooseSpecRepo()

    def OnChooseSpecRepo(self):
        self.chooseRepoCallback(self.module)

    def ContinueToPublish(self):
        self.UpdateProgress(90, u"Publish module to pod repo...")
        PTCommand().publishModule(self.module, self.logCallback, self.OnPublishModuleCallback)

    def OnPublishModuleCallback(self, success, result):
        if success == True:
            self.UpdateProgress(100, u"Publish module successfully!!!")
            sizer = self.GetSizer()
            sizer.Hide(self.v1Box)
            sizer.Show(self.v2Box)
            image = wx.Image(Res.getSuccessPng()).ConvertToBitmap()
            self.successImage.SetBitmap(image)
            self.Layout()

            self.module.remoteVersion = self.module.localVersion
            self.callback(self.module)
        else:
            wx.MessageBox(u"Publish module to pod repo failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

    def OnSuccessPublish(self, event):
        self.EndModal(wx.ID_OK)

    def UpdateProgress(self, percent, text):
        self.progressTip.SetLabel(text)
        self.progress.SetValue(percent, u"%d%%" % percent)