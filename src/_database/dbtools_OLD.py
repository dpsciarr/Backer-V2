import pymysql


'''
'
'	addUser(user, pw)
'
'	user (string)
'		Username of the desired user
'
'	pw (string)
'		Password of the desired user
'
'
'''
def addUser(user, pw):
	check = checkStrValidity(user)
	if user == "":
		return "FAILED: No Username entered."
	if pw == "":
		return "FAILED: No Password entered."
	if user != check:
		return "FAILED: Invalid characters detected."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"INSERT INTO users(user_name, pwd) VALUES('{user}','{pw}')"
	try:
		cursor.execute(sql)
		db.commit()
	except pymysql.Error as e:
		db.rollback()
		if e.args[0] == 1062:
			return "FAILED: Duplicate user detected."
		else:
			return "Unknown error detected...contact support if the problem persists."
	db.close()
	return "SUCCESS: " + user + " added."

'''
'
'	addCollection(collectionName, user)
'
'		collectionName:
'			Name of collection.
'
'		user:
'			User attributed to said collection.
'
'''

def addCollection(collectionName, user):
	check = checkStrValidity(user)
	if collectionName == "":
		return "FAILED: No Collection Name entered."
	if user == "":
		return "FAILED: No Username entered."
	if user != check:
		return "FAILED: Invalid characters detected in Username."
	check = checkStrValidity(collectionName)
	if collectionName != check:
		return "FAILED: Invalid characters detected in Collection Name."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"INSERT INTO collection(collection_name, collection_creator) VALUES('{collectionName}', '{user}')"
	try:
		cursor.execute(sql)
		db.commit()
	except pymysql.Error as e:
		db.rollback()
		if e.args[0] == 1062:
			return "FAILED: Duplicate Collection detected."
		else:
			return "Unknown error detected...contact support if the problem persists."
	db.close()
	return "SUCCESS: " + collectionName + " has been entered for user " + user + "."


'''
'	addProcedure
'
'		procName:
'			The procedure name.
'
'		collectionName:
'			The collection where the procedure will be stored.
'
'		source:
'			The source path which will be be backed up.
'		
'		destination:
'			The destination of the back-up file
'
'		op_code:
'			The code that describes how to treat the back-up source and destination files.
'			Op_codes are listed in the possibleOpCodes array.
'
'
'''

possibleOpCodes = [1, 2, 3, 4, 5, 6, 7]
def addProcedure(procName, collectionName, source, destination, op_code):
	if op_code not in possibleOpCodes:
		return "FAILED: Op code unresolved."
	check = checkStrValidity(procName)
	if check != procName:
		return "FAILED: Procedure name contains unvalid characters."

	#check if source is real
	#check if destination is real

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	sql = f"SELECT * FROM collection WHERE collection.collection_name='{collectionName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except pymysql.Error as e:
		db.rollback()

	data = cursor.fetchall()
	flag = 0
	for d in data:
		if d[1] == collectionName:
			flag = 1
			break

	if flag == 0:
		db.close()
		return "FAILED: Collection does not exist."

	sql = f"INSERT INTO procedures(src_path, dest_path, member_of, op_code, proc_name) VALUES('{source}', '{destination}', '{collectionName}', {op_code}, '{procName}')"
	try:
		cursor.execute(sql)
		db.commit()
	except pymysql.Error as e:
		db.rollback()
		if e.args[0] == 1062:
			return "FAILED: Duplicate Procedure detected."
		else:
			return "Unknown error detected...contact support if the problem persists."


	db.close()
	return "SUCCESS: Procedure " + procName + " added to " + collectionName + ". \nSource: " + source + " Destination: " + destination + "\nOp Code: " + str(op_code)

'''
'
'	removeUser(user)
'
'		user:
'			Specifies the user to remove.
'
'''

