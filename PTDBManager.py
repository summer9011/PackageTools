#!/usr/bin/env python
import os
import sqlite3
from PTModule import PTModule
from PTSpecRepo import PTSpecRepo

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
        "name" TEXT NOT NULL DEFAULT '',
        "local_path" TEXT NOT NULL DEFAULT '',
        "remote_path" TEXT NOT NULL DEFAULT '',
        "username" TEXT NOT NULL DEFAULT '',
        "password" TEXT NOT NULL DEFAULT '',
        "spec_repo_id" INTEGER NOT NULL DEFAULT 0
        );""")

    def createSpecTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_spec_repo" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" TEXT NOT NULL DEFAULT '',
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
            module.name = row[1]
            module.localPath = row[2]
            module.remotePath = row[3]
            module.username = row[4]
            module.password = row[5]
            module.specRepoId = row[6]
            moduleList.append(module)
        return moduleList

    def addNewModule(self, moduleList, callback):
        self.openDB()
        for module in moduleList:
            self.dbCursor.execute("""insert into "pt_module"(
            "name",
            "local_path",
            "remote_path",
            "username",
            "password",
            "spec_repo_id"
            ) values ("%s","%s","%s","%s","%s","%s");""" % (module.name,
                                                            module.localPath,
                                                            module.remotePath,
                                                            module.username,
                                                            module.password,
                                                            module.specRepoId))
            module.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(moduleList)

    def deleteModule(self, module):
        self.openDB()
        self.dbCursor.execute("delete from pt_module where id = %d;" % module.id)
        self.dbConnect.commit()
        return True

    def getSpecRepo(self, specRepoId):
        self.openDB()
        self.dbCursor.execute("select * from pt_spec_repo where id = %d;" % specRepoId)
        result = self.dbCursor.fetchone()
        if result != None:
            specRepo = PTSpecRepo()
            specRepo.id = specRepoId
            specRepo.name = result[1]
            specRepo.remotePath = result[2]
            return specRepo
        return None

    def getSpecRepoList(self):
        self.openDB()
        self.dbCursor.execute("select * from pt_spec_repo;")
        results = self.dbCursor.fetchall()

        specRepoList = []
        for row in results:
            specRepo = PTSpecRepo()
            specRepo.id = row[0]
            specRepo.name = row[1]
            specRepo.remotePath = row[2]
            specRepoList.append(specRepo)
        return specRepoList

    def addNewSpecRepo(self, specRepo, callback):
        self.openDB()
        self.dbCursor.execute("""insert into "pt_spec_repo"(
        "name",
        "remote_path"
        ) values ("%s","%s");""" % (specRepo.name, specRepo.remotePath))
        specRepo.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(specRepo)

    def deleteSpecRepo(self, specRepo):
        self.openDB()
        self.dbCursor.execute("delete from pt_spec_repo where id = %d;" % specRepo.id)
        self.dbConnect.commit()
        return True