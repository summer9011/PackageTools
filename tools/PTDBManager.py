#!/usr/bin/env python
import os
import sqlite3
import PTOSPath
from models.PTModule import PTModule
from models.PTModule import PTModuleRepo

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
            dbPath = PTOSPath.getDBPath()
            existVersion = os.path.exists(dbPath)

            self.dbConnect = sqlite3.connect(dbPath)
            self.dbCursor = self.dbConnect.cursor()

            if existVersion == False:
                self.createModuleRepo()
                self.createModuleTable()
                self.dbConnect.commit()

    def createModuleRepo(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_module_repo" (
          "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          "url" TEXT NOT NULL DEFAULT '',
          "user" TEXT NOT NULL DEFAULT '',
          "pwd" TEXT NOT NULL DEFAULT ''
        );""")

    def createModuleTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_module" (
          "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          "name" TEXT NOT NULL DEFAULT '',
          "path" TEXT NOT NULL DEFAULT '',
          "repo_id" INTEGER NOT NULL DEFAULT 0,
          "trunk_id" INTEGER NOT NULL DEFAULT 0,
          "spec_name" TEXT NOT NULL DEFAULT ''
        );""")

    # Module methods
    def getModuleList(self):
        self.openDB()
        self.dbCursor.execute("select * from pt_module as a left outer join pt_module_repo as b on a.repo_id=b.id;")
        results = self.dbCursor.fetchall()

        moduleList = []
        for row in results:
            module = PTModule()
            module.id = row[0]
            module.name = row[1]
            module.path = row[2]
            module.trunkId = row[4]
            module.sepcName = row[5]

            if row[3] > 0:
                module.repo = PTModuleRepo()
                module.repo.id = row[6]
                module.repo.url = row[7]
                module.repo.user = row[8]
                module.repo.pwd = row[9]
            moduleList.append(module)

        return moduleList

    def addNewModule(self, moduleList, callback):
        self.openDB()
        for module in moduleList:
            self.dbCursor.execute("""insert into "pt_module"(
            "name",
            "local_path",
            "code_repo_id",
            "spec_repo_id"
            ) values ("%s","%s","%s","%s");""" % (module.name,
                                                  module.localPath,
                                                  module.codeRepoId,
                                                  module.specRepoId))
            module.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(moduleList)

    def deleteModule(self, module):
        self.openDB()
        self.deleteModuleBranches(module.id)
        self.dbCursor.execute("delete from pt_module where id = %d;" % module.id)
        self.dbConnect.commit()
        return True