#!/usr/bin/env python
import os
import sqlite3
import json
from PTModule import PTModule
from PTSpecRepo import PTSpecRepo
from PTCodeRepo import PTCodeRepo
from PTModuleBranch import PTModuleBranch
from PTCommandPath import PTCommandPath

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
                self.createCodeTable()
                self.createModuleBranchesTable()
                self.createCommandPathTable()
                self.dbConnect.commit()

    # Add module table
    def createModuleTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_module" (
          "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          "name" TEXT NOT NULL DEFAULT '',
          "local_path" TEXT NOT NULL DEFAULT '',
          "code_repo_id" INTEGER NOT NULL DEFAULT 0,
          "spec_repo_id" INTEGER NOT NULL DEFAULT 0
        );""")

    # Add spec repo table
    def createSpecTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_spec_repo" (
          "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          "name" TEXT NOT NULL DEFAULT '',
          "remote_path" TEXT NOT NULL DEFAULT ''
        );""")

    # Add code repo table
    def createCodeTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_code_repo" (
          "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          "name" TEXT NOT NULL DEFAULT '',
          "remote_path" TEXT NOT NULL DEFAULT '',
          "username" TEXT NOT NULL DEFAULT '',
          "password" TEXT NOT NULL DEFAULT '',
          "type" INTEGER NOT NULL DEFAULT 0
        );""")

    # Add module branches table
    def createModuleBranchesTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_module_branch" (
          "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          "remote_name" TEXT NOT NULL DEFAULT '',
          "local_path" TEXT NOT NULL DEFAULT '',
          "module_id" INTEGER NOT NULL DEFAULT 0
        );""")

    # Add command path config table
    def createCommandPathTable(self):
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS "pt_command_path" (
          "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          "name" TEXT NOT NULL DEFAULT '',
          "command_path" TEXT NOT NULL DEFAULT ''
        );""")

    # Import & export
    def importData(self, filePath, callback):
        self.openDB()

        f = open(filePath, 'r')
        jsonStr = f.read()
        jsonObj = json.loads(jsonStr)

        moduleData = jsonObj["pt_module"]
        specRepoData = jsonObj["pt_spec_repo"]
        codeRepoData = jsonObj["pt_code_repo"]

        self.dbCursor.execute("delete from pt_module;")
        self.dbCursor.execute("delete from pt_spec_repo;")
        self.dbCursor.execute("delete from pt_code_repo;")
        self.dbConnect.commit()

        self.dbCursor.execute("update sqlite_sequence set seq = 0 where name = \"pt_module\";")
        self.dbCursor.execute("update sqlite_sequence set seq = 0 where name = \"pt_spec_repo\";")
        self.dbCursor.execute("update sqlite_sequence set seq = 0 where name = \"pt_code_repo\";")
        self.dbConnect.commit()

        for dict in moduleData:
            names = []
            vals = []
            for key in dict:
                names.append(key)
                vals.append("\"%s\"" % dict[key])

            nameStr = ",".join(str(name) for name in names)
            valStr = ",".join(str(val) for val in vals)
            sql = """insert into "pt_module"(%s) values (%s);""" % (nameStr, valStr)
            self.dbCursor.execute(sql)
            self.dbConnect.commit()

        for dict in specRepoData:
            names = []
            vals = []
            for key in dict:
                names.append(key)
                vals.append("\"%s\"" % dict[key])

            nameStr = ",".join(str(name) for name in names)
            valStr = ",".join(str(val) for val in vals)
            sql = """insert into "pt_spec_repo"(%s) values (%s);""" % (nameStr, valStr)
            self.dbCursor.execute(sql)
            self.dbConnect.commit()

        for dict in codeRepoData:
            names = []
            vals = []
            for key in dict:
                names.append(key)
                vals.append("\"%s\"" % dict[key])

            nameStr = ",".join(str(name) for name in names)
            valStr = ",".join(str(val) for val in vals)
            sql = """insert into "pt_code_repo"(%s) values (%s);""" % (nameStr, valStr)
            self.dbCursor.execute(sql)
            self.dbConnect.commit()

        callback(True)

    def exportData(self, filePath, callback):
        self.openDB()

        moduleData = []
        self.dbCursor.execute("select * from {}".format("pt_module"))
        moduleDesc = self.dbCursor.description
        self.dbCursor.execute("select * from pt_module;")
        moduleResult = self.dbCursor.fetchall()

        specRepoData = []
        self.dbCursor.execute("select * from {}".format("pt_spec_repo"))
        specRepoDesc = self.dbCursor.description
        self.dbCursor.execute("select * from pt_spec_repo;")
        specRepoResult = self.dbCursor.fetchall()

        codeRepoData = []
        self.dbCursor.execute("select * from {}".format("pt_code_repo"))
        codeRepoDesc = self.dbCursor.description
        self.dbCursor.execute("select * from pt_code_repo;")
        codeRepoResult = self.dbCursor.fetchall()

        for row in moduleResult:
            dict = {}
            for i in range(0, 5):
                dict[moduleDesc[i][0]] = row[i]
            moduleData.append(dict)

        for row in specRepoResult:
            dict = {}
            for i in range(0, 3):
                dict[specRepoDesc[i][0]] = row[i]
            specRepoData.append(dict)

        for row in codeRepoResult:
            dict = {}
            for i in range(0, 6):
                dict[codeRepoDesc[i][0]] = row[i]
            codeRepoData.append(dict)

        jsonObj = {"pt_module":moduleData, "pt_spec_repo":specRepoData, "pt_code_repo":codeRepoData}
        jsonStr = json.dumps(jsonObj)

        f = open(filePath, 'w')
        f.write(jsonStr)
        f.close()

        callback(True)

    # Module methods
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
            module.codeRepoId = row[3]
            module.specRepoId = row[4]
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

    # Spec repo methods
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
        ) values ("%s","%s");""" % (specRepo.name,
                                    specRepo.remotePath))
        specRepo.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(specRepo)

    def deleteSpecRepo(self, specRepo):
        self.openDB()
        self.dbCursor.execute("delete from pt_spec_repo where id = %d;" % specRepo.id)
        self.dbConnect.commit()
        return True

    # Code repo methods
    def getCodeRepo(self, codeRepoId):
        self.openDB()
        self.dbCursor.execute("select * from pt_code_repo where id = %d;" % codeRepoId)
        result = self.dbCursor.fetchone()
        if result != None:
            codeRepo = PTCodeRepo()
            codeRepo.id = codeRepoId
            codeRepo.name = result[1]
            codeRepo.remotePath = result[2]
            codeRepo.username = result[3]
            codeRepo.password = result[4]
            codeRepo.type = result[5]
            return codeRepo
        return None

    def getCodeRepoList(self):
        self.openDB()
        self.dbCursor.execute("select * from pt_code_repo;")
        results = self.dbCursor.fetchall()

        codeRepoList = []
        for row in results:
            codeRepo = PTCodeRepo()
            codeRepo.id = row[0]
            codeRepo.name = row[1]
            codeRepo.remotePath = row[2]
            codeRepo.username = row[3]
            codeRepo.password = row[4]
            codeRepo.type = row[5]
            codeRepoList.append(codeRepo)
        return codeRepoList

    def addNewCodeRepo(self, codeRepo, callback):
        self.openDB()
        self.dbCursor.execute("""insert into "pt_code_repo"(
        "name",
        "remote_path",
        "username",
        "password",
        "type"
        ) values ("%s","%s","%s","%s","%s");""" % (codeRepo.name,
                                                   codeRepo.remotePath,
                                                   codeRepo.username,
                                                   codeRepo.password,
                                                   codeRepo.type))
        codeRepo.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(codeRepo)

    def deleteCodeRepo(self, codeRepo):
        self.openDB()
        self.dbCursor.execute("delete from pt_code_repo where id = %d;" % codeRepo.id)
        self.dbConnect.commit()
        return True

    # Module branches methods
    def getModuleBranches(self, moduleId):
        self.openDB()
        self.dbCursor.execute("select * from pt_module_branch where module_id = %d;" % moduleId)
        results = self.dbCursor.fetchall()

        branchList = []
        for row in results:
            moduleBranch = PTModuleBranch()
            moduleBranch.id = row[0]
            moduleBranch.remoteName = row[1]
            moduleBranch.localPath = row[2]
            moduleBranch.moduleId = row[3]
            branchList.append(moduleBranch)
        return branchList

    def addNewModuleBranch(self, moduleBranch, callback):
        self.openDB()
        self.dbCursor.execute("""insert into "pt_module_branch"(
        "remote_name",
        "local_path",
        "module_id"
        ) values ("%s","%s","%s");""" % (moduleBranch.remoteName,
                                         moduleBranch.localPath,
                                         moduleBranch.moduleId))
        moduleBranch.id = self.dbCursor.lastrowid
        self.dbConnect.commit()
        callback(moduleBranch)

    def deleteModuleBranch(self, moduleBranch):
        self.openDB()
        self.dbCursor.execute("delete from pt_module_branch where id = %d;" % moduleBranch.id)
        self.dbConnect.commit()
        return True

    def deleteModuleBranches(self, moduleId):
        self.openDB()
        self.dbCursor.execute("delete from pt_module_branch where module_id = %d;" % moduleId)
        self.dbConnect.commit()
        return True

    # Command path config
    def getCommandPathDict(self):
        self.openDB()
        self.dbCursor.execute("select * from pt_command_path;")
        results = self.dbCursor.fetchall()

        commandPathDict = {}
        for row in results:
            commandPath = PTCommandPath()
            commandPath.id = row[0]
            commandPath.name = row[1]
            commandPath.commandPath = row[2]
            commandPathDict[commandPath.name] = commandPath.commandPath
        return commandPathDict

    def addCommandPath(self, commandPath):
        self.openDB()
        self.dbCursor.execute("select * from pt_command_path where name = \"%s\"" % commandPath.name)
        result = self.dbCursor.fetchone()
        if result == None:
            self.dbCursor.execute("""insert into "pt_command_path"(
                    "name",
                    "command_path"
                    ) values ("%s","%s");""" % (commandPath.name,
                                                commandPath.commandPath))
            commandPath.id = self.dbCursor.lastrowid
        else:
            self.dbCursor.execute("update pt_command_path set command_path = \"%s\" where name = \"%s\"" % (commandPath.commandPath, commandPath.name))
        self.dbConnect.commit()
        return True