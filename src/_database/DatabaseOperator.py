import sqlite3
import os.path

class DatabaseOperator:
	def __init__(self):
		self._databaseName = "backer.db"
		self._databasePath = os.path.join(os.path.dirname(__file__), self._databaseName)
		self._connection = None
		self._connected = False
		self._cursor = None
		self._invalidChars = ["|", "'", ".", "-", "*", "/", "<", ";", ">", ",", "=", "~", "!", "^", "(", ")"]

	@property
	def invalidChars(self):
		return self._invalidChars
	
	def openDatabase(self):
		if self._connected == False:
			self._connection = sqlite3.connect(self._databasePath)
			self._connected = True

	def closeDatabase(self):
		if self._connected == True:
			self._connection.close()
			self._connected = False

	def setCursor(self):
		self._cursor = self._connection.cursor()

	def fetchall(self):
		if self._cursor != None:
			return self._cursor.fetchall()
		else:
			return None

	def fetchone(self):
		if self._cursor != None:
			return self._cursor.fetchone()
		else:
			return None

	def execute(self, sql):
		self._cursor.execute(sql)


	def commit(self):
		if self._connected:
			if self._connection != None:
				self._connection.commit()