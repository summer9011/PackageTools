#!/usr/bin/env python
import wx
import wx.adv
import resources.PTResourcePath as Res
from tools.PTCommand import PTCommand
from tools.PTCommandPathConfig import PTCommandPathConfig

class PTEnvironmentFrame (wx.Frame):
    svnCommandText = None
    setSvnCommandBtn = None
    checkSvnCommandBtn = None
    checkSvnLoadingCtrl = None

    podCommandText = None
    setPodCommandBtn = None
    checkPodCommandBtn = None
    checkPodLoadingCtrl = None

    logCallback = None
    closeCallback = None

    def __init__(self, parent, logCallback, closeCallback):
        super(PTEnvironmentFrame, self).__init__(parent, wx.ID_ANY, u"Commands", size=(600, 400), style= wx.CLOSE_BOX | wx.SYSTEM_MENU)

        self.logCallback = logCallback
        self.closeCallback = closeCallback

        self.SetupUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CentreOnScreen()
        self.Show(True)

    def OnClose(self, event):
        self.Destroy()
        self.closeCallback()

    def SetupUI(self):
        animation = wx.adv.Animation(Res.getSmallLoadingGif())

        self.svnCommandText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(280, 22))
        self.svnCommandText.SetValue(PTCommandPathConfig().command("svn"))
        self.setSvnCommandBtn = wx.Button(self, wx.ID_ANY, u"Set `svn` command")
        self.setSvnCommandBtn.Bind(wx.EVT_BUTTON, self.OnSetSvnCommand)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.svnCommandText, 0, wx.RIGHT, 10)
        hBox1.Add(self.setSvnCommandBtn, 0, wx.RIGHT, 10)

        self.checkSvnCommandBtn = wx.Button(self, wx.ID_ANY, u"Check `svn` Command")
        self.checkSvnCommandBtn.Bind(wx.EVT_BUTTON, self.OnCheckSvnCommand)
        self.checkSvnLoadingCtrl = wx.adv.AnimationCtrl(self, wx.ID_ANY, animation, size=(22, 22))
        self.checkSvnLoadingCtrl.Hide()
        hBox11 = wx.BoxSizer(wx.HORIZONTAL)
        hBox11.Add(self.checkSvnCommandBtn, 0, wx.RIGHT, 10)
        hBox11.Add(self.checkSvnLoadingCtrl, 0)

        self.podCommandText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(280, 22))
        self.podCommandText.SetValue(PTCommandPathConfig().command("pod"))
        self.setPodCommandBtn = wx.Button(self, wx.ID_ANY, u"Set `pod` command")
        self.setPodCommandBtn.Bind(wx.EVT_BUTTON, self.OnSetPodCommand)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(self.podCommandText, 0, wx.RIGHT, 10)
        hBox2.Add(self.setPodCommandBtn, 0, wx.RIGHT, 10)

        self.checkPodCommandBtn = wx.Button(self, wx.ID_ANY, u"Check `pod` Command")
        self.checkPodCommandBtn.Bind(wx.EVT_BUTTON, self.OnCheckPodCommand)
        self.checkPodLoadingCtrl = wx.adv.AnimationCtrl(self, wx.ID_ANY, animation, size=(22, 22))
        self.checkPodLoadingCtrl.Hide()
        hBox21 = wx.BoxSizer(wx.HORIZONTAL)
        hBox21.Add(self.checkPodCommandBtn, 0, wx.RIGHT, 10)
        hBox21.Add(self.checkPodLoadingCtrl, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hBox11, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(hBox1, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(hBox21, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(hBox2, 0, wx.LEFT|wx.TOP, 10)

        self.SetSizer(sizer)

    # Check svn command
    def OnSetSvnCommand(self, event):
        self.setSvnCommandBtn.Enable(False)
        self.setSvnCommandBtn.SetLabelText(u"Setting")

        PTCommandPathConfig().addCommand("svn", self.svnCommandText.GetValue())

        self.setSvnCommandBtn.Enable(True)
        self.setSvnCommandBtn.SetLabelText(u"Set `svn` command")

    def OnCheckSvnCommand(self, event):
        self.checkSvnLoadingCtrl.Show()
        self.checkSvnLoadingCtrl.Play()
        self.checkSvnCommandBtn.Enable(False)
        self.checkSvnCommandBtn.SetLabelText(u"Checking")
        self.Layout()

        PTCommand().checkSvnCommand(self.logCallback, self.OnCheckSvnCommandCallback)

    def OnCheckSvnCommandCallback(self, result):
        self.checkSvnCommandBtn.Enable(True)
        self.checkSvnLoadingCtrl.Stop()
        self.checkSvnLoadingCtrl.Hide()
        if result == True:
            self.checkSvnCommandBtn.SetLabelText(u"Check `svn` Command")
        else:
            self.checkSvnCommandBtn.SetLabelText(u"Recheck")
        self.Layout()

    # Check pod command
    def OnSetPodCommand(self, event):
        self.setPodCommandBtn.Enable(False)
        self.setPodCommandBtn.SetLabelText(u"Setting")

        PTCommandPathConfig().addCommand("pod", self.podCommandText.GetValue())

        self.setPodCommandBtn.Enable(True)
        self.setPodCommandBtn.SetLabelText(u"Set `pod` command")

    def OnCheckPodCommand(self, event):
        self.checkPodLoadingCtrl.Show()
        self.checkPodLoadingCtrl.Play()
        self.checkPodCommandBtn.Enable(False)
        self.checkPodCommandBtn.SetLabelText(u"Checking")
        self.Layout()

        PTCommand().checkPodCommand(self.logCallback, self.OnCheckPodCommandCallback)

    def OnCheckPodCommandCallback(self, result):
        self.checkPodCommandBtn.Enable(True)
        self.checkPodLoadingCtrl.Stop()
        self.checkPodLoadingCtrl.Hide()
        if result == True:
            self.checkPodCommandBtn.SetLabelText(u"Check `pod` Command")
        else:
            self.checkPodCommandBtn.SetLabelText(u"Recheck")
        self.Layout()