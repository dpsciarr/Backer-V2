import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ModelObjects import User
from ModelObjects import Device
from ModelObjects import Drive
from ModelObjects import Collection
from ModelObjects import Procedure
from os import sep

DIALOG_BOX_SCREEN_SIZE = "350x150+500+200"
NO_SOURCE = 0
SOURCE_DATABASE = 1
SOURCE_DATABASE_NO_CFG = 2
SOURCE_CONFIG_NO_DB = 3

class ConfigurationFrame(tk.Frame):
	def __init__(self, parent, viewController):
		self.vc = viewController
		self.parent = parent
		self.tree = None
		self.currTreeItemID = None
		tk.Frame.__init__(self, parent, bg='WHITE', width=250)

		self.collectionsContextMenu = tk.Menu(self, tearoff=0)
		self.collectionsContextMenu.add_command(label="Add Collection", command=lambda : self.showDialog(AddCollectionWindow))

		self.collectionNameContextMenu = tk.Menu(self, tearoff=0)
		self.collectionNameContextMenu.add_command(label="Add Procedure", command=lambda : self.showDialog(AddProcedureWindow))
		self.collectionNameContextMenu.add_command(label="Select for Run Configuration", command = self.selectCollectionForRunConfig)
		self.collectionNameContextMenu.add_command(label="Deselect for Run Configuration", command = self.deselectCollectionForRunConfig)
		self.collectionNameContextMenu.add_command(label="Rename Collection", command=lambda : self.showDialog(RenameCollectionWindow))
		self.collectionNameContextMenu.add_command(label="Delete Collection", command=lambda : self.showDialog(DeleteCollectionWindow))

		self.procedureNameContextMenu = tk.Menu(self, tearoff=0)
		self.procedureNameContextMenu.add_command(label="Edit Procedure", command=lambda : self.showDialog(EditProcedureWindow))
		self.procedureNameContextMenu.add_command(label="Select for Run Configuration", command= self.selectProcForRunConfig)
		self.procedureNameContextMenu.add_command(label="Deselect for Run Configuration", command= self.deselectProcForRunConfig)
		self.procedureNameContextMenu.add_command(label="Delete Procedure", command=lambda : self.showDialog(DeleteProcedureWindow))

		self.devicesContextMenu = tk.Menu(self, tearoff=0)
		self.devicesContextMenu.add_command(label="Add Device", command=lambda : self.showDialog(AddDeviceWindow))

		self.deviceNameContextMenu = tk.Menu(self, tearoff=0)
		self.deviceNameContextMenu.add_command(label="Add Drive", command=lambda : self.showDialog(AddDriveWindow))
		self.deviceNameContextMenu.add_command(label="Rename Device", command=lambda : self.showDialog(RenameDeviceWindow))
		self.deviceNameContextMenu.add_command(label="Delete Device", command=lambda : self.showDialog(DeleteDeviceWindow))

		self.driveNameContextMenu = tk.Menu(self, tearoff=0)
		self.driveNameContextMenu.add_command(label="Edit Drive", command=lambda : self.showDialog(EditDriveWindow))
		self.driveNameContextMenu.add_command(label="Delete Drive", command=lambda : self.showDialog(DeleteDriveWindow))

	def buildTree(self, objModel):
		userObj = objModel.getCurrentUserObject()
		#print(userObj)
		self.tree = ttk.Treeview(self, selectmode='browse')

		self.tree.bind("<Button-3>", self.popupMenu)
		self.tree.bind('<<TreeviewSelect>>', self.tree_click_event)

		#self.tree.bind("<Double-1>", self.OnDoubleClick)
		self.tree.heading('#0', text='Configuration Tree')
		self.tree.insert("", "end", iid="user", text=f"User: {userObj.getName()}")

		self.tree.insert("user", "end", iid="devices", text="Devices")
		devDict = userObj.getDevices()
		for devKey in devDict:
			devID = devDict[devKey].getID()
			devName = devDict[devKey].getName()
			self.tree.insert("devices","end", text=f"Device: {devName}", iid=f"dev{devID}")

			drvDict = devDict[devKey].getDrives()
			for (key, val) in drvDict.items():
				drvID = val.getID()
				drvName = val.getName()
				self.tree.insert(f"dev{devID}", "end", text=f"Drive: {drvName}", iid=f"drv{drvID}")

		self.tree.insert("user", "end", iid="collections", text="Collections")
		collDict = userObj.getCollections()
		for collKey in collDict:
			collID = collDict[collKey].getID()
			collName = collDict[collKey].getName()
			self.tree.insert("collections", "end", text=f"Collection: {collName}", iid=f"coll{collID}")
			
			procDict = collDict[collKey].getProcedures()
			for (key, val) in procDict.items():
				procID = val.getID()
				procName = val.getName()
				self.tree.insert(f"coll{collID}", "end", text=f"Procedure: {procName}", iid=f"proc{procID}")

		self.tree.pack(fill = 'both', expand = True)

	def getTree(self):
		return self.tree

	def showDialog(self, func):
		t = func(self, self.vc)
		t.mainloop()

	def tree_click_event(self, event):
		self.currTreeItemID = self.tree.focus()

	'''
	popupMenu()

	Opens context menu. Vertical position is determined by event.y and the context menu to display is determined by the iid of the 
	treeview object.
	'''
	def popupMenu(self, event):
		#select row under mouse
		iid = self.tree.identify_row(event.y)
		if iid:
			self.tree.selection_set(iid)
			if "devices" in iid:
				self.devicesContextMenu.post(event.x_root, event.y_root)
			if "dev" in iid and iid != "devices":
				self.deviceNameContextMenu.post(event.x_root, event.y_root)
			if "drv" in iid:
				self.driveNameContextMenu.post(event.x_root, event.y_root)
			if "collections" in iid:
				self.collectionsContextMenu.post(event.x_root, event.y_root)
			if "coll" in iid and iid != "collections":
				self.collectionNameContextMenu.post(event.x_root, event.y_root)
			if "proc" in iid:
				self.procedureNameContextMenu.post(event.x_root, event.y_root)
		else:
			pass

	
	def selectCollectionForRunConfig(self):
		displayFrame = self.parent.getDisplayFrame()
		mc = self.vc.getView().getMainController().getModel().getController()
		userObj = mc.requestObjectManager().getCurrentUserObject()
		
		sel = self.getTree().selection()
		digits = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i

		if digits != "":
			collObjs = userObj.getCollections()
			collObjItems = [(item[0],item[1]) for item in collObjs.items()]
			for collection in collObjItems:
				collID = collection[1].getID()
				collName = collection[1].getName()
				if collID == int(digits):
					procs = collection[1].getProcedures()
					procObjItems = [(item[0],item[1]) for item in procs.items()]
					for proc in procObjItems:
						procObj = proc[1]
						procID = procObj.getID()
						newiid = "proc" + str(procID)
						if displayFrame.getIdleConfigTree().exists(newiid):
							selectedItemDict = displayFrame.getIdleConfigTree().item(newiid)
							displayFrame.getRunConfigTree().insert("", "end", iid=newiid, text=selectedItemDict['text'], values=selectedItemDict['values'])
							displayFrame.getIdleConfigTree().delete(newiid)
		
		#selects collection in current run configuration
		mc.runConfig_selectCollection(int(digits))

	def deselectCollectionForRunConfig(self):
		displayFrame = self.parent.getDisplayFrame()
		mc = self.vc.getView().getMainController().getModel().getController()
		userObj = mc.requestObjectManager().getCurrentUserObject()
		
		sel = self.getTree().selection()
		digits = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i

		if digits != "":
			collObjs = userObj.getCollections()
			collObjItems = [(item[0],item[1]) for item in collObjs.items()]
			for collection in collObjItems:
				collID = collection[1].getID()
				collName = collection[1].getName()
				if collID == int(digits):
					procs = collection[1].getProcedures()
					procObjItems = [(item[0],item[1]) for item in procs.items()]
					for proc in procObjItems:
						procObj = proc[1]
						procID = procObj.getID()
						newiid = "proc" + str(procID)
						if displayFrame.getRunConfigTree().exists(newiid):
							selectedItemDict = displayFrame.getRunConfigTree().item(newiid)
							displayFrame.getIdleConfigTree().insert("", "end", iid=newiid, text=selectedItemDict['text'], values=selectedItemDict['values'])
							displayFrame.getRunConfigTree().delete(newiid)
		
		
		#deselects collection from current run configuration
		mc.runConfig_deselectCollection(int(digits))

	def selectProcForRunConfig(self):
		displayFrame = self.parent.getDisplayFrame()
		mc = self.vc.getView().getMainController().getModel().getController()
		userObj = mc.requestObjectManager().getCurrentUserObject()
		
		procSel = self.getTree().selection()
		collDigits = ""
		procDigits = ""
		self.proc_iidFromTree = ""
		self.coll_iid = ""
		self.collObj = ""
		if len(procSel) > 0:
			self.proc_iidFromTree = procSel[0]
			for j in self.proc_iidFromTree:
				if j.isdigit():
					procDigits = procDigits + j
			self.coll_iid = self.getTree().parent(self.proc_iidFromTree)
			for i in self.coll_iid:
				if i.isdigit():
					collDigits = collDigits + i

		if procDigits != "":
			collObjs = userObj.getCollections()
			collObjItems = [(item[0],item[1]) for item in collObjs.items()]
			for collection in collObjItems:
				collID = collection[1].getID()
				procObjs = collection[1].getProcedures()
				procObjItems = [(item[0],item[1]) for item in procObjs.items()]

				for procedure in procObjItems:
					procID = procedure[0]
					procObj = procedure[1]
					if procID == int(procDigits):
						selectedItemDict = displayFrame.getIdleConfigTree().item(self.proc_iidFromTree)
						displayFrame.getRunConfigTree().insert("", "end", iid=self.proc_iidFromTree, text=selectedItemDict['text'], values=selectedItemDict['values'])
						displayFrame.getIdleConfigTree().delete(self.proc_iidFromTree)

		mc.runConfig_selectProcedure(int(procDigits), int(collDigits))



	def deselectProcForRunConfig(self):
		displayFrame = self.parent.getDisplayFrame()
		mc = self.vc.getView().getMainController().getModel().getController()
		userObj = mc.requestObjectManager().getCurrentUserObject()
		
		
		procSel = self.getTree().selection()
		collDigits = ""
		procDigits = ""
		self.proc_iidFromTree = ""
		self.coll_iid = ""
		self.collObj = ""
		if len(procSel) > 0:
			self.proc_iidFromTree = procSel[0]
			for j in self.proc_iidFromTree:
				if j.isdigit():
					procDigits = procDigits + j
			self.coll_iid = self.getTree().parent(self.proc_iidFromTree)
			for i in self.coll_iid:
				if i.isdigit():
					collDigits = collDigits + i

		if procDigits != "":
			collObjs = userObj.getCollections()
			collObjItems = [(item[0],item[1]) for item in collObjs.items()]
			for collection in collObjItems:
				collID = collection[1].getID()
				procObjs = collection[1].getProcedures()
				procObjItems = [(item[0],item[1]) for item in procObjs.items()]

				for procedure in procObjItems:
					procID = procedure[0]
					procObj = procedure[1]
					if procID == int(procDigits):
						selectedItemDict = displayFrame.getRunConfigTree().item(self.proc_iidFromTree)
						displayFrame.getIdleConfigTree().insert("", "end", iid=self.proc_iidFromTree, text=selectedItemDict['text'], values=selectedItemDict['values'])
						displayFrame.getRunConfigTree().delete(self.proc_iidFromTree)

		mc.runConfig_deselectProcedure(int(procDigits), int(collDigits))


