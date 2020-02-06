
	'''
	buildObjectModel()

	If the information source is from the MySQL database, then this is a wrapper function for 'buildModelFromDatabase()' in the Object
	   Manager class.
	If the information course is from the configuration file, then this is a wrapper function for 'buildModelFromConfigFile()' in the
	   Object Manager class.
	'''
	def buildObjectModel(self):
		#self.informationSource = SOURCE_CONFIG_NO_DB
		self.sendToOutput("Building Object Model...")
		self.sendToOutput(f"    Current information source: {self.informationSource}")

		objManager = self.getModel().getController().requestObjectManager()

		#database
		if self.informationSource == SOURCE_DATABASE or self.informationSource == SOURCE_DATABASE_NO_CFG:
			self.getModel().getController().requestOpenDatabase()
			objManager.buildModelFromDatabase()
			self.getModel().getController().requestCloseDatabase()
			self.sendToOutput("    Object model built from database.")

		#config file
		if self.informationSource == SOURCE_CONFIG_NO_DB:
			objManager.buildModelFromConfigFile()
			self.sendToOutput("    Object model built from configuration file.")

		#no source
		if self.informationSource == NO_SOURCE:
			self.sendToOutput("    WARNING: No information source available.")
			self.sendToOutput("      Connect to a database or connect a configuration file.")



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
	objectModelCongruencyTest()

	Builds a JSON-like object from the current Object Model

	If the information source is based on the database, then a JSON-like object is built from the database configuration.
	Else, if the information source is based on the configurtion file, then a JSON-like object is built from the configuration file.

	If the two generated JSON-like objects are equal then this function returns True, else False
	'''
	def objectModelCongruencyTest(self):
		self.sendToOutput("Running Object Model Congruency Test...")

		#build JSON from Object Model
		jsonObjModel = self.buildJSONFromObjectModel()

		if self.informationSource == SOURCE_DATABASE or self.informationSource == SOURCE_DATABASE_NO_CFG:
			result = self.buildJSONFromDatabase()
			try:
				jsonDatabaseModel = result[self.currentUserID]
			except Exception as e:
				jsonDatabaseModel = result[str(self.currentUserID)]

			if jsonObjModel == jsonDatabaseModel:
				self.sendToOutput("   Success: Object Model matches Database.")
				return True
			else:
				self.sendToOutput("   WARNING: Object Model does not match database. Generate new object model.")


		if self.informationSource == SOURCE_CONFIG_NO_DB:
			configFolder = os.path.join(self.getModel().getController().requestApplicationRoot(), "cfg")
			with open(os.path.join(configFolder, "config.cfg"), 'r') as fileToLoad:
				jsonConfigFromFile = json.load(fileToLoad)

			jsonConfigModel = jsonConfigFromFile[str(self.currentUserID)]

			if jsonObjModel == jsonConfigModel:
				self.sendToOutput("   Success: Object Model matches Configuration File")
				return True
			else:
				self.sendToOutput("   WARNING: Object Model does not match configuration file. ")
				self.sendToOutput("     Generate new configure file or new object model.")
				return False

		if self.informationSource == NO_SOURCE:
			self.sendToOutput("   WARNING: No information source detected.")
			return False

	'''
	buildJSONFromObjectModel()

	Returns a JSON structure that represents the current user's Object Model.
	'''
	def buildJSONFromObjectModel(self):
		objManager = self.getModel().getController().requestObjectManager()

		objModelStruct = {}

		user = objManager.getCurrentUserObject()
		userStruct = {}
		devices = user.getDevices()
		collections = user.getCollections()

		userStruct["user_id"] = user.getID()
		userStruct["user_name"] = user.getName()
		userStruct["pwd"] = user.getPassword()

		deviceList = []
		for key in devices:
			devStruct = {}
			devStruct["device_id"] = devices[key].getID()
			devStruct["device_name"] = devices[key].getName()
			devStruct["device_user"] = devices[key].getDeviceUser()

			drives = devices[key].getDrives()
			driveList = []

			for key2 in drives:
				driveStruct = {}
				driveStruct["drive_id"] = drives[key2].getID()
				driveStruct["drive_letter"] = drives[key2].getDriveLetter()
				driveStruct["drive_name"] = drives[key2].getName()
				driveStruct["associated_device"] = drives[key2].getAssociatedDevice()
				driveList.append(driveStruct)

			if len(driveList) == 0:
				emptyStruct = {}
				driveList.append(emptyStruct)

			devStruct["drives"] = driveList
			deviceList.append(devStruct)
		
		userStruct["devices"] = deviceList
		
		collList = []
		for key in collections:
			collStruct = {}
			collStruct["collection_id"] = collections[key].getID()
			collStruct["collection_name"] = collections[key].getName()
			collStruct["collection_creator"] = collections[key].getCollectionCreator()

			procs = collections[key].getProcedures()
			procList = []
			for key2 in procs:
				procStruct = {}
				procStruct["proc_num"] = procs[key2].getID()
				procStruct["src_path"] = procs[key2].getSourcePath()
				procStruct["dest_path"] = procs[key2].getDestinationPath()
				procStruct["member_of"] = procs[key2].getParentCollection()
				procStruct["op_code"] = procs[key2].getOperationCode()
				procStruct["proc_name"] = procs[key2].getName()
				procList.append(procStruct)

			collStruct["procedures"] = procList
			collList.append(collStruct)

		userStruct["collections"] = collList

		return userStruct