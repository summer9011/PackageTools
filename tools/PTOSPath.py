#!/usr/bin/env python

import os

def getUserRootPath():
    return os.path.expanduser('~')

def getDataRootPath():
    dir = os.path.join(getUserRootPath(), ".pt_tools")
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    return dir

def getDBPath():
    return os.path.join(getDataRootPath(), "pt_1.db")

def getConfigPath():
    configPath = os.path.join(getDataRootPath(), "pt_config.json")
    if os.path.exists(configPath) == False:
        f = open(configPath, "w")
        f.write("{}")
        f.close()
    return configPath