class AddDeviceWindow(tk.Tk):
	def __init__(self, configFrame, viewController):
		self.vc = viewController
		self.cFrame = configFrame
		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Add Device")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')
		
		devNameLabel = tk.Label(f, text="Device Name: ", bg="white", fg="black")
		self.devNameEntry = tk.Entry(f, width=35, borderwidth=2)
		self.addDeviceButton = tk.Button(f, text="Add Device", height=2, width=10, command = lambda : self.addDevice())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		devNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.devNameEntry.place(x=110, y=20, relx=0, rely=0, anchor='nw')

		self.addDeviceButton.place(x=30, y = 80, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=80, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def addDevice(self):
		#get required variables
		newDeviceName = self.devNameEntry.get()
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()

		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to add Device {newDeviceName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:
			#look to see if device is already in the database for currentUser
			sql = f"SELECT device_name FROM devices WHERE device_user = {currUserID}"
			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			
			devExists = False
			if len(result) != 0:
				for each in result:
					if each[0] == newDeviceName:
						devExists = True
						self.vc.getView().getMainController().sendToOutput(f"   Device {newDeviceName} already exists in database for user {currUser}. Could not add device.")
			
			
			#add device to database
			if devExists == False:
				#add device to database
				sql1 = f"INSERT INTO devices(device_name, device_user) VALUES ('{newDeviceName}', {currUserID})"
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					self.vc.getView().getMainController().getModel().getController().queryDatabase(sql1, commitReq = True)
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				except Exception as e:
					print(e)

				#get the key number
				sql2 = f"SELECT device_id FROM devices WHERE device_name = '{newDeviceName}'"
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					devID = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql2)[0][0]
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
					print(devID)
					

					if devID is not None:
						#notify user that device was added to database
						self.vc.getView().getMainController().sendToOutput(f"   Device '{newDeviceName}' added to database.")

						#add device to object model
						usrObject = self.vc.getView().getMainController().getObjectManager().getCurrentUserObject()
						devObject = Device(id=devID, name=newDeviceName, user=currUserID)
						usrObject.addDevice(devObject)

						#notify user that device was added to object model
						self.vc.getView().getMainController().sendToOutput(f"   Device '{newDeviceName}' added to Object Model.")
						print("Device Object: " + str(usrObject.getDevice(devID)))

						#add device object to tree view
						self.cFrame.getTree().insert("devices", "end", iid=f"dev{devID}", text=f"Device: {newDeviceName}")
					
				except Exception as e:
					print(e)
					print("Failed to add device to database")			

		#add device to configuration file
		elif infoSrc == SOURCE_CONFIG_NO_DB:
			print("Config File sourcing")
			self.vc.getView().getMainController().sendToOutput(f"   Device '{newDeviceName}' cannot be added to configuration. Connect to database first.")

			#get the JSON string of the configuration file

			#find out if the device is already in the config file for that user using the device name

			#if it is already there, notify the user

			#if it is not, move on

			#add device to changeLogImport.cfg
				#build JSON tree description for where the device

		else:
			print("No source...")
			self.vc.getView().getMainController().sendToOutput(f"   Device '{newDeviceName}' cannot be added to configuration. Connect to database first.")

		self.winfo_toplevel().destroy()


	def kill(self):
		self.winfo_toplevel().destroy()

class AddCollectionWindow(tk.Tk):
	def __init__(self, configFrame, viewController):
		self.vc = viewController
		self.cFrame = configFrame
		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Add Collection")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')
		collNameLabel = tk.Label(f, text="Collection Name:", bg="white", fg="black")
		self.collNameEntry = tk.Entry(f, width=30, borderwidth=2)
		self.addCollectionButton = tk.Button(f, text="Add\nCollection", height=2, width=10, command = lambda : self.addCollection())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		collNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.collNameEntry.place(x=135, y=20, relx=0, rely=0, anchor='nw')

		self.addCollectionButton.place(x=30, y = 80, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=80, relx=0, rely=0, anchor='nw')


		f.pack(fill='both', expand=1)

	def addCollection(self):
		newCollectionName = self.collNameEntry.get()
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		
		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to add Collection {newCollectionName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:
			#look to see if collection is already in the database for currentUser
			sql = f"SELECT collection_name FROM collections WHERE collection_creator = '{currUser}'"
			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			
			collExists = False
			if len(result) != 0:
				for each in result:
					if each[0] == newCollectionName:
						collExists = True
						self.vc.getView().getMainController().sendToOutput(f"   Collection {newCollectionName} already exists in database for user {currUser}. Could not add collection.")
			
			#add collection to database
			if collExists == False:
				#add collection to database
				sql1 = f"INSERT INTO collections(collection_name, collection_creator) VALUES ('{newCollectionName}', '{currUser}')"
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					self.vc.getView().getMainController().getModel().getController().queryDatabase(sql1, commitReq = True)
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				except Exception as e:
					print(e)

				#get the key number
				sql2 = f"SELECT collection_id FROM collections WHERE collection_name = '{newCollectionName}'"
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					collID = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql2)[0][0]
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
					print(collID)
					
					if collID is not None:
						#notify user that collection was added to database
						self.vc.getView().getMainController().sendToOutput(f"   Collection '{newCollectionName}' added to database.")

						#add collection to object model
						usrObject = self.vc.getView().getMainController().getObjectManager().getCurrentUserObject()
						collObject = Collection(id=collID, name=newCollectionName, creator=currUser)
						usrObject.addCollection(collObject)

						#notify user that the collection was added to object model
						self.vc.getView().getMainController().sendToOutput(f"   Collection '{newCollectionName}' added to Object Model.")

						#add device object to tree view
						self.cFrame.getTree().insert("collections", "end", iid=f"coll{collID}", text=f"Collection: {newCollectionName}")
				
				except Exception as e:
					print(e)
					print("Failed to add collection to database.")

		elif infoSrc == SOURCE_CONFIG_NO_DB:
			print("Config File sourcing")
			self.vc.getView().getMainController().sendToOutput(f"   Collection '{newCollectionName}' cannot be added to configuration. Connect to database first.")

		else:
			print("No source...")
			self.vc.getView().getMainController().sendToOutput(f"   Collection '{newCollectionName}' cannot be added to configuration. Connect to database first.")

		self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()


class AddDriveWindow(tk.Tk):
	def __init__(self, configFrame, viewController):
		self.vc = viewController
		self.cFrame = configFrame

		#get object manager and dict of device objects owned by the current user
		objMan = self.vc.getView().getMainController().getObjectManager()
		deviceObjs = objMan.getCurrentUserObject().getDevices()

		#obtain a dict with key as the device ID and value as the device name
		devObjItems = [(item[0],item[1]) for item in deviceObjs.items()]
		devNames = []
		devIDs = []
		self.devDict = {}
		self.driveDictReversed = {}
		if len(devObjItems) > 0:
			for eachDevice in devObjItems:
				devItemName = eachDevice[1].getName()
				devItemID = eachDevice[1].getID()
				devNames.append(devItemName)
				devIDs.append(devItemID)
			self.devDict = dict(zip(devIDs, devNames))
			self.driveDictReversed = {v: k for k, v in self.devDict.items()}

		#get the selected drive's "iid" from treeview and map that to drive name
		sel = self.cFrame.getTree().selection()
		digits = ""
		selectedDevName = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			selectedDevName = self.devDict[int(digits)]

		driveLetters = [
			"A",
			"B",
			"C",
			"D",
			"E",
			"F",
			"G",
			"H",
			"I",
			"J",
			"K",
			"L",
			"M",
			"N",
			"O",
			"P",
			"Q",
			"R",
			"S",
			"T",
			"U",
			"V",
			"W",
			"X",
			"Y",
			"Z"
		]

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Add Drive")
		self.winfo_toplevel().geometry("350x180+500+200")
		f = tk.Frame(self, bg='white')

		drvNameLabel = tk.Label(f, text="Drive Name:", bg="white", fg="black")
		drvLetterLabel = tk.Label(f, text="Drive Letter:", bg="white", fg="black")
		drvAssociatedDeviceLabel = tk.Label(f, text="Parent Device:", bg="white", fg="black")
		self.drvNameEntry = tk.Entry(f, width=30, borderwidth=2)

		self.drvLetterList = ttk.Combobox(f, values = driveLetters, state='readonly')
		self.drvLetterList.set(driveLetters[0])

		self.devList = ttk.Combobox(f, values = devNames, state='readonly')
		if selectedDevName in devNames:
			self.devList.set(selectedDevName)
		else:
			self.devList.set(devNames[0])

		self.addDriveButton = tk.Button(f, text="Add Drive", height=2, width=10, command = lambda : self.addDrive())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		drvNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.drvNameEntry.place(x=135, y=20, relx=0, rely=0, anchor='nw')
		drvLetterLabel.place(x=30, y=50, relx=0, rely=0, anchor='nw')
		self.drvLetterList.place(x=135, y = 50, relx=0, rely=0, anchor='nw')
		drvAssociatedDeviceLabel.place(x=30, y=80, relx=0, rely=0, anchor='nw')
		self.devList.place(x=135, y=80, relx=0, rely=0, anchor='nw')

		self.addDriveButton.place(x=30, y = 115, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=115, relx=0, rely=0, anchor='nw')

		self.drvLetterList.config(width=10)
		self.devList.config(width = 30)
		f.pack(fill='both', expand=1)

	def addDrive(self):
		newDriveName = self.drvNameEntry.get()
		newDriveLetter = self.drvLetterList.get()
		associatedDeviceName = self.devList.get()
		associatedDeviceID = self.driveDictReversed[associatedDeviceName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()

		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to add Drive {newDriveName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:
			#look to see if drive is already in the database for currentUser and parent device

			sql = f"SELECT drive_name FROM drives WHERE associated_device = {associatedDeviceID}"
			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()

			drvExists = False
			if len(result) != 0:
				for each in result:
					if each[0] == newDriveName:
						drvExists = True
						self.vc.getView().getMainController().sendToOutput(f"   Drive {newDriveName} already exists in database for user {currUser}. Could not add drive.")

			#add drive to database
			if drvExists == False:
				#add drive to database
				sql1 = f"INSERT INTO drives(drive_letter, drive_name, associated_device) VALUES ('{newDriveLetter}', '{newDriveName}', {associatedDeviceID})"
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					self.vc.getView().getMainController().getModel().getController().queryDatabase(sql1, commitReq = True)
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				except Exception as e:
					print(e)

				#get the resulting key number
				sql2 = f"SELECT drive_id FROM drives WHERE drive_name = '{newDriveName}' AND associated_device = {associatedDeviceID}"
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					drvID = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql2)[0][0]
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				
					if drvID is not None:
						#notify user that drive was added to database
						self.vc.getView().getMainController().sendToOutput(f"   Drive '{newDriveName}' added to database.")

						#add drive to object model
						usrObject = self.vc.getView().getMainController().getObjectManager().getCurrentUserObject()
						drvObject = Drive(id=drvID, letter=newDriveLetter, name=newDriveName, device=associatedDeviceID)
						devObject = usrObject.getDevice(associatedDeviceID)
						devObject.addDrive(drvObject)

						#notify user that the drive was added to object model
						self.vc.getView().getMainController().sendToOutput(f"   Drive '{newDriveName}' added to Object Model.")

						#add device object to tree view
						self.cFrame.getTree().insert(self.iidFromTree, "end", iid=f"drv{drvID}", text=f"Drive: {newDriveName}")
				except Exception as e:
					self.vc.getView().getMainController().sendToOutput(f"   Error: {e} Failed to add drive to database.")

		elif infoSrc == SOURCE_CONFIG_NO_DB:
			print("Config File sourcing")
			self.vc.getView().getMainController().sendToOutput(f"   Drive '{newDriveName}' cannot be added to configuration. Connect to database first.")
		
		else:
			print("No source...")
			self.vc.getView().getMainController().sendToOutput(f"   Drive '{newDriveName}' cannot be added to configuration. Connect to database first.")

		self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()



class AddProcedureWindow(tk.Tk):
	def __init__(self, configFrame, viewController):
		self.vc = viewController
		self.cFrame = configFrame
		self.displayFrame = self.cFrame.parent.getDisplayFrame()

		self.procOpDictionary = self.vc.getView().getMainController().getAvailableProceduresNumToStr()
		self.procOpDictionaryStrToNum = self.vc.getView().getMainController().getAvailableProceduresStrToNum()
		operations = []
		for i in range(14):#len(self.procOpDictionary)):
			operations.append(self.procOpDictionary[i])

		#get object manager and dict of collection objects owned by user
		objMan = self.vc.getView().getMainController().getObjectManager()
		collectionObjs = objMan.getCurrentUserObject().getCollections()

		#obtain a dict with key as the device ID and value as the device name
		collObjItems = [(item[0],item[1]) for item in collectionObjs.items()]
		collNames = []
		collIDs = []
		self.collDict = {}
		self.collDictReversed ={}
		if len(collObjItems) > 0:
			for eachCollection in collObjItems:
				collItemName = eachCollection[1].getName()
				collItemID = eachCollection[1].getID()
				collNames.append(collItemName)
				collIDs.append(collItemID)
			self.collDict = dict(zip(collIDs, collNames))
			self.collDictReversed = {v: k for k, v in self.collDict.items()}

		#get the selected collection's "iid" from treeview and map that to drive name
		sel = self.cFrame.getTree().selection()
		digits = ""
		selectedCollName = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			selectedCollName = self.collDict[int(digits)]


		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Add Procedure")
		self.winfo_toplevel().geometry("600x250+400+200")
		f = tk.Frame(self, bg='white')


		procNameLabel = tk.Label(f, text="Procedure Name:", bg="white", fg="black")
		procOpLabel = tk.Label(f, text="Operation:", bg='white', fg='black')
		procSourceLabel = tk.Label(f, text="Source:", bg='white', fg='black')
		procDestLabel = tk.Label(f, text="Destination:", bg='white', fg='black')
		procAssociatedCollectionLabel = tk.Label(f, text="Parent Collection:", bg="white", fg="black")
		procAppendLabel = tk.Label(f, text="Suffix:", bg='white', fg='black')
		self.procNameEntry = tk.Entry(f, width=30, borderwidth=2)
		self.procSourceEntry = tk.Entry(f, width=70, borderwidth=2)
		self.procDestEntry = tk.Entry(f, width=70, borderwidth=2)


		self.opsListBox = ttk.Combobox(f, values = operations, state='readonly')
		self.opsListBox.set(operations[0])


		self.collList = ttk.Combobox(f, values = collNames, state='readonly')
		if selectedCollName in collNames:
			self.collList.set(selectedCollName)
		else:
			self.collList.set(collNames[0])


		self.multiFileValues = ["Basic", "Date", "Date-Time", "Time-Stamp"]
		self.singleFileValues = ["Basic", "Date", "Date-Time", "Time-Stamp", "Revision"]
		self.appendageList = ttk.Combobox(f, values = self.multiFileValues, state = 'readonly')
		self.appendageList.set(self.multiFileValues[0])


		self.addProcedureButton = tk.Button(f, text="Add\nProcedure", height=2, width=10, command = lambda : self.addProcedure())
		self.sourceFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openSrcBrowser(self.opsListBox.get(), self.procSourceEntry))
		self.destFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openDestBrowser(self.opsListBox.get(), self.procDestEntry))
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)


		procNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		procOpLabel.place(x=30, y=55, relx=0, rely=0, anchor='nw')
		procSourceLabel.place(x=30, y=90, relx=0, rely=0, anchor='nw')
		procDestLabel.place(x=30, y=125, relx=0, rely=0, anchor='nw')
		procAssociatedCollectionLabel.place(x=30, y = 160, relx = 0, rely = 0, anchor='nw')
		self.procNameEntry.place(x=135, y=20, relx=0, rely=0, anchor='nw')
		self.opsListBox.place(x=135, y=55, relx=0, rely=0, anchor='nw')
		self.opsListBox.config(width=30)
		procAppendLabel.place(x=390, y=55, relx=0,rely=0,anchor='nw')
		self.appendageList.place(x=440, y = 55, relx = 0, rely = 0, anchor='nw')
		self.appendageList.config(width=15)
		self.procSourceEntry.place(x=135, y=90, relx=0, rely=0, anchor='nw')
		self.procDestEntry.place(x=135, y=125, relx=0, rely=0, anchor='nw')
		self.collList.place(x=135, y=160, relx=0, rely=0, anchor='nw')


		self.sourceFileBrowserButton.place(x=555, y=88, relx=0, rely=0, anchor='nw')
		self.destFileBrowserButton.place(x=555, y=123, relx=0, rely=0, anchor='nw')
		self.addProcedureButton.place(x=160, y=200, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=360, y=200, relx=0, rely=0, anchor='nw')


		self.opsListBox.bind('<<ComboboxSelected>>', self.callback)
		self.collList.config(width = 50)
		f.pack(fill='both', expand=1)

	def openSrcBrowser(self, operation, entrybox):
		directoryName = ""
		if "Single File" in operation:
			directoryName = filedialog.askopenfilename(initialdir="/", title="Select File")
		else:
			directoryName = filedialog.askdirectory(initialdir="/", title="Select Folder")
		entrybox.delete(0, 'end')
		entrybox.insert(0, directoryName)

	def openDestBrowser(self, operation, entrybox):
		directoryName = filedialog.askdirectory(initialdir="/", title = "Select Folder")
		entrybox.delete(0, 'end')
		entrybox.insert(0, directoryName)

	def callback(self, event):
		currOpSelected = self.opsListBox.get()

		if "Single File" in currOpSelected and "Overwrite" not in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.singleFileValues)
			self.appendageList.set(self.singleFileValues[0])
		elif "File Copy New" in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])
		elif "File Migrate New" in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])
		elif "Folder Copy New" in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])
		else:
			self.appendageList.config(state='disabled')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])


	def addProcedure(self):
		newProcedureName = self.procNameEntry.get()
		newProcedureOpCode = self.opsListBox.get()

		statedAppendage = self.appendageList.get()
		statedOpCode = self.opsListBox.get()
		if (self.appendageList.state()[0] == 'readonly' or self.appendageList.state()[0] == 'focus') and statedAppendage != "Basic":
			statedOpCode = statedOpCode + " (" + str(statedAppendage) + ")"
			newProcedureOpCode = statedOpCode

		procOpCodeID = self.procOpDictionaryStrToNum[newProcedureOpCode]
		newProcedureSrc = self.procSourceEntry.get()
		newProcedureSrc = newProcedureSrc.replace(sep, '/')
		newProcedureDest = self.procDestEntry.get()
		newProcedureDest = newProcedureDest.replace(sep, '/')
		associatedCollName = self.collList.get()
		associatedCollectionID = self.collDictReversed[associatedCollName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		

		displayFrame = self.cFrame.parent.getDisplayFrame()
		mc = self.vc.getView().getMainController().getModel().getController()
		userObj = mc.requestObjectManager().getCurrentUserObject()
		

		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to add Procedure {newProcedureName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:

			sql = f"SELECT proc_name FROM procedures WHERE member_of = {associatedCollectionID}"
			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()

			procExists = False
			if len(result) != 0:
				for each in result:
					if each[0] == newProcedureName:
						procExists = True
						self.vc.getView().getMainController().sendToOutput(f"   Procedure {newProcedureName} already exists in database for user {currUser}. Could not add procedure.")

			if procExists == False:
				#add procedure to database
				sql1 = f"""INSERT INTO procedures(src_path, dest_path, member_of, op_code, proc_name) VALUES ('{newProcedureSrc}', '{newProcedureDest}', {associatedCollectionID}, {procOpCodeID}, '{newProcedureName}')"""
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					self.vc.getView().getMainController().getModel().getController().queryDatabase(sql1, commitReq = True)
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				except Exception as e:
					print(e)

				#get the resulting key number
				sql2 = f"SELECT proc_num FROM procedures WHERE proc_name = '{newProcedureName}' AND member_of = {associatedCollectionID}"
				try:
					self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
					procID = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql2)[0][0]
					self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				
					if procID is not None:
						#notify user that procedure was added to database
						self.vc.getView().getMainController().sendToOutput(f"   Procedure '{newProcedureName}' added to database.")

						#add procedure to object model
						usrObject = self.vc.getView().getMainController().getObjectManager().getCurrentUserObject()
						procObject = Procedure(id=procID, name=newProcedureName, src=newProcedureSrc, dest=newProcedureDest, collection=associatedCollectionID, operation=procOpCodeID)
						collObject = usrObject.getCollection(associatedCollectionID)
						collObject.addProcedure(procObject)

						#add procedure to current run configuration dictionary in Config Manager
						cfgMan = self.vc.getView().getMainController().getConfigurationManager()
						cfgMan.addProcToRunConfig(procID)

						#notify user that the procedure was added to object model
						self.vc.getView().getMainController().sendToOutput(f"   Procedure '{newProcedureName}' added to Object Model.")

						newiid = "proc" + str(procID)
						displayFrame.getIdleConfigTree().insert("", "end", iid=newiid, values=[f"{collObject.getName()}", f"{newProcedureName}"])

						#add procedure object to tree view
						self.cFrame.getTree().insert(self.iidFromTree, "end", iid=f"proc{procID}", text=f"Procedure: {newProcedureName}")
				except Exception as e:
					self.vc.getView().getMainController().sendToOutput(f"   Error: {e} Failed to add procedure to database.")


			elif infoSrc == SOURCE_CONFIG_NO_DB:
				print("Config File sourcing")
				self.vc.getView().getMainController().sendToOutput(f"   Procedure '{newProcedureName}' cannot be added to configuration. Connect to database first.")
			
			else:
				print("No source...")
				self.vc.getView().getMainController().sendToOutput(f"   Procedure '{newProcedureName}' cannot be added to configuration. Connect to database first.")




			self.winfo_toplevel().destroy()
		

	def kill(self):
		self.winfo_toplevel().destroy()


class DeleteDeviceWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame
		
		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()
		devObjs = self.userObj.getDevices()

		devObjItems = [(item[0],item[1]) for item in devObjs.items()]
		devNames = []
		devIDs = []
		self.devDict = {}
		self.devDictReversed = {}
		if len(devObjItems) > 0:
			for eachDevice in devObjItems:
				devItemName = eachDevice[1].getName()
				devItemID = eachDevice[1].getID()
				devNames.append(devItemName)
				devIDs.append(devItemID)
			self.devDict = dict(zip(devIDs, devNames))
			self.devDictReversed = {v: k for k, v in self.devDict.items()}

		sel = self.cFrame.getTree().selection()
		digits = ""
		self.selectedDevName = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			self.selectedDevName = self.devDict[int(digits)]


		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Device")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')

		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedDevName}?", bg="white", fg="black")
		self.deleteDevButton = tk.Button(f, text="Delete Device", height=2, width=10, command = lambda : self.deleteDevice())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteDevButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def deleteDevice(self):
		deviceID = self.devDictReversed[self.selectedDevName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		
		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to delete Device {self.selectedDevName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:

			#remove from database
			sql = f"DELETE FROM devices WHERE device_id = '{deviceID}'"
			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			self.vc.getView().getMainController().sendToOutput(f"   Deleted device '{self.selectedDevName}' from database.")
						
			#remove from object model
			self.userObj.removeDevice(deviceID)
			try:
				self.userObj.getDevice(deviceID, justChecking = True)
				self.vc.getView().getMainController().sendToOutput(f"   Device '{self.selectedDevName}' not deleted from object model.")
			except KeyError:
				self.vc.getView().getMainController().sendToOutput(f"   Deleted device '{self.selectedDevName}' from object model.")
				self.cFrame.getTree().delete(self.iidFromTree)

			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()

class DeleteCollectionWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame

		self.displayFrame = self.cFrame.parent.getDisplayFrame()

		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()
		collObjs = self.userObj.getCollections()

		collObjItems = [(item[0],item[1]) for item in collObjs.items()]
		collNames = []
		collIDs = []
		self.collDict = {}
		self.collDictReversed = {}
		if len(collObjItems) > 0:
			for eachCollection in collObjItems:
				collItemName = eachCollection[1].getName()
				collItemID = eachCollection[1].getID()
				collNames.append(collItemName)
				collIDs.append(collItemID)
			self.collDict = dict(zip(collIDs, collNames))
			self.collDictReversed = {v: k for k, v in self.collDict.items()}

		sel = self.cFrame.getTree().selection()
		digits = ""
		self.selectedCollName = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			self.selectedCollName = self.collDict[int(digits)]

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Collection")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')

		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedCollName}?", bg="white", fg="black")
		self.deleteCollButton = tk.Button(f, text="Delete\nCollection", height=2, width=10, command = lambda : self.deleteCollection())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteCollButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def deleteCollection(self):
		collectionID = self.collDictReversed[self.selectedCollName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		collObj = self.userObj.getCollection(int(collectionID))
		procObjs = collObj.getProcedures()
		procObjItems = [(item[0],item[1]) for item in procObjs.items()]
		

		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to delete Collection {self.selectedCollName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:

			#remove from database
			sql = f"DELETE FROM collections WHERE collection_id = '{collectionID}'"

			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			self.vc.getView().getMainController().sendToOutput(f"   Deleted collection '{self.selectedCollName}' from database.")

			#remove from object model
			self.userObj.removeCollection(collectionID)
			try:
				self.userObj.getCollection(collectionID, justChecking = True)
				self.vc.getView().getMainController().sendToOutput(f"   Collection '{self.selectedCollName}' not deleted from object model.")
			except KeyError:
				self.vc.getView().getMainController().sendToOutput(f"   Deleted collection '{self.selectedCollName}' from object model.")
				self.cFrame.getTree().delete(self.iidFromTree)

			displayFrame = self.cFrame.parent.getDisplayFrame()
			for eachProcObj in procObjItems:
				print(eachProcObj[1].getName())
				procName = eachProcObj[1].getName()
				procID = eachProcObj[1].getID()
				procStr = "proc" + str(procID)

				if displayFrame.getIdleConfigTree().exists(procStr):
					displayFrame.getIdleConfigTree().delete(procStr)
				elif displayFrame.getRunConfigTree().exists(procStr):
					displayFrame.getRunConfigTree().delete(procStr)

			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()

class DeleteDriveWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame

		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()

		drvSel = self.cFrame.getTree().selection()
		devDigits = ""
		drvDigits = ""
		self.selectedDrvName = ""
		self.drv_iidFromTree = ""
		self.dev_iid = ""
		self.devObj = ""
		if len(drvSel) > 0:
			self.drv_iidFromTree = drvSel[0]
			for j in self.drv_iidFromTree:
				if j.isdigit():
					drvDigits = drvDigits + j

			self.dev_iid = self.cFrame.getTree().parent(self.drv_iidFromTree)
			for i in self.dev_iid:
				if i.isdigit():
					devDigits = devDigits + i
			self.devObj = self.userObj.getDevice(int(devDigits))
			drvObj = self.devObj.getDrive(int(drvDigits))
			self.selectedDrvName = drvObj.getName()

		drvObjs = self.devObj.getDrives()
		drvObjItems = [(item[0],item[1]) for item in drvObjs.items()]
		drvNames = []
		drvIDs = []
		self.drvDict = {}
		self.drvDictReversed = {}
		if len(drvObjItems) > 0:
			for eachDrive in drvObjItems:
				drvItemName = eachDrive[1].getName()
				drvItemID = eachDrive[1].getID()
				drvNames.append(drvItemName)
				drvIDs.append(drvItemID)
			self.drvDict = dict(zip(drvIDs, drvNames))
			self.drvDictReversed = {v: k for k, v in self.drvDict.items()}

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Drive")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')

		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedDrvName}?", bg="white", fg="black")
		self.deleteDrvButton = tk.Button(f, text="Delete Drive", height=2, width=10, command = lambda : self.deleteDrive())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteDrvButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def deleteDrive(self):
		driveID = self.drvDictReversed[self.selectedDrvName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		
		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to delete Drive {self.selectedDrvName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:

			#remove from database
			sql = f"DELETE FROM drives WHERE drive_id = '{driveID}'"
			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			self.vc.getView().getMainController().sendToOutput(f"   Deleted drive '{self.selectedDrvName}' from database.")

			#remove from object model
			self.devObj.removeDrive(driveID)
			try:
				self.devObj.getDrive(driveID, justChecking = True)
				self.vc.getView().getMainController().sendToOutput(f"   Drive '{self.selectedDrvName}' not deleted from object model.")
			except KeyError:
				self.vc.getView().getMainController().sendToOutput(f"   Deleted drive '{self.selectedDrvName}' from object model.")
				self.cFrame.getTree().delete(self.drv_iidFromTree)

			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()

class DeleteProcedureWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame

		self.displayFrame = self.cFrame.parent.getDisplayFrame()

		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()

		procSel = self.cFrame.getTree().selection()
		collDigits = ""
		procDigits = ""
		self.selectedProcName = ""
		self.proc_iidFromTree = ""
		self.coll_iid = ""
		self.collObj = ""
		if len(procSel) > 0:
			self.proc_iidFromTree = procSel[0]
			for j in self.proc_iidFromTree:
				if j.isdigit():
					procDigits = procDigits + j

			self.coll_iid = self.cFrame.getTree().parent(self.proc_iidFromTree)
			for i in self.coll_iid:
				if i.isdigit():
					collDigits = collDigits + i
			self.collObj = self.userObj.getCollection(int(collDigits))
			procObj = self.collObj.getProcedure(int(procDigits))
			self.selectedProcName = procObj.getName()

		procObjs = self.collObj.getProcedures()
		procObjItems = [(item[0],item[1]) for item in procObjs.items()]
		procNames = []
		procIDs = []
		self.procDict = {}
		self.procDictReversed = {}
		if len(procObjItems) > 0:
			for eachProcedure in procObjItems:
				procItemName = eachProcedure[1].getName()
				procItemID = eachProcedure[1].getID()
				procNames.append(procItemName)
				procIDs.append(procItemID)
			self.procDict = dict(zip(procIDs, procNames))
			self.procDictReversed = {v: k for k, v in self.procDict.items()}

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Procedure")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')


		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedProcName}?", bg="white", fg="black")
		self.deleteProcButton = tk.Button(f, text="Delete\nProcedure", height=2, width=10, command = lambda : self.deleteProcedure())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteProcButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def deleteProcedure(self):
		procID = self.procDictReversed[self.selectedProcName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		
		displayFrame = self.cFrame.parent.getDisplayFrame()
		mc = self.vc.getView().getMainController().getModel().getController()
		userObj = mc.requestObjectManager().getCurrentUserObject()
		

		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to delete Procedure {self.selectedProcName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:

			#remove from database
			sql = f"DELETE FROM procedures WHERE proc_num = '{procID}'"
			self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
			result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			self.vc.getView().getMainController().sendToOutput(f"   Deleted procedure '{self.selectedProcName}' from database.")

			#remove from object model
			self.collObj.removeProcedure(procID)
			try:
				self.collObj.getProcedure(procID, justChecking = True)
				self.vc.getView().getMainController().sendToOutput(f"   Procedure '{self.selectedProcName}' not deleted from object model.")
			except KeyError:
				self.vc.getView().getMainController().sendToOutput(f"   Deleted procedure '{self.selectedProcName}' from object model.")
				
				if displayFrame.getIdleConfigTree().exists(self.proc_iidFromTree):
					displayFrame.getIdleConfigTree().delete(self.proc_iidFromTree)
				elif displayFrame.getRunConfigTree().exists(self.proc_iidFromTree):
					displayFrame.getRunConfigTree().delete(self.proc_iidFromTree)

				self.cFrame.getTree().delete(self.proc_iidFromTree)

			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()

class RenameDeviceWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame

		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()
		devObjs = self.userObj.getDevices()

		devObjItems = [(item[0],item[1]) for item in devObjs.items()]
		devNames = []
		devIDs = []
		self.devDict = {}
		self.devDictReversed = {}
		if len(devObjItems) > 0:
			for eachDevice in devObjItems:
				devItemName = eachDevice[1].getName()
				devItemID = eachDevice[1].getID()
				devNames.append(devItemName)
				devIDs.append(devItemID)
			self.devDict = dict(zip(devIDs, devNames))
			self.devDictReversed = {v: k for k, v in self.devDict.items()}
		
		sel = self.cFrame.getTree().selection()
		digits = ""
		self.selectedDevName = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			self.selectedDevName = self.devDict[int(digits)]

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Rename Device")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')

		self.renameDevLabel = tk.Label(f, bg='white', text=f"Rename device '{self.selectedDevName}' to:")
		self.renameDevEntry = tk.Entry(f, width = 28, borderwidth = 2)
		self.renameDevButton = tk.Button(f, text="Rename\nDevice", height=2, width=10, command = lambda : self.renameDevice())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		self.renameDevLabel.place(x=10, y=20, relx=0, rely=0, anchor='nw')
		self.renameDevEntry.place(x=160, y=20, relx=0, rely=0, anchor='nw')
		self.renameDevButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def renameDevice(self):
		deviceID = self.devDictReversed[self.selectedDevName]
		newDeviceName = self.renameDevEntry.get()
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		
		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:
			self.vc.getView().getMainController().sendToOutput(f"Renaming device '{self.selectedDevName}'...")
			
			sql = f"UPDATE devices SET device_name = '{newDeviceName}' WHERE device_id = {deviceID}"
			try:
				self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
				result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
			except Exception as e:
				print(e)

			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			self.vc.getView().getMainController().sendToOutput(f"   Renamed device '{self.selectedDevName}' to '{newDeviceName}' in database.")
		
			#rename in object model
			devObj = self.userObj.getDevice(deviceID)
			print(devObj)
			devObj.setName(newDeviceName)
			print(devObj.getName())
			self.vc.getView().getMainController().sendToOutput(f"   Renamed device '{self.selectedDevName}' to '{newDeviceName}' in object model.")
			
			#rename the device in the tree
			st = "Device: " + newDeviceName
			self.cFrame.getTree().item(self.iidFromTree, text = st)
			
			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()



class RenameCollectionWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame

		self.displayFrame = self.cFrame.parent.getDisplayFrame()

		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()
		collObjs = self.userObj.getCollections()

		collObjItems = [(item[0],item[1]) for item in collObjs.items()]
		collNames = []
		collIDs = []
		self.collDict = {}
		self.collDictReversed = {}
		if len(collObjItems) > 0:
			for eachCollection in collObjItems:
				collItemName = eachCollection[1].getName()
				collItemID = eachCollection[1].getID()
				collNames.append(collItemName)
				collIDs.append(collItemID)
			self.collDict = dict(zip(collIDs, collNames))
			self.collDictReversed = {v: k for k, v in self.collDict.items()}
		
		sel = self.cFrame.getTree().selection()
		digits = ""
		self.selectedCollName = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			self.selectedCollName = self.collDict[int(digits)]

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Rename Collection")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')

		self.renameCollLabel = tk.Label(f, bg='white', text=f"Rename collection '{self.selectedCollName}' to:")
		self.renameCollEntry = tk.Entry(f, width = 40, borderwidth = 2)
		self.renameCollButton = tk.Button(f, text="Rename\nCollection", height=2, width=10, command = lambda : self.renameCollection())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		self.renameCollLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.renameCollEntry.place(x=30, y=50, relx=0, rely=0, anchor='nw')
		self.renameCollButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def renameCollection(self):
		collID = self.collDictReversed[self.selectedCollName]
		newCollectionName = self.renameCollEntry.get()
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		collObj = self.userObj.getCollection(int(collID))
		procObjs = collObj.getProcedures()
		procObjItems = [(item[0],item[1]) for item in procObjs.items()]
		

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:
			self.vc.getView().getMainController().sendToOutput(f"Renaming collection '{self.selectedCollName}'...")
			
			sql = f"UPDATE collections SET collection_name = '{newCollectionName}' WHERE collection_id = {collID}"
			try:
				self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
				result = self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
			except Exception as e:
				print(e)

			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			self.vc.getView().getMainController().sendToOutput(f"   Renamed collection '{self.selectedCollName}' to '{newCollectionName}' in database.")
		
			#rename in object model
			collObj = self.userObj.getCollection(collID)
			collObj.setName(newCollectionName)
			self.vc.getView().getMainController().sendToOutput(f"   Renamed collection '{self.selectedCollName}' to '{newCollectionName}' in object model.")
			
			#rename the device in the tree
			st = "Collection: " + newCollectionName
			self.cFrame.getTree().item(self.iidFromTree, text = st)

			displayFrame = self.cFrame.parent.getDisplayFrame()
			for eachProcObj in procObjItems:
				procName = eachProcObj[1].getName()
				procID = eachProcObj[1].getID()
				procStr = "proc" + str(procID)

				if displayFrame.getIdleConfigTree().exists(procStr):
					displayFrame.getIdleConfigTree().item(procStr, values=[newCollectionName, procName])
				elif displayFrame.getRunConfigTree().exists(procStr):
					displayFrame.getRunConfigTree().item(procStr, values=[newCollectionName, procName])
				

			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()



class EditDriveWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame

		driveLetters = [
			"A",
			"B",
			"C",
			"D",
			"E",
			"F",
			"G",
			"H",
			"I",
			"J",
			"K",
			"L",
			"M",
			"N",
			"O",
			"P",
			"Q",
			"R",
			"S",
			"T",
			"U",
			"V",
			"W",
			"X",
			"Y",
			"Z"
		]

		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()

		drvSel = self.cFrame.getTree().selection()
		devDigits = ""
		drvDigits = ""
		self.selectedDrvName = ""
		self.drv_iidFromTree = ""
		self.dev_iid = ""
		self.devObj = ""
		if len(drvSel) > 0:
			self.drv_iidFromTree = drvSel[0]
			for j in self.drv_iidFromTree:
				if j.isdigit():
					drvDigits = drvDigits + j

			self.dev_iid = self.cFrame.getTree().parent(self.drv_iidFromTree)
			for i in self.dev_iid:
				if i.isdigit():
					devDigits = devDigits + i
			self.devObj = self.userObj.getDevice(int(devDigits))
			self.drvObj = self.devObj.getDrive(int(drvDigits))
			self.selectedDrvName = self.drvObj.getName()

		drvObjs = self.devObj.getDrives()
		drvObjItems = [(item[0],item[1]) for item in drvObjs.items()]
		drvNames = []
		drvIDs = []
		self.drvDict = {}
		self.drvDictReversed = {}
		if len(drvObjItems) > 0:
			for eachDrive in drvObjItems:
				drvItemName = eachDrive[1].getName()
				drvItemID = eachDrive[1].getID()
				drvNames.append(drvItemName)
				drvIDs.append(drvItemID)
			self.drvDict = dict(zip(drvIDs, drvNames))
			self.drvDictReversed = {v: k for k, v in self.drvDict.items()}

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Edit Drive")
		self.winfo_toplevel().geometry(DIALOG_BOX_SCREEN_SIZE)
		f = tk.Frame(self, bg='white')

		self.drvNameLabel = tk.Label(f, bg='white', text="Name:")
		self.drvNameEntry = tk.Entry(f, width = 28, borderwidth = 2)
		self.drvNameEntry.insert(0, self.drvObj.getName())
		self.drvLetterLabel = tk.Label(f, bg='white', text="Letter:")
		self.drvLetterList = ttk.Combobox(f, values = driveLetters, state='readonly')
		self.drvLetterList.set(self.drvObj.getDriveLetter())
		self.editDriveButton = tk.Button(f, text="Edit Drive", height=2, width=10, command = lambda : self.editDrive())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		self.drvNameLabel.place(x = 30, y = 10, relx=0, rely=0, anchor='nw')
		self.drvNameEntry.place(x = 75, y = 10, relx=0, rely=0, anchor='nw')
		self.drvLetterLabel.place(x=30, y = 45, relx=0, rely=0, anchor='nw')
		self.drvLetterList.place(x = 75, y = 45, relx=0, rely=0, anchor='nw')
		self.editDriveButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		self.drvLetterList.config(width=10)
		f.pack(fill='both', expand=1)

	def editDrive(self):
		driveID = self.drvDictReversed[self.selectedDrvName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()
		
		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to edit Drive {self.selectedDrvName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:
			#compare drive letter and drive name with what's in the object model
			currDrvName = self.drvObj.getName()
			currDrvLetter = self.drvObj.getDriveLetter()

			enteredDrvName = self.drvNameEntry.get()
			enteredDrvLetter = self.drvLetterList.get()

			drvLetterToSave = currDrvLetter
			letterChanged = False
			if currDrvLetter != enteredDrvLetter:
				drvLetterToSave = enteredDrvLetter
				letterChanged = True

			drvNameToSave = currDrvName
			nameChanged = False
			if currDrvName != enteredDrvName:
				drvNameToSave = enteredDrvName
				nameChanged = True
			
			#update database
			sql1 = f"UPDATE drives SET drive_name = '{enteredDrvName}' WHERE drive_id = {driveID}"
			sql2 = f"UPDATE drives SET drive_letter = '{enteredDrvLetter}' WHERE drive_id = {driveID}"
			try:
				self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
				self.vc.getView().getMainController().getModel().getController().queryDatabase(sql1, commitReq = True)
				self.vc.getView().getMainController().getModel().getController().queryDatabase(sql2, commitReq = True)
			except Exception as e:
				print(e)

			self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
			if nameChanged == True:
				self.vc.getView().getMainController().sendToOutput(f"   Renamed drive '{currDrvName}' to '{enteredDrvName}' in database.")
			if letterChanged == True:
				self.vc.getView().getMainController().sendToOutput(f"   Changed drive letter from '{currDrvLetter}' to '{enteredDrvLetter}' in database.")
			if nameChanged == False and letterChanged == False:
				self.vc.getView().getMainController().sendToOutput(f"   Did not change drive information in database.")
			
			#update object model
			self.drvObj.setName(drvNameToSave)
			self.drvObj.setDriveLetter(drvLetterToSave)

			if nameChanged == True:
				self.vc.getView().getMainController().sendToOutput(f"   Renamed drive '{currDrvName}' to '{enteredDrvName}' in object model.")
			if letterChanged == True:
				self.vc.getView().getMainController().sendToOutput(f"   Changed drive letter from '{currDrvLetter}' to '{enteredDrvLetter}' in obect model.")
			if nameChanged == False and letterChanged == False:
				self.vc.getView().getMainController().sendToOutput(f"   Did not change drive information in object model.")
				
			#update tree
			st = "Drive: " + drvNameToSave
			self.cFrame.getTree().item(self.drv_iidFromTree, text = st)

			self.winfo_toplevel().destroy()



	def kill(self):
		self.winfo_toplevel().destroy()



class EditProcedureWindow(tk.Tk):
	def __init__(self, configFrame, viewController, iid=''):
		self.vc = viewController
		self.cFrame = configFrame

		self.displayFrame = self.cFrame.parent.getDisplayFrame()

		self.procOpDictionary = self.vc.getView().getMainController().getAvailableProceduresNumToStr()
		self.procOpDictionaryStrToNum = self.vc.getView().getMainController().getAvailableProceduresStrToNum()
		operations = []
		for i in range(len(self.procOpDictionary)):
			operations.append(self.procOpDictionary[i])

		objMan = self.vc.getView().getMainController().getObjectManager()
		self.userObj = objMan.getCurrentUserObject()

		procSel = self.cFrame.getTree().selection()
		collDigits = ""
		procDigits = ""
		self.selectedProcName = ""
		self.proc_iidFromTree = ""
		self.coll_iid = ""
		self.collObj = ""
		if len(procSel) > 0:
			self.proc_iidFromTree = procSel[0]
			for j in self.proc_iidFromTree:
				if j.isdigit():
					procDigits = procDigits + j

			self.coll_iid = self.cFrame.getTree().parent(self.proc_iidFromTree)
			for i in self.coll_iid:
				if i.isdigit():
					collDigits = collDigits + i
			self.collObj = self.userObj.getCollection(int(collDigits))
			self.procObj = self.collObj.getProcedure(int(procDigits))
			self.selectedProcName = self.procObj.getName()


		procObjs = self.collObj.getProcedures()
		procObjItems = [(item[0],item[1]) for item in procObjs.items()]
		procNames = []
		procIDs = []
		self.procDict = {}
		self.procDictReversed = {}
		if len(procObjItems) > 0:
			for eachProcedure in procObjItems:
				procItemName = eachProcedure[1].getName()
				procItemID = eachProcedure[1].getID()
				procNames.append(procItemName)
				procIDs.append(procItemID)
			self.procDict = dict(zip(procIDs, procNames))
			self.procDictReversed = {v: k for k, v in self.procDict.items()}


		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Edit Procedure")
		self.winfo_toplevel().geometry("600x250+400+200")
		f = tk.Frame(self, bg='white')

		procNameLabel = tk.Label(f, text="Procedure Name:", bg="white", fg="black")
		procOpLabel = tk.Label(f, text="Operation:", bg='white', fg='black')
		procSourceLabel = tk.Label(f, text="Source:", bg='white', fg='black')
		procDestLabel = tk.Label(f, text="Destination:", bg='white', fg='black')
		self.procNameEntry = tk.Entry(f, width=30, borderwidth=2)
		self.procNameEntry.insert(0, self.procObj.getName())
		self.opsListBox = ttk.Combobox(f, values = operations, state='readonly')
		self.currOpCode = self.vc.getView().getMainController().getAvailableProceduresNumToStr()[self.procObj.getOperationCode()]
		self.opsListBox.set(self.currOpCode)
		self.procSourceEntry = tk.Entry(f, width=70, borderwidth=2)
		self.procSourceEntry.insert(0, self.procObj.getSourcePath())
		self.procDestEntry = tk.Entry(f, width=70, borderwidth=2)
		self.procDestEntry.insert(0, self.procObj.getDestinationPath())
		self.sourceFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openSrcBrowser(self.opsListBox.get(), self.procSourceEntry))
		self.destFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openDestBrowser(self.opsListBox.get(), self.procDestEntry))
		self.editProcedureButton = tk.Button(f, text="Edit\nProcedure", height=2, width=10, command = lambda : self.editProcedure())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		procNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		procOpLabel.place(x=30, y=55, relx=0, rely=0, anchor='nw')
		procSourceLabel.place(x=30, y=90, relx=0, rely=0, anchor='nw')
		procDestLabel.place(x=30, y=125, relx=0, rely=0, anchor='nw')
		self.procNameEntry.place(x=135, y=20, relx=0, rely=0, anchor='nw')
		self.opsListBox.place(x=135, y=55, relx=0, rely=0, anchor='nw')
		self.opsListBox.config(width=30)
		self.procSourceEntry.place(x=135, y=90, relx=0, rely=0, anchor='nw')
		self.procDestEntry.place(x=135, y=125, relx=0, rely=0, anchor='nw')
		self.sourceFileBrowserButton.place(x=555, y=88, relx=0, rely=0, anchor='nw')
		self.destFileBrowserButton.place(x=555, y=123, relx=0, rely=0, anchor='nw')
		self.editProcedureButton.place(x=160, y=200, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=360, y=200, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

	def openSrcBrowser(self, operation, entrybox):
		directoryName = ""
		if "Single File" in operation:
			directoryName = filedialog.askopenfilename(initialdir="/", title="Select File")
		else:
			directoryName = filedialog.askdirectory(initialdir="/", title="Select Folder")
		entrybox.delete(0, 'end')
		entrybox.insert(0, directoryName)

	def openDestBrowser(self, operation, entrybox):
		directoryName = filedialog.askdirectory(initialdir="/", title = "Select Folder")
		entrybox.delete(0, 'end')
		entrybox.insert(0, directoryName)

	def editProcedure(self):
		procID = self.procDictReversed[self.selectedProcName]
		infoSrc = self.vc.getView().getMainController().getInformationSource()
		currUser = self.vc.getView().getMainController().getCurrentUser()
		currUserID = self.vc.getView().getMainController().getCurrentUserID()

		#notify user of operation
		self.vc.getView().getMainController().sendToOutput(f"Attempting to edit Procedure {self.selectedProcName}...")

		if infoSrc == SOURCE_DATABASE or infoSrc == SOURCE_DATABASE_NO_CFG:
			currProcName = self.procObj.getName()
			currProcSrc = self.procObj.getSourcePath()
			currProcDest = self.procObj.getDestinationPath()
			currProcOpCode = self.currOpCode # string representation

			enteredProcName = self.procNameEntry.get()
			enteredProcSrc = self.procSourceEntry.get()
			enteredProcDest = self.procDestEntry.get()
			enteredOpCode = self.opsListBox.get()

			enteredProcSrc = enteredProcSrc.replace(sep, '/')
			enteredProcDest = enteredProcDest.replace(sep, '/')

			procNameToSave = currProcName
			procNameChanged = False
			if currProcName != enteredProcName:
				procNameToSave = enteredProcName
				procNameChanged = True

			procSrcToSave = currProcSrc
			procSrcChanged = False
			if currProcSrc != enteredProcSrc:
				procSrcToSave = enteredProcSrc
				procSrcChanged = True

			procDestToSave = currProcDest
			procDestChanged = False
			if currProcDest != enteredProcDest:
				procDestToSave = enteredProcDest
				procDestChanged = True

			procOpCodeToSave = currProcOpCode
			procOpCodeChanged = False
			if currProcOpCode != enteredOpCode:
				procOpCodeToSave = enteredOpCode
				procOpCodeChanged = True
			
			procOpCodeToSave = self.vc.getView().getMainController().getAvailableProceduresStrToNum()[procOpCodeToSave]

			if procNameChanged:
				sql = f"UPDATE procedures SET proc_name = '{procNameToSave}' WHERE proc_num = {procID}"
				self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
				self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
				self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				
				self.vc.getView().getMainController().sendToOutput(f"   Renamed procedure '{currProcName}' to '{procNameToSave}' in database.")

				self.procObj.setName(procNameToSave)

				self.vc.getView().getMainController().sendToOutput(f"   Renamed procedure '{currProcName}' to '{procNameToSave}' in object model.")

				st = "Procedure: " + procNameToSave
				self.cFrame.getTree().item(self.proc_iidFromTree, text = st)

				displayFrame = self.cFrame.parent.getDisplayFrame()
				if displayFrame.getIdleConfigTree().exists(self.proc_iidFromTree):
					displayFrame.getIdleConfigTree().item(self.proc_iidFromTree, values=[self.collObj.getName(), procNameToSave])
				elif displayFrame.getRunConfigTree().exists(self.proc_iidFromTree):
					displayFrame.getRunConfigTree().item(self.proc_iidFromTree, values=[self.collObj.getName(), procNameToSave])
			

			if procSrcChanged:
				sql = f"UPDATE procedures SET src_path = '{procSrcToSave}' WHERE proc_num = {procID}"
				self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
				self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
				self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				
				self.vc.getView().getMainController().sendToOutput(f"   Renamed source path in database to: \n'{procSrcToSave}'")
				
				self.procObj.setSourcePath(procSrcToSave)

				self.vc.getView().getMainController().sendToOutput(f"   Renamed source path in object model to: \n'{procSrcToSave}'")
				


			if procDestChanged:
				sql = f"UPDATE procedures SET dest_path = '{procDestToSave}' WHERE proc_num = {procID}"
				self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
				self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
				self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				
				self.vc.getView().getMainController().sendToOutput(f"   Renamed destination path in database to: \n'{procDestToSave}'")
				
				self.procObj.setDestinationPath(procDestToSave)
				
				self.vc.getView().getMainController().sendToOutput(f"   Renamed destination path in object model to: \n'{procDestToSave}'")
				

			if procOpCodeChanged:
				sql = f"UPDATE procedures SET op_code = {procOpCodeToSave} WHERE proc_num = {procID}"
				self.vc.getView().getMainController().getModel().getController().requestOpenDatabase()
				self.vc.getView().getMainController().getModel().getController().queryDatabase(sql, commitReq = True)
				self.vc.getView().getMainController().getModel().getController().requestCloseDatabase()
				
				self.vc.getView().getMainController().sendToOutput(f"   Reset op code in database to: {procOpCodeToSave}")

				self.procObj.setOperationCode(procOpCodeToSave)
				
				self.vc.getView().getMainController().sendToOutput(f"   Reset op code in object model to: {procOpCodeToSave}")
				
		self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()