import tkinter as tk
from tkinter import ttk

class AddDriveDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame

		deviceObjects = self.application.objectModel.currentUser.devices

		deviceObjectItems = [(item[0], item[1]) for item in deviceObjects.items()]
		deviceNames = []
		deviceIDs = []
		self._deviceDictKV = {}
		self._deviceDictVK = {}
		if len(deviceObjectItems) > 0:
			for eachDevice in deviceObjectItems:
				devItemName = eachDevice[1].deviceName
				devItemID = eachDevice[1].deviceID
				deviceNames.append(devItemName)
				deviceIDs.append(devItemID)
			self._deviceDictKV = dict(zip(deviceIDs,deviceNames))
			self._deviceDictVK = {v: k for k, v in self._deviceDictKV.items()}

		sel = self._treeViewFrame.tree.selection()
		digits = ""
		selectedDeviceName = ""
		self.iidFromTree = ""
		if len(sel) > 0:
			self.iidFromTree = sel[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			selectedDeviceName = self._deviceDictKV[int(digits)]

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Add Drive")
		self.winfo_toplevel().geometry("350x180+500+200")
		frame = tk.Frame(self, bg='white')

		drvNameLabel = tk.Label(frame, text="Drive Name:", bg="white", fg="black")
		drvLetterLabel = tk.Label(frame, text="Drive Letter:", bg="white", fg="black")
		drvAssociatedDeviceLabel = tk.Label(frame, text="Parent Device:", bg="white", fg="black")
		self.drvNameEntry = tk.Entry(frame, width=30, borderwidth=2)

		self.drvLetterList = ttk.Combobox(frame, values = self.application.objectModel.driveLetters, state='readonly')
		self.drvLetterList.set(self.application.objectModel.driveLetters[0])

		self.devList = ttk.Combobox(frame, values = deviceNames, state='readonly')
		if selectedDeviceName in deviceNames:
			self.devList.set(selectedDeviceName)
		else:
			self.devList.set(deviceNames[0])

		self.addDriveButton = tk.Button(frame, text="Add Drive", height=2, width=10, command = lambda : self.addDrive())
		self.closeButton = tk.Button(frame, text="Cancel", height=2, width=10, command = self.kill)

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

		frame.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())

	@property
	def application(self):
		return self._application

	def addDrive(self):
		newDriveName = self.drvNameEntry.get()
		newDriveLetter = self.drvLetterList.get()
		associatedDeviceName = self.devList.get()
		newDeviceID = self._deviceDictVK[associatedDeviceName]

		infoSrc = self.application.informationSource.name
		currUser = self.application.currentUser
		currUserID = self.application.currentUserID

		#Notify user of add operation
		self.application.outputManager.broadcast(f"Attempting to add Drive {newDriveName} . . .")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Check whether the drive is already in the database
			driveExists = self.application.databaseOperator.queries.checkDatabaseForDrive(newDriveName, currUserID)

			if driveExists == True:
				self.application.outputManager.broadcast(f"   Drive {newDriveName} already exists in database for device {associatedDeviceName}. Could not add drive.")
			else:
				#Add drive to database
				driveID = self.application.databaseOperator.queries.addDrive(newDriveName, newDriveLetter, newDeviceID)

				if driveID is not None:
					self.application.outputManager.broadcast(f"   Drive '{newDriveName}' added to database.")

					#Add drive to object model
					driveID = self.application.objectModel.addDriveToModel(driveID, newDriveName, newDriveLetter, newDeviceID)
					if driveID is not None:
						self.application.outputManager.broadcast(f"   Drive '{newDriveName}' added to object model.")

						#Add drive to TreeView
						self._treeViewFrame.tree.insert(self.iidFromTree, "end", iid=f"drv{driveID}", text=f"{newDriveName}")
		
		elif infoSrc == "SOURCE_CONFIG_NO_DB":
			self.application.outputManager(f"   Drive '{newDriveName}' cannot be added to configuration. Connect to database.")
		else:
			self.application.outputManager(f"   Drive '{newDriveName}' cannot be added to configuration. Connect to database.")
		
		#Close the window
		self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()
