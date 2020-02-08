
class BackerQueries:
	def __init__(self, operator):
		self._operator = operator

	@property
	def operator(self):
		return self._operator
	
	'''
	addUser(self, passcode)

	Adds a user to the database.
	'''
	def addUser(self, user, passcode):
		usernameValid = self.operator.toolset.checkInsertData(user)
		
		if user == "":
			return "FAILED: No Username entered."
		if passcode == "":
			return "FAILED: No Passcode entered."
		if usernameValid == False:
			return "FAILED: Invalid characters detected in username."

		#Get the next available ID in users table
		userID = self.operator.toolset.nextAvailableID("users")

		try:
			self.operator.openDatabase()
			sql = f"""INSERT INTO users(user_id, user_name, passcode) VALUES({userID}, '{user}', '{passcode}')"""
			self.operator.setCursor()
			self.operator.execute(sql)
			self.operator.commit()
			self.operator.closeDatabase()
		except Exception as e:
			self.operator.closeDatabase()
			return f"FAILED: {e}"

		return "SUCCESS: '" + user + "' added."



	'''
	getUserDictFromDatabase(userID)

	Returns user data as a struct (for building JSON structs)
	
	'userID' specifies the user ID.
	'''
	def getUserDictFromDatabase(self, userID):
		table = "users"
		field = "user_id"
		user_id = userID

		self.operator.openDatabase()
		sql = f"""SELECT * FROM {table} WHERE {field} = '{user_id}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		struct = {}
		for result in data:
			struct.update(dict(zip(headers, result)))
			
		return struct

	'''
	getDevicesDictFromDatabase(userID)

	Returns device header/data from database
	
	'userID' specifies the user ID the device is associated with
	'''
	def getDevicesDictFromDatabase(self, userID):
		table = "devices"
		field = "user_id"
		user_id = userID

		self.operator.openDatabase()
		sql = f"""SELECT * FROM {table} WHERE {field} = '{user_id}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		return headers, data

	'''
	getDrivesDictFromDatabase(userID)

	Returns drive data as a struct (for building JSON structs)
	
	'devID' specifies the device ID the drive is associated with
	'''
	def getDrivesDictFromDatabase(self, devID):
		table = "drives"
		field = "device_id"
		deviceID = devID

		self.operator.openDatabase()
		sql = f"""SELECT * FROM {table} WHERE {field} = '{deviceID}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		struct = {}
		for result in data:
			struct.update(dict(zip(headers, result)))
			
		return struct

	'''
	getCollectionsDictFromDatabase(userID)

	Returns collection data as a struct (for building JSON structs)
	
	'userID' specifies the user ID the collections is associated with
	'''
	def getCollectionsDictFromDatabase(self, userID):
		table = "collections"
		field = "user_id"
		user_id = userID

		self.operator.openDatabase()
		sql = f"""SELECT * FROM {table} WHERE {field} = '{userID}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		return headers, data

	'''
	getProceduresDictFromDatabase(collID)

	Returns procedure data as a struct (for building JSON structs)
	
	'collID' specifies the collection ID the procedures are associated with
	'''
	def getProceduresDictFromDatabase(self, collID):
		table = "procedures"
		field = "collection_id"
		coll_id = collID

		self.operator.openDatabase()
		sql = f"""SELECT * FROM {table} WHERE {field} = '{coll_id}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		return headers, data

	'''
	getDriveLetterForDeviceFromDatabase(devID)
	'''

	def getDriveLetterForDeviceFromDatabase(self, devID):
		table = "drives"
		device_id = devID
		select = "drive_letter"

		self.operator.openDatabase()
		sql = f"""SELECT {select} FROM {table} WHERE device_id = {device_id}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		return headers, data

	'''
	checkDatabaseForCollection(collectionName, currUser)

	Checks if the collection exists in the database for user 'curreUser'
	'''
	def checkDatabaseForCollection(self, collectionName, currUser):
		table = "collections"
		select = "collection_name"
		where = "user_id"

		self.operator.openDatabase()
		sql = f"SELECT {select} FROM {table} WHERE {where} = '{currUser}'"
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		collExists = False
		if len(data) != 0:
			for each in data:
				if each[0] == collectionName:
					collExists = True

		return collExists

	'''
	addCollection(collectionName, userID)

	Add a new collection to the next available ID in the database.
	'''
	def addCollection(self, collectionName, userID):
		table = "collections"

		#Find the next available collection ID
		collectionID = self.operator.toolset.nextAvailableID("collections")

		#Add Collection to database
		self.operator.openDatabase()
		sql = f"INSERT INTO collections(collection_id, collection_name, user_id) VALUES ({collectionID}, '{collectionName}', '{userID}')"
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

		return collectionID

	'''
	checkDatabaseForDevice(deviceName, currUser)

	Checks if the device exists in the database for user 'curreUser'
	'''
	def checkDatabaseForDevice(self, deviceName, currUser):
		table = "devices"
		select = "device_name"
		where = "user_id"

		self.operator.openDatabase()
		sql = f"SELECT {select} FROM {table} WHERE {where} = '{currUser}'"
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		deviceExits = False
		if len(data) != 0:
			for each in data:
				if each[0] == deviceName:
					deviceExits = True

		return deviceExits

	'''
	addDevice(deviceName, userID)

	Add a new device to the next available ID in the database.
	'''
	def addDevice(self, deviceName, userID):
		table = "devices"

		#Find the next available collection ID
		deviceID = self.operator.toolset.nextAvailableID("devices")

		#Add Collection to database
		self.operator.openDatabase()
		sql = f"INSERT INTO devices(device_id, device_name, user_id) VALUES ({deviceID}, '{deviceName}', '{userID}')"
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

		return deviceID

	'''
	checkDatabaseForDrive(driveName, currUser)

	Checks if the drive exists in the database for user 'currUser'
	'''
	def checkDatabaseForDrive(self, driveName, deviceID):
		table = "drives"
		select = "drive_name"
		where = "device_id"

		self.operator.openDatabase()
		sql = f"SELECT {select} FROM {table} WHERE {where} = '{deviceID}'"
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		driveExists = False
		if len(data) != 0:
			for each in data:
				if each[0] == driveName:
					driveExists = True

		return driveExists


	'''
	addDrive(driveName, driveLetter, deviceID)

	Add a new drive to the next available ID in the database.
	'''
	def addDrive(self, driveName, driveLetter, deviceID):
		table = "drives"

		#Find the next available collection ID
		driveID = self.operator.toolset.nextAvailableID("drives")

		#Add Collection to database
		self.operator.openDatabase()
		sql = f"INSERT INTO drives(drive_id, drive_name, drive_letter, device_id) VALUES ({driveID}, '{driveName}', '{driveLetter}', '{deviceID}')"
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

		return driveID