def removeUser(user):
	check = checkStrValidity(user)
	if user == "":
		return "FAILED: Nothing entered."
	if user != check:
		return "FAILED: Invalid characters detected."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM users WHERE user_name = '{user}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	data = cursor.fetchall()

	flag = 0
	for d in data:
		if d[1] == user:
			flag = 1
			break;

	if flag == 0:
		db.close()
		return "FAILED: Username does not exist in database."

	sql = f"DELETE FROM users WHERE user_name = '{user}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
		print("Rolling back...")
	db.close()

	return "SUCCESS: User " + user + " removed."

'''
'
'	removeCollection(collectionName, userid="")
'
'		collectionName:
'			Name of collection to remove.
'
'		userid:
'			Name of user to remove collection from.
'
'''

def removeCollection(collectionName, userid=""):
	if(userid==""):
		return "FAILED: Use both the Collection Name and the Username associated with the Collection."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	sql = f"SELECT * FROM collection WHERE collection_name = '{collectionName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	data = cursor.fetchall()

	flag = 0
	for d in data:
		if d[1] == collectionName:
			flag = 1
			break

	if flag == 0:
		db.close()
		return "FAILED: Collection does not exist in database."

	sql = f"DELETE FROM collection WHERE collection.collection_name='{collectionName}' AND collection.collection_creator='{userid}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	db.close()
	return "SUCCESS: " + collectionName + " from User " + userid + " has been removed."

def removeProcedures(procid, collectionName):
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"DELETE FROM procedures WHERE procedures.proc_num={procid} AND procedures.member_of='{collectionName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
		print("Rolling back...")
	db.close()

'''
'
'	changePassword(username, new_pw)
'
'		username:
'			User to change password
'
'		new_pw:
'			the new password
'
'''

def changePassword(username, new_pw):
	if username == "":
		return "FAILED: No user specified."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"UPDATE users SET pwd='{new_pw}' WHERE user_name='{username}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	db.close()

	return "SUCCESS: Password for " + username + " changed."

'''
'
'	changeCollectionName(collName, new_name)
'
'		collName:
'			The name of the collection you want to change the name of.
'
'		new_name:
'			The new name of the collection.
'
'''

def changeCollectionName(collName, new_name):
	if new_name == "":
		return "FAILED: No collection name specified."
	check = checkStrValidity(new_name)
	if check != new_name:
		return "FAILED: Invalid characters detected."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	sql = f"SELECT * FROM collection WHERE collection.collection_name='{collName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except pymysql.Error as e:
		db.rollback()
		print(e.args[1])

	data = cursor.fetchall()
	flag = 0
	for d in data:
		if d[1] == collName:
			flag = 1
			break

	if flag == 0:
		db.close()
		return "FAILED: No such collection in database."

	sql = f"UPDATE collection SET collection.collection_name='{new_name}' WHERE collection.collection_name='{collName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
		print("Rolling back...")
	db.close()
	return "SUCCESS: Collection " + collName + " changed to " + new_name + "."





def changeProcedureName(procCurrentName, procNewName):
	if procNewName != checkStrValidity(procNewName):
		return "FAILED: Invalid characters detected."
	if procCurrentName == "":
		return "FAILED: No procedure selected."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM procedures WHERE procedures.proc_name='{procCurrentName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
		print("Rolling back...")

	data = cursor.fetchall()
	flag = 0
	for d in data:
		if d[5] == procCurrentName:
			flag = 1
			break

	if flag == 0:
		db.close()
		return "FAILED: No Procedure found."

	sql = f"UPDATE procedures SET procedures.proc_name='{procNewName}' WHERE procedures.proc_name='{procCurrentName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except pymysql.Error as e:
		db.rollback()
		if e.args[0] == 1062:
			return "FAILED: Duplicate procedure detected, cannot change name to " + procNewName
	db.close()
	return "SUCCESS: Procedure name changed to: " + procNewName

def changeSourcePath(procName, new_source):
	if procName != checkStrValidity(procName):
		return "FAILED: Invalid characters detected."
	if procName == "":
		return "FAILED: No procedure selected."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"UPDATE procedures SET procedures.src_path='{new_source}' WHERE procedures.proc_name='{procName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	db.close()
	return "SUCCESS: " + procName + " source changed to " + new_source + "."

