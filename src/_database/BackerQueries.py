
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
		sql = f"""SELECT * FROM {table} WHERE {field} = 'device_id'"""
		self.operator.setCursor()
		self.operator.execute(sql)
		headers = [x[0] for x in self.operator.cursor.description]
		data = self.operator.fetchall()
		self.operator.closeDatabase()

		struct = {}
		for result in data:
			struct.update(dict(zip(headers, result)))
			
		return struct