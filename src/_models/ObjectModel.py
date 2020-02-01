import json

class ObjectModel:
	def __init__(self, application):
		print("Hi, I host the application's object model!")

	def buildDatabaseModel(self):
		print("Building model from database...")
	

	'''
	def buildModelFromDatabase(self):
		userID = self.mainController.getCurrentUserID()
		userName = self.mainController.getCurrentUser()

		sql = f"""SELECT pwd FROM users WHERE user_id = '{userID}'"""
		pwd = self.modelController.queryDatabase(sql)[0][0]
		self.currentUser = User(userID, userName, pwd)

		sql = f"""SELECT * FROM devices WHERE device_user = '{userID}'"""
		devices = self.modelController.queryDatabase(sql)
		for item in devices:
			dev = Device(id=item[0], name=item[1], user=item[2])
			
			sql = f"""SELECT * FROM drives WHERE associated_device = '{item[0]}'"""
			drives = self.modelController.queryDatabase(sql)
			for drive in drives:
				drv = Drive(id=drive[0], letter=drive[1], name=drive[2], device=drive[3])
				dev.addDrive(drv)

			self.currentUser.addDevice(dev)


		sql = f"""SELECT * FROM collections WHERE collection_creator = '{userName}'"""
		collections = self.modelController.queryDatabase(sql)
		for item in collections:
			coll = Collection(id=item[0], name=item[1], creator=item[2])

			sql = f"""SELECT * FROM procedures WHERE member_of = '{item[0]}'"""
			procs = self.modelController.queryDatabase(sql)
			for proc in procs:
				p = Procedure(id=proc[0], name=proc[5], src=proc[1], dest=proc[2], collection=proc[3], operation=proc[4])
				coll.addProcedure(p)

			self.currentUser.addCollection(coll)



	'''
	def buildConfigurationModel(self):
		print("Building model from configuration file...")
	

	'''
	def buildModelFromConfigFile(self):
		userID = self.mainController.getCurrentUserID()
		userName = self.mainController.getCurrentUser()

		#need to get configuration file contents
		cfgFilePath = self.modelController.requestConfigFilePath()

		with open(cfgFilePath, 'r') as cfgFile:
			cfgJSON = json.load(cfgFile)

		userConfig = ""
		try:
			userConfig = cfgJSON[userID]
		except Exception as e:
			userConfig = cfgJSON[str(userID)]

		#get user information
		pwd = userConfig["pwd"]
		self.currentUser = User(userID, userName, pwd)
		
		#get devices information
		for dev in userConfig["devices"]:
			devID = dev["device_id"]
			devName = dev["device_name"]
			devUser = dev["device_user"]

			device = Device(devID, devName, devUser)
			self.currentUser.addDevice(device)

			drvs = dev["drives"]
			for drv in drvs:
				drvID = drv["drive_id"]
				drvLetter = drv["drive_letter"]
				drvName = drv["drive_name"]
				drvDevice = drv["associated_device"]

				drive = Drive(drvID, drvLetter, drvName, drvDevice)
				device.addDrive(drive)

		for coll in userConfig["collections"]:
			collID = coll["collection_id"]
			collName = coll["collection_name"]
			collCreator = coll["collection_creator"]

			collection = Collection(collID, collName, collCreator)
			self.currentUser.addCollection(collection)

			procs = coll["procedures"]
			for proc in procs:
				procNum = proc["proc_num"]
				procName = proc["proc_name"]
				procSrc = proc["src_path"]
				procDest = proc["dest_path"]
				procColl = proc["member_of"]
				procOp = proc["op_code"]

				procedure = Procedure(procNum, procName, procSrc, procDest, procColl, procOp)
				collection.addProcedure(procedure)
	'''











class BackerObject():
	def __init__(self):
		self._identifier = -1
		self._name = ""

	@property
	def identifier(self):
		return self._identifier
	
	@identifier.setter
	def identifier(self, value):
		self._identifier = value

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value









class User(BackerObject):
	def __init__(self, identifier, name, passcode):
		self._userID = identifier
		self._username = name
		self._passcode = passcode
		super().identifier = self._userID
		super().name = self._username
		self._devices = {}
		self._collections = {}

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
		self.collections[collection.identifier] = collection
	
	def addDevice(self, device):
		self.devices[device.identifier] = device

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













class Device(BackerObject):
	def __init__(self, identifier, name, user):
		self._deviceID = identifier
		self._deviceName = name
		self._deviceUser = user
		super().identifier = self._identifier
		super().name = self._deviceName
		self._drives = {}

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
		self.drives[drive.identifier] = drive

	def getDrive(self, driveID):
		if len(self.drives) > 0 and self.drives[driveID] is not None:
			return self.drives[driveID]
		else:
			return None

	def removeDrive(self, driveID):
		return self.drives.pop(driveID, None)















class Drive(BackerObject):
	def __init__(self, identifier, driveLetter, driveName, deviceID):
		self._driveID = identifier
		self._driveLetter = driveLetter
		self._driveName = driveName
		self._deviceID = deviceID
		super().identifier = self._driveID
		super().name = self._driveName

	@property
	def driveLetter(self):
		return self._driveLetter

	@property
	def deviceID(self):
		return self._deviceID

	@driveLetter.setter
	def driveLetter(self, value):
		self._driveLetter = value

	@deviceID.setter
	def deviceID(self, value):
		self._deviceID = value
	













	
class Collection(BackerObject):
	def __init__(self, identifier, collectionName, userID):
		self._collectionID = identifier
		self._collectionName = collectionName
		self._userID = userID
		super().identifier = self._collectionID
		super().name = self._collectionName
		self._procedures = {}

	@property
	def userID(self):
		return self._userID

	@userID.setter
	def userID(self, value):
		self._userID = value

	@property
	def procedures(self):
		return self._procedures
	
	def addProcedure(self, procedure):
		self._procedures[procedure.identifier] = procedure

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















class Procedure(BackerObject):
	def __init__(self, identifier, procName, source, destination, collectionID, operationID):
		self._procedureID = identifier
		self._procedureName = procName
		self._sourcePath = source
		self._destinationPath = destination
		self._collectionID = collectionID
		self._operationID, operationID

		self._selectedForRunConfig = False
		super().identifier = self._procedureID
		super().name = self._procedureName

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
	

	