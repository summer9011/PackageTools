#!/usr/bin/env python
import wx
import wx.dataview
from PTModule import PTModule

class PTModuleModel (wx.dataview.DataViewModel):
    modules = []

    def __init__(self):
        super(PTModuleModel, self).__init__()
        self.CreateDemoData()

    def CreateDemoData(self):
        for i in range(0,10):
            iStr = "%d" % i
            pt = PTModule()
            pt.id = iStr
            pt.name = iStr
            pt.localVersion = iStr
            pt.remoteVersion = iStr
            self.modules.append(pt)

    def FindModule(self, moduleId):
        foundModule = None
        for module in self.modules:
            if module.id == moduleId:
                foundModule = module
        return foundModule

    def IsContainer(self, item):
        if item.ID == None:
            return True
        else:
            return self.FindModule(item.ID) != None

    def GetParent(self, item):
        print "GetParent"
        print item.ID
        return None

    def GetChildren(self, item, children):
        print "GetChildren1"
        print item
        if item.ID == None:
            children.append(wx.dataview.DataViewItem(0))
            children.append(wx.dataview.DataViewItem(1))
            print "GetChildren2"
            print children
            return 2
        else:
            # children.append(wx.dataview.DataViewItem(1))
            children.append(wx.dataview.DataViewItem(2))
            children.append(wx.dataview.DataViewItem(3))
            return 2

    def GetColumnCount(self):
        return 3

    def GetColumnType(self, col):
        print "GetColumnType"
        return ""

    def GetValue(self, item, col):
        print "GetValue"
        print item.ID
        print col

        if item.ID == None:
            return "root"
        else:
            module = self.FindModule(item.ID)
            if not module:
                return ""
            else:
                if col == 0:
                    return module.name
                elif col == 1:
                    return module.localVersion
                elif col == 2:
                    return module.remoteVersion

    def SetValue(self, variant, item, col):
        print "SetValue"
        return True
