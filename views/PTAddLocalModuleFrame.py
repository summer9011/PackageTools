#!/usr/bin/env python
import wx
import os
from tools import PTModuleHelper
from PTFileDrop import PTFileDrop
from models.PTModule import PTModule
from PTRepoDialog import PTRepoDialog
from PTSVNCheckDialog import PTSVNCheckDialog
from tools.PTCommand import PTCommand

class PTAddLocalModuleFrame (wx.Frame):
    dropBox = None
    fileDrop = None

    logCallback = None
    callback = None

    def __init__(self, parent, logCalllback, callback):
        super(PTAddLocalModuleFrame, self).__init__(parent, wx.ID_ANY, u"Add local module", size=(600, 400))

        self.logCallback = logCalllback
        self.callback = callback

        self.SetupUI()
        self.CentreOnScreen()
        self.Show(True)

    def SetupUI(self):
        self.fileDrop = PTFileDrop(self.OnDropFileCallback)
        self.dropBox = wx.StaticBox(self, label=u"*Drag local module here.")
        self.dropBox.SetDropTarget(self.fileDrop)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dropBox, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(sizer)

    def OnDropFileCallback(self, filepath):
        PTCommand().svnCheckPath(filepath, self.logCallback, self.OnCheckSvnEnable)

    def OnCheckSvnEnable(self, success, filepath, result):
        if result.startswith(u"svn:") == False:
            self.OnSVNCheckCallback(success, filepath)
        else:
            if 'is not a working copy' in result:
                notWorkingCopy = True
            else:
                notWorkingCopy = False
            dialog = PTSVNCheckDialog(self, filepath, notWorkingCopy, result, self.logCallback, self.OnSVNCheckCallback)
            dialog.ShowWindowModal()

    def OnSVNCheckCallback(self, success, filepath):
        if success == 0:
            PTModuleHelper.FindModuleInfo(filepath, self.logCallback, self.FindModuleInfoCallback)

    def FindModuleInfoCallback(self, trunkName, path, version, url, user):
        if trunkName == None:
            wx.MessageBox(u"Can't find module info.", u"Error", wx.OK | wx.ICON_INFORMATION)
        else:
            m = PTModule()
            m.name = os.path.basename(path)
            m.trunkName = trunkName
            m.path = path
            m.localVersion = version

            urlArr = url.split("/")
            urlArr.pop()
            dlg = PTRepoDialog(self, m, "/".join(urlArr), user, self.callback)
            dlg.ShowWindowModal()