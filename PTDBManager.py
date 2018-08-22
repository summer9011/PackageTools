#!/usr/bin/env python
import os
import sqlite3
from PTModule import PTModule

class PTDBManager:
    __instance = None
    dbConnect = None
    dbCursor = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance=object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def openDB(self):
        if self.dbConnect == None:
            versionDB = os.path.join(os.getcwd(),"pt-1.db")
            existVersion = os.path.exists(versionDB)

            self.dbConnect = sqlite3.connect(versionDB)
            self.dbCursor = self.dbConnect.cursor()

            if existVersion == False:
                self.createModuleTable()
                self.dbConnect.commit()

    def createModuleTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_module" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "module_name" TEXT NOT NULL DEFAULT '',
        "local_path" TEXT NOT NULL DEFAULT '',
        "remote_path" TEXT NOT NULL DEFAULT '',
        "username" TEXT NOT NULL DEFAULT '',
        "password" TEXT NOT NULL DEFAULT ''
        );""")

    def getModuleList(self):
        self.openDB()
        self.dbCursor.execute("select * from pt_module;")

        moduleList = []
        for row in self.dbCursor:
            module = PTModule()
            module.id = row[0]
            module.moduleName = row[1]
            module.localPath = row[2]
            module.remotePath = row[3]
            module.username = row[4]
            module.password = row[5]
            moduleList.append(module)
        return moduleList

    def addNewModule(self, moduleList, callback):
        self.openDB()

        for module in moduleList:
            self.dbCursor.execute("""insert into "pt_module"(
            "module_name",
            "local_path",
            "remote_path",
            "username",
            "password"
            ) values ("%s","%s","%s","%s","%s");""" % (module.moduleName,
                                                               module.localPath,
                                                               module.remotePath,
                                                               module.username,
                                                               module.password))
            module.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(moduleList)