def changeDestPath(procName, new_dest):
	if procName != checkStrValidity(procName):
		return "FAILED: Invalid characters detected."
	if procName == "":
		return "FAILED: No procedure selected."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"UPDATE procedures SET procedures.dest_path='{new_dest}' WHERE procedures.proc_name='{procName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	db.close()
	return "SUCCESS: " + procName + " destination changed to " + new_dest + "."

def changeProcOpCode(procName, new_op):
	if new_op not in possibleOpCodes:
		return "FAILED: Op code unresolved."
	if procName != checkStrValidity(procName):
		return "FAILED: Invalid characters detected."
	if procName == "":
		return "FAILED: No procedure selected."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"UPDATE procedures SET procedures.op_code={new_op} WHERE procedures.proc_name='{procName}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	db.close()
	return "SUCCESS: " + procName + " op-code changed to " + str(new_op) + "."


'''
'	showUser()
'
'	Returns and prints all users as a Collection object
'
'''

def showUsers():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM users"
	try:
		cursor.execute(sql)
	except pymysql.Error as e:
		db.rollback()
		print("Rolling back...")

	data = cursor.fetchall()
	db.close()

	for d in data:
		print("  Username: " + d[1] + ", Password: " + d[2])
	return data


'''
'
'	showCollection()
'
'	Returns and prints all collections as a Collection object
'
'''

def showCollections():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM collection"
	try:
		cursor.execute(sql)
	except pymysql.Error as e:
		db.rollback()
		print("Rolling back...")
	data = cursor.fetchall()
	db.close()

	for d in data:
		print("  Collection: " + d[1] + ", Owned by: " + d[2])
	return data

'''
'
'	showProcedure()
'
'	Shows all procedures in the database, regardless of user. Returns collection of procedures.
'
'''

def showProcedures():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM procedures"
	try:
		cursor.execute(sql)
	except:
		db.rollback()
		print("Rolling back...")
	data = cursor.fetchall()
	db.close()

	for d in data:
		print("  Procedure: " + d[5] + " in Collection: " + d[3])
	return data

'''
'
'	showCollectionsInUser(user)
'
'		user:
'			Collections will show for the given user
'
'''

def showCollectionsInUser(user):
	if user == "":
		return "No User specified..."

	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM users WHERE user_name = '{user}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	data = cursor.fetchall()

	flag = 0
	for d in data:
		if d[1] == user:
			flag = 1
			break;

	if flag == 0:
		db.close()
		return "FAILED: Username does not exist in database."

	sql = f"SELECT * FROM collection WHERE collection.collection_creator = '{user}'"
	try:
		cursor.execute(sql)
	except:
		db.rollback()
	data = cursor.fetchall()
	db.close()
	return data

'''
'
'	showProcInCollection(coll_name)
'
'		coll_name:
'			Name of collection to extract procedures from.
'
'''

def showProcInCollection(coll_name):
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM collection WHERE collection.collection_name='{coll_name}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	data = cursor.fetchall()

	flag = 0
	for d in data:
		if d[1] == coll_name:
			flag = 1
			break

	if flag == 0:
		db.close()
		return "FAILED: Collection does not exist in the database."
	
	sql = f"SELECT * FROM procedures WHERE procedures.member_of='{coll_name}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	data = cursor.fetchall()
	db.close()
	return data

def searchSourcePaths(search_term):
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM procedures WHERE procedures.src_path LIKE '{search_term}'"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	data = cursor.fetchall()
	db.close()
	if len(data) == 0:
		return "No results found."
	return data

def searchDestPaths(search_term):
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	sql = f"SELECT * FROM procedures WHERE procedures.dest_path LIKE '{search_term}'"
	try:
		cursor.execute(sql)
	except:
		db.rollback()
	data = cursor.fetchall()
	db.close()
	if len(data) == 0:
		return "No results found."
	return data

