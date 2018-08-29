#!/usr/bin/env python

from PTDBManager import PTDBManager
from PTCommandPath import PTCommandPath

class PTCommandPathConfig:
    __instance = None
    commandPathData = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def GetCommands(self):
        if self.commandPathData == None:
            self.commandPathData = PTDBManager().getCommandPathDict()
        return self.commandPathData

    def command(self, name):
        return self.GetCommands().get(name, self.defaultCommand(name))

    def addCommand(self, commandPath):
        if commandPath.commandPath == None or len(commandPath.commandPath) == 0:
            commandPath.commandPath = self.defaultCommand(commandPath.name)
        result = PTDBManager().addCommandPath(commandPath)
        if result == True:
            self.GetCommands()[commandPath.name] = commandPath.commandPath

    def defaultCommand(self, name):
        command = ""
        if name == "svn":
            command = "svn"
        elif name == "pod":
            command = "/usr/local/bin/pod"
        return command