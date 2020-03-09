import os
import sys
import enum
import tkinter as tk
from gui.application_gui import ApplicationWindow
from gui.login_gui import LoginWindow

srcDir = os.path.dirname(__file__)
dbDir = os.path.join(srcDir, "_database")
cfgDir = os.path.join(srcDir, "cfg")
modelDir = os.path.join(srcDir, "_models")
outputDir = os.path.join(srcDir, "gui\\_frames")

sys.path.append(dbDir)
sys.path.append(cfgDir)
sys.path.append(modelDir)
sys.path.append(outputDir)

from DatabaseOperator import DatabaseOperator
from ConfigurationManager import ConfigurationManager
from ObjectModel import ObjectModel
from OutputFrame import OutputFrame as broadcaster
from ObjectModel import Operation
from ConfigurationRunner import ConfigurationRunner

sys.path.remove(outputDir)
sys.path.remove(modelDir)
sys.path.remove(cfgDir)
sys.path.remove(dbDir)

class source(enum.Enum):
	NO_SOURCE = 0
	SOURCE_DATABASE = 1
	SOURCE_DATABASE_NO_CFG = 2
	SOURCE_CONFIG_NO_DB = 3





class Application:
	def __init__(self):
		print("Initializing Backer V2...")
		self._databaseName = "backer.db"
		self._informationSource = source.NO_SOURCE
		self._objectModelSyncronized = False
		self._driveExistence = False
		self._operationObject = Operation(self)

		self._srcDirectory = os.path.dirname(os.path.abspath(__file__))
		self._applicationDirectory = os.path.dirname(self._srcDirectory)
		self._databaseDirectory = os.path.join(self._srcDirectory, "_database")	
		self._configDirectory = os.path.join(self._srcDirectory, "cfg")
		self._toolsDirectory = os.path.join(self._srcDirectory, "tools")
		self._imageDirectory = os.path.join(self._srcDirectory, "img")

		# Initialize Application User Properties
		self._currentUser = ""
		self._currentUserID = -1
		self._isNewUser = False

		self._databaseOperator = DatabaseOperator(self)
		self._configurationManager = ConfigurationManager(self)
		self._objectModel = ObjectModel(self)

		# Initialize Configuration Runner
		self._configurationManager.configurationRunner = ConfigurationRunner(self._configurationManager)

		# Initialize the Output Stream
		self._outputManager = OutputManager(self)


	@property
	def srcDirectory(self):
		return self._srcDirectory
	
	@property
	def applicationDirectory(self):
		return self._applicationDirectory
	
	@property
	def databaseDirectory(self):
		return self._databaseDirectory

	@property
	def configDirectory(self):
		return self._configDirectory

	@property
	def toolsDirectory(self):
		return self._toolsDirectory

	@property
	def imageDirectory(self):
		return self._imageDirectory
	

	@property
	def informationSource(self):
		return self._informationSource

	@informationSource.setter
	def informationSource(self, value):
		self._informationSource = value

	@property
	def objectModelSyncronized(self):
		return self._objectModelSyncronized

	@objectModelSyncronized.setter
	def objectModelSyncronized(self, value):
		self._objectModelSyncronized = value
	
	@property
	def driveExistence(self):
		return self._driveExistence

	@driveExistence.setter
	def driveExistence(self, value):
		self._driveExistence = value

	@property
	def currentUser(self):
		return self._currentUser

	@currentUser.setter
	def currentUser(self, value):
		self._currentUser = value

	@property
	def currentUserID(self):
		return self._currentUserID

	@currentUserID.setter
	def currentUserID(self, value):
		self._currentUserID = value

	@property
	def isNewUser(self):
		return self._isNewUser

	@isNewUser.setter
	def isNewUser(self, value):
		self._isNewUser = value
	
	@property
	def databaseOperator(self):
		return self._databaseOperator

	@property
	def configurationManager(self):
		return self._configurationManager

	@property
	def objectModel(self):
		return self._objectModel

	@property
	def outputManager(self):
		return self._outputManager

	@property
	def operationObject(self):
		return self._operationObject
	

	'''
	initializeApplication()

	Called in application_gui __init__ method just before mainloop() is called
	
	Runs all initializing functions.
	'''
	def initializeApplication(self):
		self.outputManager.broadcast("Initializing application.")

		#Database Connectivity Check
		databaseConnectionCheck = self.databaseOperator.checkConnection()

		#Config File Existence and Verification
		configurationFilesCheck = self.configurationManager.checkAllConfiguration()

		#Info Source Determination Check
		self.informationSource = self.determineInfoSource(databaseConnectionCheck, configurationFilesCheck)

		#Config File Congruency Check
		self.configurationManager.configFileSyncronized = self.sourceCongruencyCheck()

		#Drive Existence
		self.driveExistence = self.driveExistenceCheck()

		#Object Model Construction
		self.objectModel.buildObjectModel(self._informationSource)

		#Object Model Congruency Check
		self.objectModelSyncronized = self.objectModelCongruencyCheck()

		#Setup Run Configuration
		self.configurationManager.setUpRunConfiguration(self.objectModel.currentUser)


	'''
	determineInfoSource(db_check, cfg_check)

	Determines the information source for Backer application.
	'''
	def determineInfoSource(self, db_check, cfg_check):
		self.outputManager.broadcast("Determining Information Source . . .")
		infoSource = ""
		if db_check == False and cfg_check == False:
			infoSource = source.NO_SOURCE
		elif db_check == True and cfg_check == False:
			infoSource = source.SOURCE_DATABASE_NO_CFG
		elif db_check == False and cfg_check == True:
			infoSource = source.SOURCE_CONFIG_NO_DB
		else:
			infoSource = source.SOURCE_DATABASE

		self.outputManager.broadcast(f"   Information Source: {infoSource.name}")
		return infoSource

	'''
	sourceCongruencyCheck()

	Determines whether the database and configuration file are equivalent representations.
	'''
	def sourceCongruencyCheck(self):
		self.outputManager.broadcast("Performing Congruency Check . . .")
		
		strUserID = str(self.currentUserID)

		# 1. build a JSON file based on the database
		userStruct = self.configurationManager.jsonOperator.buildBaseConfigurationStructure(strUserID)
		userData = self.databaseOperator.queries.getUserDictFromDatabase(strUserID)
		userStruct[strUserID] = userData

		#Get Device Data
		devDataHeaders, devData = self.databaseOperator.queries.getDevicesDictFromDatabase(strUserID)
		devList = []
		for result in devData:
			deStruct = {}
			for result2 in result:
				devStruct= dict(zip(devDataHeaders, result))
			devList.append(devStruct)
		userStruct[strUserID]["devices"] = devList
		
		#Get Drive Data
		for device in userStruct[strUserID]["devices"]:
			drvList = []
			device["drives"] = []
			devID = device["device_id"]
			drvData = self.databaseOperator.queries.getDrivesDictFromDatabase(devID)
			drvList.append(drvData)
			device["drives"] = drvList

		#Get Collection Data
		collDataHeaders, collData = self.databaseOperator.queries.getCollectionsDictFromDatabase(strUserID)
		collList = []
		for result in collData:
			collStruct = {}
			for result2 in result:
				collStruct = dict(zip(collDataHeaders, result))
			collList.append(collStruct)
		userStruct[strUserID]["collections"] = collList

		#Get Procedure
		for collection in userStruct[strUserID]["collections"]:
			collection["procedures"] = []
			collID = collection["collection_id"]
			procDataHeaders, procData = self.databaseOperator.queries.getProceduresDictFromDatabase(collID)

			procStruct = {}
			procList = []
			for result in procData:
				procStruct = dict(zip(procDataHeaders, result))
				procList.append(procStruct)
			collection["procedures"] = procList

		databaseData = userStruct
		with open(os.path.join(self.configDirectory, "temp.txt"), 'w') as dumpFile:
			self.configurationManager.jsonOperator.dump(databaseData, dumpFile)

		dbDataFromFile = ""
		with open(os.path.join(self.configDirectory, "temp.txt"), 'r') as dbFile:
			dbDataFromFile = self.configurationManager.jsonOperator.load(dbFile)

		configData = ""
		with open(os.path.join(self.configDirectory, "config.cfg"), 'r') as cfgFile:
			configData = self.configurationManager.jsonOperator.load(cfgFile)


		if configData == dbDataFromFile:
			self.outputManager.broadcast(f"   Configuration File syncronized with database for user '{self.currentUser}'.")
			return True
		else:
			self.outputManager.broadcast(f"   WARNING: Configuration file NOT syncronized with database.")
			return False

	'''
	driveExistenceCheck()

	Looks up the drives associated with the current user (source of this information varies based on informationSource variable)

	Checks to see if the configured drives actually exist.
	'''

	def driveExistenceCheck(self):
		self.outputManager.broadcast("Performing Drive Existence Check . . .")
		strUserID = str(self.currentUserID)

		if self._informationSource == source.SOURCE_DATABASE or self._informationSource == source.SOURCE_DATABASE_NO_CFG:
			d1, d2 = self.databaseOperator.queries.getDevicesDictFromDatabase(strUserID)
			dlist = []
			for result in d2:
				d = dict(zip(d1, result))
				dlist.append(d)

			for item in dlist:
				devID = item["device_id"]

				headers, data = self.databaseOperator.queries.getDriveLetterForDeviceFromDatabase(devID)

				try:
					drivesDict = dict(zip(headers, data[0][0]))
					for drive in drivesDict["drive_letter"]:
						string = str(drive) + ":\\\\"
						if os.path.isdir(string):
							self.outputManager.broadcast(f"   {string} Drive found.")
						else:
							self.outputManager.broadcast(f"   WARNING: {string} Drive Not Found. Connect drive before running backup.")
							return False
				except Exception as e:
					print(e)
					return False

		return True

	'''
	objectModelCongruencyCheck()

	Builds a JSON-like object from the current Object Model

	If the information source is based on the database, then a JSON-like object is built from the database configuration.
	Else, if the information source is based on the configurtion file, then a JSON-like object is built from the configuration file.

	If the two generated JSON-like objects are equal then this function returns True, else False
	'''
	def objectModelCongruencyCheck(self):
		self.outputManager.broadcast("Running Object Model Congruency Check . . .")
		OBJresult = self.configurationManager.jsonOperator.buildJSONFromObjectModel(self.objectModel.currentUser)
		
		try:
			jsonObjectModel = OBJresult[self.currentUserID]
		except Exception as e:
			jsonObjectModel = OBJresult[str(self.currentUserID)]

		if self._informationSource.name == "SOURCE_DATABASE" or self._informationSource.name == "SOURCE_DATABASE_NO_CFG":
			DBresult = self.configurationManager.jsonOperator.buildJSONFromDatabase(self.currentUserID, self.databaseOperator)

			try:
				jsonDatabaseModel = DBresult[self.currentUserID]
			except Exception as e:
				jsonDatabaseModel = DBresult[str(self.currentUserID)]

			if jsonObjectModel == jsonDatabaseModel:
				self.outputManager.broadcast("   SUCCESS: Object Model matches information in the Database Model.")
				return True
			else:
				self.outputManager.broadcast("   WARNING: Object Model does not match database. Generate new object model.")

		elif self._informationSource.name == "NO_SOURCE":
			self.outputManager.broadcast("   WARNING: No information source detected.")
			return False
		else:
			self.outputManager.broadcast("   WARNING: Object Model does not match configuration file.")
			self.outputManager.broadcast("     Generate new configuration file or new object model.")
			return False










################################################################################################
# OutputManager()
#
# Manages output of broadcasted messages to the user in the Output Frame on the Main Window, use
# self.broadcast(text).
################################################################################################
class OutputManager:
	def __init__(self, application):
		self._application = application
		self._textBox = None
		self._scrollbar = None

	@property
	def application(self):
		return self._application

	@property
	def textBox(self):
		return self._textBox

	@property
	def scrollbar(self):
		return self._scrollbar

	def generateTextBox(self, frameRef):
		self._textBox = tk.Text(frameRef, height=7, width=100)
		self._textBox.config(state = 'disabled')

		self._scrollbar = tk.Scrollbar(frameRef, command = self._textBox.yview)
		self._textBox['yscrollcommand'] = self._scrollbar.set

		return self._textBox

	def broadcast(self, text):
		self._textBox.config(state='normal')
		text = text + '\n'
		self._textBox.insert(tk.END, text)
		self._textBox.config(state='disabled')
		self._textBox.yview_moveto(1)











		

if __name__ == '__main__':
	#start application
	app = Application()

	#Log In Manager
	LoginWindow(app)

	if app.currentUserID != -1:
		app.objectModel.buildDatabaseModel()
		ApplicationWindow(app)