def tableExists(tableName, crsr):
	chkTablesSQL = """SHOW TABLES"""
	crsr.execute(chkTablesSQL)
	tables = crsr.fetchall()
	results_list = [item[0] for item in tables]

	if tableName in results_list:
		return True
	else:
		return False

def createUsersTable():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)
	
	if not tableExists('users', cursor):
		sql = f"CREATE TABLE IF NOT EXISTS users (user_id INT UNIQUE NOT NULL AUTO_INCREMENT, user_name VARCHAR(20) UNIQUE NOT NULL, pwd VARCHAR(20) NOT NULL, PRIMARY KEY(user_id))"
		try:
			cursor.execute(sql)
		except:
			db.rollback()
	db.close()

def createCollectionsTable():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	if not tableExists('collections', cursor):
		sql = f"CREATE TABLE IF NOT EXISTS collections (collection_id INT UNIQUE NOT NULL AUTO_INCREMENT, collection_name VARCHAR(40), collection_creator VARCHAR(40), PRIMARY KEY(collection_id), FOREIGN KEY(collection_creator) REFERENCES users(user_name) ON DELETE CASCADE)"
		try:
			cursor.execute(sql)
		except:
			db.rollback()
	db.close()

def createProceduresTable():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	if not tableExists('procedures', cursor):
		sql = f"CREATE TABLE IF NOT EXISTS procedures (procedure_id INT UNIQUE NOT NULL AUTO_INCREMENT, src_path VARCHAR(255), dest_path VARCHAR(255), member_of INT UNIQUE, op_code INT, proc_name VARCHAR(40), PRIMARY KEY(proc_num), FOREIGN KEY(member_of) REFERENCES collections(collection_id) ON DELETE CASCADE)"
		try:
			cursor.execute(sql)
		except:
			db.rollback()
	db.close()

def createDevicesTable():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	if not tableExists('devices', cursor):
		sql = f"CREATE TABLE IF NOT EXISTS devices (device_id INT UNIQUE NOT NULL AUTO_INCREMENT, device_name VARCHAR(40), device_user INT, PRIMARY KEY(device_id), FOREIGN KEY(device_user) REFERENCES users(user_id) ON DELETE CASCADE)"
		try:
			cursor.execute(sql)
		except:
			db.rollback()
	db.close()

def createDrivesTable():
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	if not tableExists('drives', cursor):
		sql = f"CREATE TABLE IF NOT EXISTS drives (drive_id INT UNIQUE NOT NULL AUTO_INCREMENT, drive_letter VARCHAR(2), drive_name VARCHAR(40), associated_device INT, PRIMARY KEY(drive_id), FOREIGN KEY(associated_device) REFERENCES devices(device_id) ON DELETE CASCADE)"
		try:
			cursor.execute(sql)
		except:
			db.rollback()
	db.close()

def createAllTables():
	createUsersTable()
	createCollectionsTable()
	createProceduresTable()
	createDevicesTable()
	createDrivesTable()

def dropForeignKeys(tableName):
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	fkey = tableName + '_ibfk_1'

	sql = f"ALTER TABLE {tableName} DROP FOREIGN KEY {fkey}"

	try:
		cursor.execute(sql)
	except:
		print("Rolling Back...")
		db.rollback()

	db.close()

def dropTable(tableName):
	db = openDatabaseConnection("localhost", "root", "j4q5x9D#1", "Backup")
	cursor = getDatabaseCursor(db)

	sql = f"DROP TABLE {tableName}"

	try:
		cursor.execute(sql)
	except:
		print("Rolling Back...")
		db.rollback()

	db.close()

def dropAllTables():
	dropForeignKeys('collections')
	dropForeignKeys('procedures')
	dropForeignKeys('devices')
	dropForeignKeys('drives')

	dropTable('drives')
	dropTable('devices')
	dropTable('procedures')
	dropTable('collections')
	dropTable('users')