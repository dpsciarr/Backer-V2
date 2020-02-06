'''
	configFileCongruencyCheck()

	The returned JSON from buildJSONFromDatabase() is compared to the current configuration file.

	If True, the congruency check passes and the database is congruent with the configuration file.

	If False, the congruency check fails and the configuration file needs to be updated with JSON generated based on the current 
	database structure.
	'''
	def configFileCongruencyCheck(self):
		self.sendToOutput("Configuration File Congruency Check...")
		configFolder = os.path.join(self.getModel().getController().requestApplicationRoot(), "cfg")

		dbData = self.buildJSONFromDatabase()
		with open(os.path.join(configFolder, "dbcfg-temp.txt"), 'w') as dumpFile:
			json.dump(dbData, dumpFile)

		cfgData = ""
		with open(self.getModel().getController().requestConfigFilePath(), 'r') as cfgFile:
			cfgData = json.load(cfgFile)

		dbDataFromFile = ""
		with open(os.path.join(configFolder, "dbcfg-temp.txt"), 'r') as dbFile:
			dbDataFromFile = json.load(dbFile)

		if cfgData == dbDataFromFile:
			self.sendToOutput(f"   Configuration file syncronized with database for user '{self.currentUser}'")
			return True
		else:
			self.sendToOutput("   WARNING: Configuration file NOT syncronized.")
			return False






	'''
	buildJSONFromDatabase()

	Builds a JSON object based on the current database make-up for current user object.

	Returns the JSON-like dictionary based on the current user's database structure.
	'''

	def buildJSONFromDatabase(self):
		userStruct = self.buildBaseJSONStructure()
		userData = self.getDictFromDatabase("users", "user_id", self.currentUserID, True)

		#Use Current User ID instead of Default
		userStruct[self.currentUserID] = userStruct.pop(-1, -1)
		#Change User Data
		userStruct[self.currentUserID]["user_id"] = userData["user_id"]
		userStruct[self.currentUserID]["user_name"] = userData["user_name"]
		userStruct[self.currentUserID]["pwd"] = userData["pwd"]

		#Get Device Data
		devDataHeaders, devData = self.getDictFromDatabase("devices", "device_user", self.currentUserID, False)
		devList = []
		for result in devData:
			devStruct = {}
			for result2 in result:
				devStruct = dict(zip(devDataHeaders, result))
			devList.append(devStruct)
		userStruct[self.currentUserID]["devices"] = devList
		
		#Get Drive Data
		for device in userStruct[self.currentUserID]["devices"]:
			drvList = []
			device["drives"] = []
			devID = device["device_id"]
			drvData = self.getDictFromDatabase("drives", "associated_device", devID, True)
			drvList.append(drvData)
			device["drives"] = drvList

		#Get Collection Data
		collDataHeaders, collData = self.getDictFromDatabase("collections", "collection_creator", self.currentUser, False)
		collList = []
		for result in collData:
			collStruct = {}
			for result2 in result:
				collStruct = dict(zip(collDataHeaders, result))
			collList.append(collStruct)
		userStruct[self.currentUserID]["collections"] = collList

		#Get Procedure Data
		for collection in userStruct[self.currentUserID]["collections"]:
			collection["procedures"] = []
			collID = collection["collection_id"]
			procDataHeaders, procData = self.getDictFromDatabase("procedures", "member_of", collID, False)
			
			procStruct = {}
			procList = []
			for result in procData:
				procStruct = dict(zip(procDataHeaders, result))
				procList.append(procStruct)
			collection["procedures"] = procList

		return userStruct

	'''
	getDictFromDatabase()

	Takes in:
	- 'table' which specifies the table to access in the database.
	- 'field' which specifies the field to access within 'table'
	- 'dataID' which specifies the data criteria to compare against.
	- 'option'
	   - If 'True', a struct is generated and returned
	   - Else, returns raw data in the form of a tuple ('headers, data')
	'''
	def getDictFromDatabase(self, table, field, dataID, option=True):
		self.getModel().getController().requestOpenDatabase()
		sql = f"""SELECT * FROM {table} WHERE {field} = '{dataID}'"""
		crsr = self.getModel().getController().requestDatabaseCursor()
		crsr.execute(sql)
		headers = [x[0] for x in crsr.description]
		data = crsr.fetchall()
		self.model.getController().requestCloseDatabase()

		if option:
			struct = {}
			for result in data:
				struct.update(dict(zip(headers, result)))
			return struct
		else:
			return headers, data