#!/usr/bin/env python
import wx
import wx.adv
import resources.PTResourcePath as Res
import tools.PTModuleHelper as Helper

class PTVersionDialog (wx.Dialog):
    versionText = None
    publishBtn = None
    loadingCtrl = None

    module = None
    callback = None

    def __init__(self, parent, module, callback):
        super(PTVersionDialog, self).__init__(parent, size=(500,160))

        self.module = module
        self.callback = callback

        sizer = wx.BoxSizer(wx.VERTICAL)

        tip = wx.StaticText(self, wx.ID_ANY, u"Enter version")
        sizer.Add((0,10))
        sizer.Add(tip, 0, wx.RIGHT|wx.LEFT, 30)
        sizer.Add((0, 20))

        gridSizer = wx.FlexGridSizer(1, 2, 10, 10)
        versionTip = wx.StaticText(self)
        versionTip.SetLabelText(u"Version :")
        gridSizer.Add(versionTip, 0)
        self.versionText = wx.TextCtrl(self, wx.ID_ANY, self.module.localVersion, style=wx.TE_LEFT, size=(200, 22))
        self.versionText.Bind(wx.EVT_TEXT, self.OnVersionTextChange)
        gridSizer.Add(self.versionText, 1, wx.EXPAND)
        gridSizer.AddGrowableCol(1)
        sizer.Add(gridSizer, 1, wx.EXPAND | wx.RIGHT|wx.LEFT, 30)

        self.publishBtn = wx.Button(self, wx.ID_ANY, u"Save")
        self.publishBtn.Bind(wx.EVT_BUTTON, self.OnChangeModule)

        if Helper.checkVersionBigger(self.module.localVersion, self.module.remoteVersion) == True:
            self.publishBtn.Enable(True)
        else:
            self.publishBtn.Enable(False)

        cancelBtn = wx.Button(self, wx.ID_ANY, u"Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelAction)

        animation = wx.adv.Animation(Res.getSmallLoadingGif())
        self.loadingCtrl = wx.adv.AnimationCtrl(self, wx.ID_ANY, animation, size=(22, 22))
        self.loadingCtrl.Hide()

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(cancelBtn)
        b.Add((10, 0))
        b.Add(self.publishBtn)
        b.Add((10, 0))
        b.Add(self.loadingCtrl)
        sizer.Add(b, 0, wx.ALIGN_RIGHT | wx.RIGHT, 30)
        sizer.Add((0, 20))

        self.SetSizer(sizer)

    def OnVersionTextChange(self, event):
        if len(self.versionText.GetValue()) > 0 and Helper.checkVersionBigger(self.versionText.GetValue(), self.module.remoteVersion) == True:
            self.publishBtn.Enable(True)
        else:
            self.publishBtn.Enable(False)

    def OnChangeModule(self, event):
        self.loadingCtrl.Show()
        self.loadingCtrl.Play()
        self.Layout()
        Helper.writeVersionToModule(self.module, self.versionText.GetValue(), self.OnWriteVersionCallback)

    def OnWriteVersionCallback(self, versionChanged):
        if versionChanged == True:
            self.module.localVersion = self.versionText.GetValue()
            self.EndModal(wx.ID_OK)
            self.callback(self.module)
        else:
            wx.MessageBox(u"Change verison failed.", u"Error", wx.OK | wx.ICON_INFORMATION)

        self.loadingCtrl.Stop()
        self.loadingCtrl.Hide()
        self.Layout()

    def OnCancelAction(self, event):
        self.loadingCtrl.Stop()
        self.loadingCtrl.Hide()
        self.Layout()
        self.EndModal(wx.ID_OK)