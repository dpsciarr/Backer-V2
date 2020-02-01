import sqlite3
import os.path

class DatabaseToolset:
	def __init__(self, operator):
		self._operator = operator
		self._invalidChars = ["|", "'", ".", "-", "*", "/", "<", ";", ">", ",", "=", "~", "!", "^", "(", ")"]

	@property
	def operator(self):
		return self._operator

	@property
	def invalidChars(self):
		return self._invalidChars

	'''
	checkInsertData(insertData)

	Input a string, if an invalid char is detected returns False.

	Otherwise True.
	'''
	def checkInsertData(self, insertData):
		for char in self._invalidChars:
			if char in insertData:
				return False

		return True

	'''
	processData(data)
	
	Readies data to be inserted into the database by escaping
	invalid characters.
	'''
	def processData(self, data):
		_data = data
		for char in self._invalidChars:
			if char in _data:
				_data = _data.replace(char, "\\" + char)

		return _data

	'''
	nextAvailableID(tableName)
	
	Given a table name, find the next available ID in the table.
	'''
	def nextAvailableID(self, tableName):
		colName = tableName[:-1] + "_id"
		
		self._operator.openDatabase()
		sql = f"""SELECT MAX({colName}) FROM {tableName}"""
		self._operator.setCursor()
		self._operator.execute(sql)
		self._operator.commit()
		data = self._operator.fetchall()
		self._operator.closeDatabase()

		if data[0][0] == None:
			return 1
		else:
			return int(data[0][0]) + 1
	
	'''
	'	isPath(path)
	'
	'		Returns True if the path 'path' exists. False otherwise.
	'''
	def isPath(self, path):
		return os.path.exists(path)

	'''
	'	isFile(f)
	'
	'		Returns True if the path 'f' exists AND is a file.
	'''
	def isFile(self, f):
		if self.isPath(f):
			return os.path.isfile(f)
		return False