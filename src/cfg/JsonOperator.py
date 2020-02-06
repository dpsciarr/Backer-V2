import json as json

class JsonOperator:
	def __init__(self, configurationManager):
		self._configurationManager = configurationManager

	@property
	def configurationManager(self):
		return self._configurationManager
	

	def load(self, file):
		return json.load(file)


	'''
	buildBaseConfigurationStructure()

	Builds and returns a JSON template used for the Backer application.
	Essentially, a JSON dict with no stored information.
	'''
	def buildBaseConfigurationStructure(self, userID = -1):
		struct = {}
		userStruct = {"user_id": userID, "user_name":"", "passcode":""}

		userStruct["devices"] = []
		userStruct["collections"] = []

		struct[userID] = {}
		struct[userID].update(userStruct)

		return struct


