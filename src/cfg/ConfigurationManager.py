import os.path
from JsonOperator import JsonOperator as jsonOperator
from ConfigurationRunner import ConfigurationRunner

class ConfigurationManager:
	def __init__(self, application):
		self._application = application
		self._jsonOperator = jsonOperator(self)
		self._configurationRunner = None

		self._configurationOK = False
		self._configurationFilePresent = False
		self._configurationFileValidJSON = False
		self._configFileSyncronized = False

		self._runConfigurationOK = False
		self._runConfigurationFilePresent = False
		self._runConfigurationFileValidJSON = False
		self._runConfigurationDict = {}

		self._configPath = os.path.join(application.configDirectory, "config.cfg")
		self._runConfigPath = os.path.join(application.configDirectory, "runcfg.cfg")

		self._configurationOK = self.checkConfiguration()
		self._runConfigurationOK = self.checkRunConfiguration()

	@property
	def application(self):
		return self._application

	@property
	def jsonOperator(self):
		return self._jsonOperator
	
	@property
	def configPath(self):
		return self._configPath

	@property
	def runConfigPath(self):
		return self._runConfigPath

	@property
	def configurationRunner(self):
		return self._configurationRunner

	@configurationRunner.setter
	def configurationRunner(self, value):
		self._configurationRunner = value

	@property
	def configurationOK(self):
		return self._configurationOK

	@property
	def runConfigurationOK(self):
		return self._runConfigurationOK

	@property
	def configurationFilePresent(self):
		return self._configurationFilePresent

	@configurationFilePresent.setter
	def configurationFilePresent(self, value):
		self._configurationFilePresent = value

	@property
	def configurationFileValidJSON(self):
		return self._configurationFileValidJSON

	@configurationFileValidJSON.setter
	def configurationFileValidJSON(self, value):
		self._configurationFileValidJSON = value

	@property
	def configFileSyncronized(self):
		return self._configFileSyncronized

	@configFileSyncronized.setter
	def configFileSyncronized(self, value):
		self._configFileSyncronized = value

	@property
	def runConfigurationFilePresent(self):
		return self._runConfigurationFilePresent

	@runConfigurationFilePresent.setter
	def runConfigurationFilePresent(self, value):
		self._runConfigurationFilePresent = value

	@property
	def runConfigurationFileValidJSON(self):
		return self._runConfigurationFileValidJSON

	@runConfigurationFileValidJSON.setter
	def runConfigurationFileValidJSON(self, value):
		self._runConfigurationFileValidJSON = value

	@property
	def runConfigurationDict(self):
		return self._runConfigurationDict

	@runConfigurationDict.setter
	def runConfigurationDict(self, value):
		self._runConfigurationDict = value
	
	'''
	checkConfiguration()

	Checks whether the configuration file exists and whether it is valid JSON.
	Returns True only when both conditions are satisfied.
	'''
	def checkConfiguration(self):
		#check if the configuration file is there
		if self.application.databaseOperator.toolset.isFile(self._configPath):
			self.configurationFilePresent = True
		else:
			self.configurationFilePresent = False

		#check if the configuration file has been corrupted
		if self.configurationFilePresent == True:
			try:
				with open(self.configPath) as f:
					self.jsonOperator.load(f)
				self.configurationFileValidJSON = True
				return True
			except ValueError as e:
				self.configurationFileValidJSON = False
				return False
		else:
			return False

	'''
	checkRunConfiguration()

	Checks whether the run configuration file exists and whether it is valid JSON.
	Return True only when both conditions are satisfied.
	'''
	def checkRunConfiguration(self):
		#check if the run configuration file is there
		if self.application.databaseOperator.toolset.isFile(self._runConfigPath):
			self.runConfigurationFilePresent = True
		else:
			self.runConfigurationFilePresent = False

		#check if the run configuration file has been corrupted
		if self.runConfigurationFilePresent == True:
			try:
				with open(self.runConfigPath) as f:
					self.jsonOperator.load(f)
				self.runConfigurationFileValidJSON = True
				return True
			except ValueError as e:
				self.runConfigurationFileValidJSON = False
				return False
		else:
			return False

	'''
	checkTotalConfiguration()

	Checks the existence of all configuration files and validates their formatting.
	
	Return True if main configuration file exists and has valid formatting.
	'''
	def checkAllConfiguration(self):
		self.application.outputManager.broadcast("Checking Configuration Files . . .")

		#Check if configuration file exists
		if self.application.databaseOperator.toolset.isFile(self._configPath):
			self.configurationFilePresent = True
			self.application.outputManager.broadcast("   Main Configuration File: FOUND")
		else:
			self.configurationFilePresent = False
			self.application.outputManager.broadcast("   Main Configuration File: NOT FOUND")

		#Check if the run configuration file exists
		if self.application.databaseOperator.toolset.isFile(self._runConfigPath):
			self.runConfigurationFilePresent = True
			self.application.outputManager.broadcast("   Run Configuration File: FOUND")
		else:
			self.runConfigurationFilePresent = False
			self.application.outputManager.broadcast("   Run Configuration File: NOT FOUND")
		
		mainConfigValid = False
		runConfigValid = False
		if self.configurationFilePresent:
			if self.checkConfiguration():
				self.application.outputManager.broadcast("   Main Configuration File: VALIDATED")
			else:
				self.application.outputManager.broadcast("   Main Configuration File: NOT VALID")

		if self.runConfigurationFilePresent:
			if self.checkRunConfiguration():
				self.application.outputManager.broadcast("   Run Configuration File: VALIDATED")
			else:
				self.application.outputManager.broadcast("   Run Configuration File: NOT VALID")

		if self.configurationFilePresent and self.checkConfiguration():
			return True
		else:
			return False

	'''
	initRunConfig()

	Iterates through all procedures and updates the runConfigurationDict dictionary.
	'''
	def setUpRunConfiguration(self, userObject):
		collectionObjects = userObject.collections
		collectionObjectItems = [(item[0],item[1]) for item in collectionObjects.items()]
		for collection in collectionObjectItems:
			procedureObjects = collection[1].procedures
			procedureObjectItems = [(item[0],item[1]) for item in procedureObjects.items()]
			for procedure in procedureObjectItems:
				self.runConfigurationDict[procedure[0]] = procedure[1].selectedForRunConfig

	'''
	updateRunConfig(procID, runCfgStatus)
	
	Updates a single procedure, identified by procID, in the run configuration dict with runCfgStatus
	'''
	def updateRunConfig(self, procID, runCfgStatus):
		self.runConfigurationDict[procID] = runCfgStatus