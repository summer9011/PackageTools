#!/usr/bin/env python
import wx
import wx.dataview

class PTModuleTree:
    def __init__(self):
        self.name = None
        self.val = None

        self.parent = None
        self.children = []

    def AddChild(self, moduleTree):
        self.children.append(moduleTree)
        moduleTree.parent = self

    def RemoveChild(self, moduleTree):
        self.children.remove(moduleTree)
        moduleTree.parent = None

    @classmethod
    def Root(cls):
        return PTModuleTree()


class PTModuleViewModel (wx.dataview.PyDataViewModel):
    def __init__(self, moduleTree):
        super(PTModuleViewModel, self).__init__()
        self.moduleTree = moduleTree

    def GetChildren(self, item, children):
        if item.ID == None:
            moduleTree = self.moduleTree
        else:
            moduleTree = self.ItemToObject(item)

        for tree in moduleTree.children:
            children.append(self.ObjectToItem(tree))
        return len(moduleTree.children)

    def GetValue(self, item, col):
        tree = self.ItemToObject(item)
        if col == 0:
            return tree.name
        elif col == 1:
            if tree.val != None:
                return tree.val.localVersion
        elif col == 2:
            if tree.val != None:
                return tree.val.remoteVersion
        return ""

    def HasContainerColumns(self, item):
        tree = self.ItemToObject(item)
        return len(tree.children) > 0

    def IsContainer(self, item):
        tree = self.ItemToObject(item)
        return len(tree.children) > 0

    def IsEnabled(self, item, col):
        tree = self.ItemToObject(item)
        return len(tree.children) == 0

    def ItemAdded(self, parent, item):
        print "ItemAdded parent:"+parent+" item:"+item
        return False

    def ItemChanged(self, item):
        print "ItemChanged item:"+item
        return False

    def ItemDeleted(self, parent, item):
        print "ItemDeleted parent:"+parent+" item:"+item
        return False

    def ItemsAdded(self, parent, items):
        print "ItemDeleted parent:"+parent+" items:"+items
        return False

    def ItemsChanged(self, items):
        print "ItemsChanged items:"+items
        return False

    def ItemsDeleted(self, parent, items):
        print "ItemsDeleted parent:"+parent+" items:"+items
        return False