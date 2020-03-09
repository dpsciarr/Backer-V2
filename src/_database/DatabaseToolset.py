'''
Backer Backup Management Software provides the ability to customize and streamline your backup process.

Copyright (C) 2020 Dominic P. Sciarrino

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see the source code at GitHub for
COPYING.txt file or contact the author at dominic.sciarrino@gmail.com.
'''

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