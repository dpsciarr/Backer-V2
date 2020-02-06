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

		self._srcDirectory = os.path.dirname(os.path.abspath(__file__))
		self._applicationDirectory = os.path.dirname(self._srcDirectory)
		self._databaseDirectory = os.path.join(self._srcDirectory, "_database")	
		self._configDirectory = os.path.join(self._srcDirectory, "cfg")

		# Initialize Application User Properties
		self._currentUser = ""
		self._currentUserID = -1
		self._isNewUser = False

		self._databaseOperator = DatabaseOperator(self)
		self._configurationManager = ConfigurationManager(self)
		self._objectModel = ObjectModel(self)

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

	'''
	initializeApplication()

	Called in application_gui __init__ method just before mainloop() is called
	
	Runs all initializing functions.
	'''
	def initializeApplication(self):
		self.outputManager.broadcast("Initializing application.")

		#Database Connectivity Check
		db_check = self.databaseOperator.checkConnection()

		#Config File Existence and Verification
		cfg_check = self.configurationManager.checkAllConfiguration()

		#Info Source Determination Check
		self.determineInfoSource(db_check, cfg_check)

		#Config File Congruency Check
		self.configurationManager.configFileSyncronized = self.sourceCongruencyCheck()

		#Drive Existence
		#Object Model Construction
		#Object Model Congruency Check

		# Setup Configuration Screen and Display Frame needed



	'''
	determineInfoSource(db_check, cfg_check)

	Determines the information source for Backer application.
	'''
	def determineInfoSource(self, db_check, cfg_check):
		self.outputManager.broadcast("Determining Information Source . . .")
		if db_check == False and cfg_check == False:
			self._informationSource = source.NO_SOURCE
		elif db_check == True and cfg_check == False:
			self._informationSource = source.SOURCE_DATABASE_NO_CFG
		elif db_check == False and cfg_check == True:
			self._informationSource = source.SOURCE_CONFIG_NO_DB
		else:
			self._informationSource = source.SOURCE_DATABASE

		self.outputManager.broadcast(f"   Information Source: {self._informationSource.name}")

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
			drvData = self.databaseOperator.queries.getDrivesDictFromDatabase(strUserID)
			drvList.append(drvData)
			device["drives"] = drvList

		print(userStruct)

		# 2. dump the database JSON file into a temp file

		# 3. Request the configuration file

		# 4. Request the newly created temp file based on the database

		# 5. compare the two files

		# 6. Output to Manager

		# 7. Return True/False

		return True


		











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