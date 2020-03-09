import os
import sys

srcDir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
toolsDir = os.path.join(srcDir, "tools")

sys.path.append(toolsDir)

import backerOps as bops

sys.path.remove(toolsDir)

class ConfigurationRunner():
	def __init__(self, configurationManager):
		self._configurationManager = configurationManager
		self._application = configurationManager.application
		self._objectModel = self._application.objectModel


	@property
	def configurationManager(self):
		return self._configurationManager

	@property
	def application(self):
		return self._application
	
	
	def run(self):
		collectionItems = self.determineCollectionItems()
		operationObject = self.application.operationObject
		outputManager = self.application.outputManager

		runConfigDict = self.configurationManager.runConfigurationDict
		runItems = [(item[0], item[1]) for item in runConfigDict.items()]

		for item in runItems:
			procID = item[0]
			runStatus = item[1]

			if runStatus:
				for collection in collectionItems:
					if collection[1].procedureExistsInCollection(int(procID)):
						procObj = collection[1].getProcedure(int(procID))
						procName = procObj.procedureName
						procSource = procObj.sourcePath
						procDest = procObj.destinationPath
						procOpCode = procObj.operationID
						procOpString = operationObject.getOperationByNum(procOpCode)
						errorStatus = False

						outputManager.broadcast("________________________________________________________________________")
						outputManager.broadcast(f"   RUNNING PROCEDURE")
						outputManager.broadcast(f"       NAME: {procName}")
						outputManager.broadcast(f"       ID: {procID}")
						outputManager.broadcast(f"       Source Path: {procSource}")
						outputManager.broadcast(f"       Dest. Path: {procDest}")
						outputManager.broadcast(f"       Operation: {procOpString}")
						
						if int(procOpCode) == 0: #File Copy New (Basic)
							src, dest, errors = bops.fileCopyNew(procSource, procDest, token = 'BASIC')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 1: #Single File Copy New (Basic)
							src, dest, errors = bops.singleFileCopyNew(procSource, procDest, token='BASIC')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 2: #File Copy Overwrite
							src, dest, errors = bops.fileCopyOverwrite(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 3: #Single File Copy Overwrite
							src, dest, errors = bops.singleFileCopyOverwrite(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 4: #File Migrate New
							src, dest, errors = bops.fileMigrateNew(procSource, procDest, token = 'BASIC')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 5: #Single File Migrate New
							src, dest, errors = bops.singleFileMigrateNew(procSource, procDest, token = 'BASIC')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 6: #File Migrate Overwrite
							src, dest, errors = bops.fileMigrateOverwrite(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 7: #Single File Migrate Overwrite
							src, dest, errors = bops.singleFileMigrateOverwrite(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 8: #Folder Copy New
							src, dest, errors = bops.folderCopyNew(procSource, procDest, token='BASIC')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 9: #Single Folder Copy New
							src, dest, errors = bops.singleFolderCopyNew(procSource, procDest, token='BASIC')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 10: #Folder Copy Overwrite
							src, dest, errors = bops.folderCopyOverwrite(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 11:  #Single Folder Copy Overwrite
							src, dest, errors = bops.singleFolderCopyOverwrite(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 12: #Directory Sync Overwrite
							src, dest, errors = bops.directorySyncOverwrite(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 13: #Full Directory Sync
							src, dest, errors = bops.fullDirectorySync(procSource, procDest)
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 14: #File Copy New (Date)
							src, dest, errors = bops.fileCopyNew(procSource, procDest, token = 'DATE')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 15: #File Copy New (Date-Time)
							src, dest, errors = bops.fileCopyNew(procSource, procDest, token = 'DATE-TIME')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 16: #File Copy New (Time-Stamp)
							src, dest, errors = bops.fileCopyNew(procSource, procDest, token = 'TIME-STAMP')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 17: #Single File Copy New (Date)
							src, dest, errors = bops.singleFileCopyNew(procSource, procDest, token='DATE')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 18: #Single File Copy New (Date-Time)
							src, dest, errors = bops.singleFileCopyNew(procSource, procDest, token='DATE-TIME')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 19: #Single File Copy New (Time-Stamp)
							src, dest, errors = bops.singleFileCopyNew(procSource, procDest, token='TIME-STAMP')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 20: #Single File Copy New (Revision)
							src, dest, errors = bops.singleFileCopyNew(procSource, procDest, token='REV')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 21: #File Migrate New (Date)
							src, dest, errors = bops.fileMigrateNew(procSource, procDest, token = 'DATE')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 22: #File Migrate New (DATE-TIME)
							src, dest, errors = bops.fileMigrateNew(procSource, procDest, token = 'DATE-TIME')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 23: #File Migrate New (TIME-STAMP)
							src, dest, errors = bops.fileMigrateNew(procSource, procDest, token = 'TIME-STAMP')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 24: #Single File Migrate New (Date)
							src, dest, errors = bops.singleFileMigrateNew(procSource, procDest, token = 'DATE')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 25: #Single File Migrate New (Date-Time)
							src, dest, errors = bops.singleFileMigrateNew(procSource, procDest, token = 'DATE-TIME')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 26: #Single File Migrate New (TIME-STAMP)
							src, dest, errors = bops.singleFileMigrateNew(procSource, procDest, token = 'TIME-STAMP')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 27: #Single File Migrate New (REV)
							src, dest, errors = bops.singleFileMigrateNew(procSource, procDest, token = 'REV')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 28: #Folder Copy New (Date)
							src, dest, errors = bops.folderCopyNew(procSource, procDest, token='DATE')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 29: #Folder Copy New (Date-Time)
							src, dest, errors = bops.folderCopyNew(procSource, procDest, token='DATE-TIME')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 30: #Folder Copy New (Time-Stamp)
							src, dest, errors = bops.folderCopyNew(procSource, procDest, token='TIME-STAMP')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 31: #Single Folder Copy New (Date)
							src, dest, errors = bops.singleFolderCopyNew(procSource, procDest, token='DATE')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 32: #Single Folder Copy New (Date-Time)
							src, dest, errors = bops.singleFolderCopyNew(procSource, procDest, token='DATE-TIME')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 33: #Single Folder Copy New (TIME-STAMP)
							src, dest, errors = bops.singleFolderCopyNew(procSource, procDest, token='TIME-STAMP')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						elif int(procOpCode) == 34: #Single Folder Copy New (REV)
							src, dest, errors = bops.singleFolderCopyNew(procSource, procDest, token='REV')
							if len(errors) > 0:
								errorStatus = True
								for err in errors:
									outputManager.broadcast(f"       Error: {err}")
						else:
							print("")

						if errorStatus == False:
							outputManager.broadcast("       SUCCESS")
						else:
							outputManager.broadcast("       UNSUCCESSFUL")
							errorStatus = False

						outputManager.broadcast("________________________________________________________________________")

	

	'''
	determineCollectionItems()

	Returns a dict of the current user's collection objects.
	'''
	def determineCollectionItems(self):
		userObject = self._objectModel.currentUser
		collectionObjects = userObject.collections
		return [(item[0], item[1]) for item in collectionObjects.items()]