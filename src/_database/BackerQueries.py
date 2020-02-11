
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

	'''
	checkDatabaseForProcedure(procName, collectionName)

	Checks if the procedure exists in the database for collection 'collectionName'
	'''
	def checkDatabaseForProcedure(self, procName, collectionID):
		table = "procedures"
		select = "procedure_name"
		where = "collection_id"

		self.operator.openDatabase()
		sql = f"SELECT {select} FROM {table} WHERE {where} = '{collectionID}'"
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		procExists = False
		if len(data) != 0:
			for each in data:
				if each[0] == procName:
					procExists = True

		return procExists

	'''
	addProcedure(procedureName, sourcePath, destinationPath, collectionID, operationID)

	Add a new procedure to the next available ID in the database.
	'''
	def addProcedure(self, procedureName, sourcePath, destinationPath, collectionID, operationID):
		table = "procedures"

		#Find the next available collection ID
		procedureID = self.operator.toolset.nextAvailableID("procedures")

		#Add Collection to database
		self.operator.openDatabase()
		sql = f"INSERT INTO procedures(procedure_id, procedure_name, source_path, destination_path, collection_id, operation_id) \
		VALUES ({procedureID}, '{procedureName}', '{sourcePath}', '{destinationPath}', {collectionID}, {operationID})"
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

		return procedureID

	'''
	deleteProcedure(procedureID)

	Deletes a procedure from the procedures table in database.
	'''
	def deleteProcedure(self, procID):
		table = "procedures"
		field = "procedure_id"

		self.operator.openDatabase()
		sql = f"""DELETE FROM {table} WHERE {field} = '{procID}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

		
	'''
	deleteDrive(driveID)

	Deletes a drive from the drives table in database.
	'''
	def deleteDrive(self, driveID):
		table = "drives"
		field = "drive_id"

		self.operator.openDatabase()
		sql = f"""DELETE FROM {table} WHERE {field} = '{driveID}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	deleteCollection(collectionID)

	Deletes a collection from the collections table in database.
	'''
	def deleteCollection(self, collectionID):
		table = "collections"
		field = "collection_id"

		self.operator.openDatabase()
		sql = f"""DELETE FROM {table} WHERE {field} = '{collectionID}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	deleteDevice(deviceID)

	Deletes a device from the devices table in database.
	'''
	def deleteDevice(self, deviceID):
		table = "devices"
		field = "device_id"

		self.operator.openDatabase()
		sql = f"""DELETE FROM {table} WHERE {field} = '{deviceID}'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	renameDevice(old_id, new)

	Renames a device from 'old' to 'new'.
	'''
	def renameDevice(self, old_id, new):
		table = "devices"
		field = "device_name"
		where = "device_id"
	
		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET {field} = '{new}' WHERE {where} = {old_id}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	renameCollection(old_id, new)

	Renames a collection from 'old' to 'new'.
	'''
	def renameCollection(self, old_id, new):
		table = "collections"
		field = "collection_name"
		where = "collection_id"
	
		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET {field} = '{new}' WHERE {where} = {old_id}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	editDriveName(name)

	Renames a drive to "name".
	'''
	def updateDriveName(self, newDriveName, driveID):
		table = "drives"
		field = "drive_name"
		where = "drive_id"

		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET "{field}" = '{newDriveName}' WHERE "{where}" = {driveID}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	editDriveLetter(letter)

	Assigns a new letter to a drive.
	'''
	def updateDriveLetter(self, newLetter, driveID):
		table = "drives"
		field = "drive_letter"
		where = "drive_id"

		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET "{field}" = '{newLetter}' WHERE "{where}" = {driveID}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()
	
	'''
	updateProcedureName(name, procID)

	Updates procedure name.
	'''
	def updateProcedureName(self, newProcedureName, procID):
		table = "procedures"
		field = "procedure_name"
		where = "procedure_id"

		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET "{field}" = '{newProcedureName}' WHERE "{where}" = {procID}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	updateProcedureSource(src, procID)

	Updates the source of procedure with ID procID.
	'''
	def updateProcedureSource(self, newSourcePath, procID):
		table = "procedures"
		field = "source_path"
		where = "procedure_id"

		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET "{field}" = '{newSourcePath}' WHERE "{where}" = {procID}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	updateProcedureDestination(destination, procID)

	Updates the destination of procedure with ID procID.
	'''
	def updateProcedureDestination(self, newDestinationPath, procID):
		table = "procedures"
		field = "destination_path"
		where = "procedure_id"

		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET "{field}" = '{newDestinationPath}' WHERE "{where}" = {procID}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	'''
	updateProcedureOpCode(opCode, procID)

	Updates the op code of procedure with ID procID.
	'''
	def updateProcedureOpCode(self, opCode, procID):
		table = "procedures"
		field = "operation_id"
		where = "procedure_id"

		self.operator.openDatabase()
		sql = f"""UPDATE {table} SET "{field}" = '{opCode}' WHERE "{where}" = {procID}"""
		self.operator.setCursor()
		self.operator.execute(sql)
		self.operator.commit()
		self.operator.closeDatabase()

	