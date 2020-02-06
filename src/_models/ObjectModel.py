import json

class ObjectModel:
	def __init__(self, application):
		self._currentUser = None
		self._application = application

	@property
	def currentUser(self):
		return self._currentUser

	@currentUser.setter
	def currentUser(self, value):
		self._currentUser = value

	@property
	def application(self):
		return self._application
	
	

	def buildDatabaseModel(self):
		userID = self.application.currentUserID
		userName = self.application.currentUser
		userPasscode = ""

		userData = ""
		try:
			self.application.databaseOperator.openDatabase()
			sql = f"""SELECT passcode FROM users WHERE user_id = '{userID}'"""
			self.application.databaseOperator.setCursor()
			self.application.databaseOperator.execute(sql)
			userData = self.application.databaseOperator.fetchall()
			self.application.databaseOperator.closeDatabase()
		except Exception as e:
			print(e)

		if len(userData) > 0:
				userPasscode = userData[0][0]
				self.currentUser = User(userID, userName, userPasscode)



		if userData != "":
			deviceData = ""
			collectionData = ""

			try:
				self.application.databaseOperator.openDatabase()
				sql = f"""SELECT * FROM devices WHERE user_id = '{userID}'"""
				self.application.databaseOperator.setCursor()
				self.application.databaseOperator.execute(sql)
				deviceData = self.application.databaseOperator.fetchall()
				self.application.databaseOperator.closeDatabase()
			except Exception as e:
				print(e)

			if len(deviceData) > 0:
				for device in deviceData:
					deviceObject = Device(identifier = device[0], name = device[1], user = device[2])

					driveData = ""
					try:
						self.application.databaseOperator.openDatabase()
						sql = f"""SELECT * FROM drives WHERE device_id = '{device[0]}'"""
						self.application.databaseOperator.setCursor()
						self.application.databaseOperator.execute(sql)
						driveData = self.application.databaseOperator.fetchall()
						self.application.databaseOperator.closeDatabase()
					except Exception as e:
						print(e)

					if len(driveData) > 0:
						for drive in driveData:
							driveObject = Drive(identifier=drive[0], driveLetter=drive[1], driveName=drive[2], deviceID=drive[3])
							deviceObject.addDrive(driveObject)

					self.currentUser.addDevice(deviceObject)

			try:
				self.application.databaseOperator.openDatabase()
				sql = f"""SELECT * FROM collections WHERE user_id = '{userID}'"""
				self.application.databaseOperator.setCursor()
				self.application.databaseOperator.execute(sql)
				collectionData = self.application.databaseOperator.fetchall()
				self.application.databaseOperator.closeDatabase()
			except Exception as e:
				print(e)

			if len(collectionData) > 0:
				for collection in collectionData:
					collectionObject = Collection(identifier = collection[0], collectionName = collection[1], userID = collection[2])

					procedureData = ""
					try:
						self.application.databaseOperator.openDatabase()
						sql = f"""SELECT * FROM procedures WHERE collection_id = '{collection[0]}'"""
						self.application.databaseOperator.setCursor()
						self.application.databaseOperator.execute(sql)
						procedureData = self.application.databaseOperator.fetchall()
						self.application.databaseOperator.closeDatabase()
					except Exception as e:
						print(e)

					for procedure in procedureData:
						procedureObject = Procedure(identifier = procedure[0], procName = procedure[1], source = procedure[2], destination = procedure[3], collectionID = procedure[4], operationID = procedure[5])
						collectionObject.addProcedure(procedureObject)

					self.currentUser.addCollection(collection)


	def buildConfigurationModel(self):
		print("Building model from configuration file...")
		userID = self.application.currentUserID
		userName = self.application.currentUser
		userPasscode = ""

		with open(application.configurationManager.configPath, 'r') as configFile:
			configJSON = json.load(configFile)

		userConfiguration = configJSON[userID]
		
		userPasscode = userConfiguration["passcode"]

		self.currentUser = User(userID, userName, userPasscode)

		for device in userConfiguration["devices"]:
			deviceID = device["device_id"]
			deviceName = device["device_name"]
			deviceUser = device["user_id"]

			deviceObject = Device(deviceID, deviceName, deviceUser)

			drives = device["drives"]
			for drive in drives:
				drive_id = drive["drive_id"]
				drive_letter = drive["drive_letter"]
				drive_name = drive["drive_name"]
				device_id = drive["drive_id"]

				driveObject = Drive(identifier = drive_id, driveLetter = drive_letter, driveName = drive_name, deviceID = device_id)
				deviceObject.addDrive(driveObject)


			self.currentUser.addDevice(deviceObject)


		for collection in userConfiguration["collections"]:
			collectionID = collection["collection_id"]
			collectionName = collection["collection_name"]
			userID = collection["user_id"]

			collectionObject = Collection(identifier=collectionID, collectionName = collectionName, userID = userID)

			procedures = collection["procedures"]
			for procedure in procedures:
				procedureID = procedure["procedure_id"]
				procedureName = procedure["procedure_name"]
				procedureSource = procedure["procedure_source"]
				procedureDestination = procedure["procedure_destination"]
				collectionID = procedure["collection_id"]
				procedureOp = procedure["operation_id"]

				procedureObject = Procedure(identifier=procedureID, procName = procedureName, source = procedureSource, destination = procedureDestination, collectionID = collection_id, operationID = operationID)
				collectionObject.addProcedure(procedureObject)


			self.currentUser.addCollection(collectionObject)















