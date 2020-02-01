import os
import sys
from gui.application_gui import ApplicationWindow
from gui.login_gui import LoginWindow

srcDir = os.path.dirname(__file__)
dbDir = os.path.join(srcDir, "_database")
cfgDir = os.path.join(srcDir, "cfg")
modelDir = os.path.join(srcDir, "_models")
sys.path.append(dbDir)
sys.path.append(cfgDir)
sys.path.append(modelDir)

from DatabaseOperator import DatabaseOperator
from ConfigurationManager import ConfigurationManager
from ObjectModel import ObjectModel

sys.path.remove(modelDir)
sys.path.remove(cfgDir)
sys.path.remove(dbDir)

class Application:
	def __init__(self):
		print("Initializing Backer V2...")
		self._databaseName = "backer.db"

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
	def outputManager(self):
		return self._outputManager

	@outputManager.setter
	def outputManager(self, value):
		self.outputManager = value
	





class OutputManager:
	def __init__(self, application):
		self._application = application

	@property
	def application(self):
		return self._application

	def printToOutput(self, text):
		print(text)
	




if __name__ == '__main__':
	#Initialize application
	app = Application()

	#Log In Manager
	LoginWindow(app)

	if app.currentUserID != -1:
		app.outputManager.printToOutput("Hello World")
		ApplicationWindow(app)