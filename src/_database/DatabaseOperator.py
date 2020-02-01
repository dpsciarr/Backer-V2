import sqlite3
import os.path
import sys

dbDir = os.path.dirname(__file__)
sys.path.append(dbDir)

from DatabaseToolset import DatabaseToolset
from BackerQueries import BackerQueries

sys.path.remove(dbDir)

class DatabaseOperator:
	def __init__(self, application):
		self._application = application
		self._databaseOK = False
		self._sqliteVersion = ""
		self._databaseName = "backer.db"
		self._databasePath = os.path.join(os.path.dirname(__file__), self._databaseName)
		self._connection = None
		self._connected = False
		self._cursor = None

		self._toolset = DatabaseToolset(self)
		self._queries = BackerQueries(self)

		try:
			self.openDatabase()
			sql = """SELECT sqlite_version()"""
			self.setCursor()
			self.execute(sql)
			self.commit()
			version = self.fetchall()
			self.closeDatabase()
			self._databaseOK = True
			if len(version) > 0:
				self._sqliteVersion = version[0][0]
			else:
				self._databaseOK = False
		except Exception as e:
			self._databaseOK = False

	@property
	def toolset(self):
		return self._toolset

	@property
	def queries(self):
		return self._queries

	@property
	def application(self):
		return self._application

	@property
	def databaseOK(self):
		return self._databaseOK
	
	
	
	
	'''
	openDatabase()

	Opens the SQLite3 database file.
	'''

	def openDatabase(self):
		try:
			if self._connected == False:
				self._connection = sqlite3.connect(self._databasePath)
				self._connected = True
		except:
			print(f"Failed to connect to database {self._databaseName}")
			return f"Failed to connect to dataase {self._databaseName}"

	'''
	closeDatabase()

	Closes the SQLite3 database file.
	'''
	def closeDatabase(self):
		if self._connected == True:
			self._connection.close()
			self._connected = False

	'''
	setCursor()

	Gives the DB Operator it's database cursor.
	'''
	def setCursor(self):
		self._cursor = self._connection.cursor()

	'''
	fetchall()

	Fetches whatever the database spits out.
	'''
	def fetchall(self):
		if self._cursor != None:
			return self._cursor.fetchall()
		else:
			return None

	'''
	fetchone()

	Fetches just one of whatever the database spits out.
	'''
	def fetchone(self):
		if self._cursor != None:
			return self._cursor.fetchone()
		else:
			return None

	'''
	execute()

	Executes a SQL query on the database.
	'''
	def execute(self, sql):
		self._cursor.execute(sql)

	'''
	commit()

	Commits to the SQLite database.
	'''
	def commit(self):
		if self._connected:
			if self._connection != None:
				self._connection.commit()

	'''
	checkInsertData(insertData)

	Wrapper for function in toolset
	'''
	def checkInsertData(self, insertData):
		return self.toolset.checkInsertData(insertData)
