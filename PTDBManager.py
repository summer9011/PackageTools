#!/usr/bin/env python
import os
import sqlite3
from PTModule import PTModule
from PTSpec import PTSpec

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
                self.createSpecTable()
                self.dbConnect.commit()

    def createModuleTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_module" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "module_name" TEXT NOT NULL DEFAULT '',
        "local_path" TEXT NOT NULL DEFAULT '',
        "remote_path" TEXT NOT NULL DEFAULT '',
        "username" TEXT NOT NULL DEFAULT '',
        "password" TEXT NOT NULL DEFAULT '',
        "spec_id" INTEGER NOT NULL DEFAULT 0
        );""")

    def createSpecTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_spec" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "spec_name" TEXT NOT NULL DEFAULT '',
        "remote_path" TEXT NOT NULL DEFAULT ''
        );""")

    def getModuleList(self):
        self.openDB()
        self.dbCursor.execute("select * from pt_module;")
        results = self.dbCursor.fetchall()

        moduleList = []
        for row in results:
            module = PTModule()
            module.id = row[0]
            module.moduleName = row[1]
            module.localPath = row[2]
            module.remotePath = row[3]
            module.username = row[4]
            module.password = row[5]
            module.specId = row[6]
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
            "password",
            "spec_id"
            ) values ("%s","%s","%s","%s","%s","%s");""" % (module.moduleName,
                                                            module.localPath,
                                                            module.remotePath,
                                                            module.username,
                                                            module.password,
                                                            module.specId))
            module.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(moduleList)

    def deleteModule(self, module):
        self.openDB()
        self.dbCursor.execute("delete from pt_module where id = %d;", module.id)
        self.dbConnect.commit()
        return True

    def getSpec(self, specId):
        self.openDB()
        self.dbCursor.execute("select * form pt_spec where id = %d;" % specId)
        result = self.dbCursor.fetchone()
        spec = PTSpec()
        spec.id = result[0]
        spec.specName = result[1]
        spec.remotePath = result[2]
        return spec
