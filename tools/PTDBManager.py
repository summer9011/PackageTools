#!/usr/bin/env python
import os
import sqlite3
import PTOSPath
from models.PTModule import PTModule
from models.PTModule import PTModuleRepo
import PTModuleHelper

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
          "trunk_name" TEXT NOT NULL DEFAULT '',
          "spec_name" TEXT NOT NULL DEFAULT ''
        );""")

    # Module methods
    def getModuleList(self, logCallback):
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
            module.trunkName = row[5]
            module.sepcName = row[6]

            if row[3] > 0:
                module.repo = PTModuleRepo()
                module.repo.id = row[7]
                module.repo.url = row[8]
                module.repo.user = row[9]
                module.repo.pwd = row[10]

            module.localVersion = PTModuleHelper.getLocalVersion(module.path, logCallback)
            moduleList.append(module)

        return moduleList

    def addNewTrunkModule(self, module):
        self.openDB()

        self.dbCursor.execute("select * from pt_module where name=\"%s\" and trunk_id = 0" % module.name)
        trunkResult = self.dbCursor.fetchone()
        if trunkResult != None:
            self.dbCursor.execute("update pt_module set path=\"%s\", repo_id=%d where id=%d" % (module.path, module.repo.id, trunkResult[0]))
            module.id = trunkResult[0]
        else:
            self.dbCursor.execute("select * from pt_module where trunk_name=\"%s\" and trunk_id > 0" % module.name)
            branchResults = self.dbCursor.fetchall()

            self.dbCursor.execute("""insert into "pt_module"(
            "name",
            "path",
            "repo_id",
            "trunk_id",
            "trunk_name",
            "spec_name"
            ) values ("%s","%s",%d,%d,"%s","%s");""" % (module.name,
                                                   module.path,
                                                   module.repo.id,
                                                   module.trunkId,
                                                   module.trunkName,
                                                   module.sepcName))
            module.id = self.dbCursor.lastrowid

            if branchResults != None:
                for branch in branchResults:
                    self.dbCursor.execute("update pt_module set trunk_id=%d, trunk_name=\"%s\" where id=%d" % (module.id, module.name, branch[0]))

        self.dbConnect.commit()

    def addNewBranchModule(self, module):
        self.openDB()
        self.dbCursor.execute("select * from pt_module where name=\"%s\" and trunk_id = 0" % module.trunkName)
        trunkResult = self.dbCursor.fetchone()
        if trunkResult != None:
            self.dbCursor.execute("""insert into "pt_module"(
            "name",
            "path",
            "repo_id",
            "trunk_id",
            "trunk_name",
            "spec_name"
            ) values ("%s","%s",%d,%d,"%s","%s");""" % (module.name,
                                                        module.path,
                                                        module.repo.id,
                                                        trunkResult[0],
                                                        trunkResult[1],
                                                        module.sepcName))
            module.id = self.dbCursor.lastrowid
            module.trunkId = trunkResult[0]
            module.trunkName = trunkResult[1]
        else:
            self.dbCursor.execute("""insert into "pt_module"(
            "name",
            "path",
            "repo_id",
            "trunk_id",
            "trunk_name",
            "spec_name"
            ) values ("%s","%s",%d,%d,"%s","%s");""" % (module.name,
                                                        module.path,
                                                        module.repo.id,
                                                        "",
                                                        "",
                                                        module.sepcName))
            module.id = self.dbCursor.lastrowid

        self.dbConnect.commit()

    def deleteModule(self, module):
        self.openDB()
        self.deleteModuleBranches(module.id)
        self.dbCursor.execute("delete from pt_module where id = %d;" % module.id)
        self.dbConnect.commit()
        return True

    # Module repo methods
    def findModuleRepo(self, url):
        self.openDB()
        self.dbCursor.execute("select * from pt_module_repo where url = \"%s\";" % url)
        result = self.dbCursor.fetchone()
        repo = PTModuleRepo()
        repo.url = url
        if result != None:
            repo.id = result[0]
            repo.user = result[2]
            repo.pwd = result[3]
        return repo

    def updateModuleRepo(self, repo):
        self.openDB()
        if repo.id > 0:
            self.dbCursor.execute("update pt_module_repo set user=\"%s\", pwd=\"%s\" where id=%d;" % (repo.user, repo.pwd, repo.id))
        else:
            self.dbCursor.execute("""insert into pt_module_repo (
            "url", 
            "user", 
            "pwd") values ("%s", "%s", "%s")""" % (repo.url, repo.user, repo.pwd))
            repo.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        return True