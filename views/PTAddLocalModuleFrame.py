#!/usr/bin/env python
import wx
import os
import wx.adv
import resources.PTResourcePath as Res
from tools import PTModuleHelper
from PTFileDrop import PTFileDrop
from models.PTModule import PTModule
from PTRepoDialog import PTRepoDialog
from PTSVNCheckDialog import PTSVNCheckDialog
from tools.PTCommand import PTCommand

class PTAddLocalModuleFrame (wx.Frame):
    tipText = None
    loadingCtrl = None
    fileDrop = None

    logCallback = None
    callback = None
    closeCallback = None

    def __init__(self, parent, logCalllback, callback, closeCallback):
        super(PTAddLocalModuleFrame, self).__init__(parent, wx.ID_ANY, u"Add local module", size=(600, 300), style= wx.CLOSE_BOX | wx.SYSTEM_MENU)

        self.logCallback = logCalllback
        self.callback = callback
        self.closeCallback = closeCallback

        self.SetupUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CentreOnScreen()
        self.Show(True)

    def OnClose(self, event):
        self.Destroy()
        self.closeCallback()

    def SetupUI(self):
        self.fileDrop = PTFileDrop(self.OnDropFileCallback, self.OnEnterDropCallback)
        self.SetDropTarget(self.fileDrop)

        image = wx.Image(Res.getAddPng()).ConvertToBitmap()
        backImage = wx.StaticBitmap(self, wx.ID_ANY, image)
        self.tipText = wx.StaticText(self, wx.ID_ANY, u"Drag module here.")

        animation = wx.adv.Animation(Res.getLoadingGif())
        self.loadingCtrl = wx.adv.AnimationCtrl(self, wx.ID_ANY, animation, size=animation.GetSize())
        self.loadingCtrl.Hide()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((0, 70))
        sizer.Add(backImage, 0, wx.ALIGN_CENTER)
        sizer.Add((0, 10))
        sizer.Add(self.tipText, 0, wx.ALIGN_CENTER)
        sizer.Add((0, 10))
        sizer.Add(self.loadingCtrl, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)

    def ShowLoading(self, show):
        if show == True:
            self.loadingCtrl.Show()
            self.loadingCtrl.Play()
        else:
            self.loadingCtrl.Stop()
            self.loadingCtrl.Hide()

    def OnEnterDropCallback(self, isEnter):
        if isEnter == True:
            self.tipText.SetLabel(u"Drop it!!!")
        else:
            self.tipText.SetLabel(u"Drag module here.")
        self.Layout()

    def OnDropFileCallback(self, filepath):
        if self.loadingCtrl.IsPlaying() == True:
            self.OnEnterDropCallback(False)
            return

        self.ShowLoading(True)
        self.OnEnterDropCallback(False)
        PTCommand().svnCheckPath(filepath, self.logCallback, self.OnCheckSvnEnable)

    def OnCheckSvnEnable(self, success, filepath, result):
        if result.startswith(u"svn:") == False:
            self.OnSVNCheckCallback(success, filepath)
        else:
            if 'is not a working copy' in result:
                self.ShowLoading(False)
                notWorkingCopy = True
            else:
                notWorkingCopy = False
            dialog = PTSVNCheckDialog(self, filepath, notWorkingCopy, result, self.logCallback, self.OnSVNCheckCallback)
            dialog.ShowWindowModal()

    def OnSVNCheckCallback(self, success, filepath):
        if success == 0:
            PTModuleHelper.FindModuleInfo(filepath, self.logCallback, self.FindModuleInfoCallback)
        else:
            self.ShowLoading(False)

    def FindModuleInfoCallback(self, trunkName, path, version, url, user):
        if trunkName == None:
            self.ShowLoading(False)
            wx.MessageBox(u"Can't find module info.", u"Error", wx.OK | wx.ICON_INFORMATION)
        else:
            m = PTModule()
            m.name = os.path.basename(path)
            m.trunkName = trunkName
            m.path = path
            m.localVersion = version

            urlArr = url.split("/")
            urlArr.pop()
            dlg = PTRepoDialog(self, m, "/".join(urlArr), user, self.OnRepoDialogCallback)
            dlg.ShowWindowModal()

    def OnRepoDialogCallback(self, module, isTrunk):
        self.ShowLoading(False)
        if module != None:
            self.callback(module, isTrunk)