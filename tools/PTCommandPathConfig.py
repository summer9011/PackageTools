#!/usr/bin/env python

import PTOSPath
import json

class PTCommandPathConfig:
    __instance = None
    configDict = None
    podspecList = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def GetCommands(self):
        if self.configDict == None:
            f = open(PTOSPath.getConfigPath(), "r")
            jsonStr = f.read()
            f.close()
            self.configDict = json.loads(jsonStr)
        return self.configDict

    def command(self, name):
        return self.GetCommands().get(name, self.defaultCommand(name))

    def addCommand(self, name, path):
        self.GetCommands()
        commandPath = path
        if commandPath == None:
            commandPath = self.defaultCommand(name)
        self.GetCommands()[name] = commandPath
        jsonStr = json.dumps(self.GetCommands())

        f = open(PTOSPath.getConfigPath(), "w")
        f.write(jsonStr)
        f.close()

    def defaultCommand(self, name):
        command = ""
        if name == "svn":
            command = "svn"
        elif name == "pod":
            command = "/usr/local/bin/pod"
        return command