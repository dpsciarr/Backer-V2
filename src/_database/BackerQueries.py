
class BackerQueries:
	def __init__(self, operator):
		self._operator = operator

	@property
	def operator(self):
		return self._operator
	

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