class User:
	def __init__(self, identifier, name, passcode):
		self._userID = identifier
		self._username = name
		self._passcode = passcode
		self._devices = {}
		self._collections = {}

	@property
	def userID(self):
		return self._userID

	@property
	def passcode(self):
		return self._passcode

	@passcode.setter
	def passcode(self, value):
		self._passcode = value

	@property
	def collections(self):
		return self._collections
	
	@property
	def devices(self):
		return self._devices

	
	def addCollection(self, collection):
		self.collections[collection.collectionID] = collection
	
	def addDevice(self, device):
		self.devices[device.deviceID] = device

	def getCollection(self, collID):
		if len(self.collections) > 0 and self.collections[collID] is not None:
			return self.collections[collID]
		else:
			return None

	def getDevice(self, devID):
		if len(self.devices) > 0 and self.devices[devID] is not None:
			return self.devices[devID]
		else:
			return None

	
	def removeCollection(self, collID):
		return self.collections.pop(collID, None)
	
	def removeDevice(self, devID):
		return self.devices.pop(devID, None)













class Device:
	def __init__(self, identifier, name, user):
		self._deviceID = identifier
		self._deviceName = name
		self._deviceUser = user
		self._drives = {}

	@property
	def deviceID(self):
		return self._deviceID

	@property
	def deviceName(self):
		return self._deviceName
	

	@property
	def deviceUser(self):
		return self._deviceUser

	@deviceUser.setter
	def deviceUser(self, value):
		self._deviceUser = value

	@property
	def drives(self):
		return self._drives

	def addDrive(self, drive):
		self.drives[drive.driveID] = drive

	def getDrive(self, driveID):
		if len(self.drives) > 0 and self.drives[driveID] is not None:
			return self.drives[driveID]
		else:
			return None

	def removeDrive(self, driveID):
		return self.drives.pop(driveID, None)















class Drive:
	def __init__(self, identifier, driveLetter, driveName, deviceID):
		self._driveID = identifier
		self._driveLetter = driveLetter
		self._driveName = driveName
		self._deviceID = deviceID

	@property
	def driveLetter(self):
		return self._driveLetter

	@property
	def deviceID(self):
		return self._deviceID

	@property
	def driveName(self):
		return self._driveName
	
	@property
	def driveID(self):
		return self._driveID
	
	@driveLetter.setter
	def driveLetter(self, value):
		self._driveLetter = value

	@deviceID.setter
	def deviceID(self, value):
		self._deviceID = value
	













	
class Collection:
	def __init__(self, identifier, collectionName, userID):
		self._collectionID = identifier
		self._collectionName = collectionName
		self._userID = userID
		self._procedures = {}

	@property
	def userID(self):
		return self._userID

	@userID.setter
	def userID(self, value):
		self._userID = value

	@property
	def collectionID(self):
		return self._collectionID

	@property
	def collectionName(self):
		return self._collectionName
	
	
	@property
	def procedures(self):
		return self._procedures
	
	def addProcedure(self, procedure):
		self._procedures[procedure.procedureID] = procedure

	def getProcedure(self, procID):
		if len(self._procedures) > 0 and self._procedures[procID] is not None:
			return self._procedures[procID]
		else:
			return None
	
	def removeProcedure(self, procID):
		return self._procedures.pop(procID, None)

	def procedureExistsInCollection(self, procID):
		procedureObjects = [(item[0], item[1]) for item in self._procedures.items()]
		if len(procedureObjects) > 0:
			for procedure in procedureObjects:
				if procedure[0] == procID:
					return True
		return False

	def selectProceduresForRunConfig(self):
		procObjects = [(item[0], item[1]) for item in self._procedures.items()]
		if len(procObjects) > 0:
			for procedure in procedureObjects:
				procedure[1].selectForRunConfig()

		return procedureObjects

	def deselectProceduresForRunConfig(self):
		procObjects = [(item[0], item[1]) for item in self._procedures.items()]
		if len(procObjects) > 0:
			for procedure in procedureObjects:
				procedure[1].deselectForRunConfig()

		return procedureObjects















class Procedure:
	def __init__(self, identifier, procName, source, destination, collectionID, operationID):
		self._procedureID = identifier
		self._procedureName = procName
		self._sourcePath = source
		self._destinationPath = destination
		self._collectionID = collectionID
		self._operationID, operationID

		self._selectedForRunConfig = False

	@property
	def procedureID(self):
		return self._procedureID

	@property
	def sourcePath(self):
		return self._sourcePath

	@sourcePath.setter
	def sourcePath(self, value):
		self._sourcePath = value

	@property
	def destinationPath(self):
		return self._destinationPath

	@destinationPath.setter
	def destinationPath(self, value):
		self._destinationPath = value
	
	@property
	def collectionID(self):
		return self._collectionID

	@property
	def operationID(self):
		return self._operationID
	
	@collectionID.setter
	def collectionID(self, value):
		self._collectionID = value

	@operationID.setter
	def operationID(self, value):
		self._operationID = value

	def selectForRunConfig(self):
		self._selectedForRunConfig = True
		return self.selectedForRunConfig

	def deselectForRunConfig(self):
		self._selectedForRunConfig = False
		return self.selectedForRunConfig

	@property
	def selectedForRunConfig(self):
		return self._selectedForRunConfig
	

	