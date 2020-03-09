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

import json

class JsonOperator:
	def __init__(self, configurationManager):
		self._configurationManager = configurationManager

	@property
	def configurationManager(self):
		return self._configurationManager
	

	def load(self, file):
		return json.load(file)

	def dump(self, data, file):
		return json.dump(data, file)


	'''
	buildBaseConfigurationStructure()

	Builds and returns a JSON template used for the Backer application.
	Essentially, a JSON dict with no stored information.
	'''
	def buildBaseConfigurationStructure(self, userID = -1):
		struct = {}
		userStruct = {"user_id": userID, "user_name":"", "passcode":""}

		userStruct["devices"] = []
		userStruct["collections"] = []

		struct[userID] = {}
		struct[userID].update(userStruct)

		return struct

	'''
	buildJSONFromObjectModel(currentUserObject)

	Returns a JSON structure that represents the current user's Object Model.
	'''
	def buildJSONFromObjectModel(self, currentUserObject):
		#strUserID = str(currentUserID)
		objectModelStruct = {}
		strUserID = str(currentUserObject.userID)

		userStruct = self.buildBaseConfigurationStructure()

		#Pop the default
		userStruct[strUserID] = userStruct.pop(-1, -1)

		user = currentUserObject
		devices = user.devices
		collections = user.collections

		userStruct[strUserID]["user_id"] = user.userID
		userStruct[strUserID]["user_name"] = user.username
		userStruct[strUserID]["passcode"] = user.passcode

		deviceList = []
		for key in devices:
			devStruct = {}
			devStruct["device_id"] = devices[key].deviceID
			devStruct["device_name"] = devices[key].deviceName
			devStruct["user_id"] = devices[key].deviceUser

			drives = devices[key].drives
			driveList = []

			for key2 in drives:
				driveStruct = {}
				driveStruct["drive_id"] = drives[key2].driveID
				driveStruct["drive_name"] = drives[key2].driveName
				driveStruct["drive_letter"] = drives[key2].driveLetter
				driveStruct["device_id"] = drives[key2].deviceID
				driveList.append(driveStruct)

			if len(driveList) == 0:
				emptyStruct = {}
				driveList.append(emptyStruct)

			devStruct["drives"] = driveList
			deviceList.append(devStruct)

		userStruct[strUserID]["devices"] = deviceList

		collectionList = []
		for key in collections:
			collStruct = {}
			collStruct["collection_id"] = collections[key].collectionID
			collStruct["collection_name"] = collections[key].collectionName
			collStruct["user_id"] = collections[key].userID

			procedures = collections[key].procedures
			procedureList = []
			for key2 in procedures:
				procStruct = {}
				procStruct["procedure_id"] = procedures[key2].procedureID
				procStruct["procedure_name"] = procedures[key2].procedureName
				procStruct["source_path"] = procedures[key2].sourcePath
				procStruct["destination_path"] = procedures[key2].destinationPath
				procStruct["collection_id"] = procedures[key2].collectionID
				procStruct["operation_id"] = procedures[key2].operationID
				procedureList.append(procStruct)

			collStruct["procedures"] = procedureList
			collectionList.append(collStruct)

		userStruct[strUserID]["collections"] = collectionList

		return userStruct





	'''
	buildJSONFromDatabase(databaseOperator)

	Builds a JSON object based on the current database make-up for current user object.

	Returns the JSON-like dictionary based on the current user's database structure.
	'''
	def buildJSONFromDatabase(self, currentUserID, databaseOperator):
		strUserID = str(currentUserID)

		userStruct = self.buildBaseConfigurationStructure()
		userData = databaseOperator.queries.getUserDictFromDatabase(strUserID)

		#Pop the default
		userStruct[strUserID] = userStruct.pop(-1, -1)

		#Get/Change User Data
		userStruct[strUserID]["user_id"] = userData["user_id"]
		userStruct[strUserID]["user_name"] = userData["user_name"]
		userStruct[strUserID]["passcode"] = userData["passcode"]

		#Get Device Data
		devDataHeaders, devData = databaseOperator.queries.getDevicesDictFromDatabase(strUserID)
		devList = []
		for result in devData:
			devStruct = {}
			for result2 in result:
				devStruct = dict(zip(devDataHeaders, result))
			devList.append(devStruct)
		userStruct[strUserID]["devices"] = devList

		for device in userStruct[strUserID]["devices"]:
			drvList = []
			device["drives"] = []
			devID = device["device_id"]
			drvData = databaseOperator.queries.getDrivesDictFromDatabase(devID)
			drvList.append(drvData)
			device["drives"] = drvList

		#Get CollectionData
		collDataHeaders, collData = databaseOperator.queries.getCollectionsDictFromDatabase(strUserID)
		collList = []
		for result in collData:
			collStruct = {}
			for result2 in result:
				collStruct = dict(zip(collDataHeaders, result))
			collList.append(collStruct)
		userStruct[strUserID]["collections"] = collList

		#Get Procedures
		for collection in userStruct[strUserID]["collections"]:
			collection["procedures"] = []
			collID = collection["collection_id"]
			procDataHeaders, procData = databaseOperator.queries.getProceduresDictFromDatabase(collID)

			procStruct = {}
			procList = []
			for result in procData:
				procStruct = dict(zip(procDataHeaders, result))
				procList.append(procStruct)
			collection["procedures"] = procList

		return userStruct