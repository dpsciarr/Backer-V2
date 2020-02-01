import json
import os.path

class ConfigurationManager:
	def __init__(self, application):
		self._application = application

		self._configurationOK = False
		self._configurationFilePresent = False
		self._configurationFileValidJSON = False

		self._runConfigurationOK = False
		self._runConfigurationFilePresent = False
		self._runConfigurationFileValidJSON = False

		self._configPath = os.path.join(application.configDirectory, "config.cfg")
		self._runConfigPath = os.path.join(application.configDirectory, "runcfg.cfg")

		self._configurationOK = self.checkConfiguration()
		self._runConfigurationOK = self.checkRunConfiguration()

	@property
	def application(self):
		return self._application

	@property
	def configPath(self):
		return self._configPath

	@property
	def runConfigPath(self):
		return self._runConfigPath
	

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
					json.load(f)
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
					json.load(f)
				self.runConfigurationFileValidJSON = True
				return True
			except ValueError as e:
				self.runConfigurationFileValidJSON = False
				return False
		else:
			return False