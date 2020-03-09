import tkinter as tk
from tkinter import ttk

class DeleteDeviceDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame

		self._currentUserObject = self.application.objectModel.currentUser

		deviceObjects = self._currentUserObject.devices

		deviceObjectItems = [(item[0], item[1]) for item in deviceObjects.items()]
		deviceNames = []
		deviceIDs = []
		self.deviceDict = {}
		self.deviceDictReversed = {}
		if len(deviceObjectItems) > 0:
			for eachDevice in deviceObjectItems:
				deviceItemName = eachDevice[1].deviceName
				deviceItemID = eachDevice[1].deviceID
				deviceNames.append(deviceItemName)
				deviceIDs.append(deviceItemID)
			self.deviceDict = dict(zip(deviceIDs, deviceNames))
			self.deviceDictReversed = {v: k for k, v in self.deviceDict.items()}

		selection = self._treeViewFrame.tree.selection()
		digits = ""
		self.selectedDeviceName = ""
		self.iidFromTree = ""
		if len(selection) > 0:
			self.iidFromTree = selection[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			self.selectedDeviceName = self.deviceDict[int(digits)]

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Device")
		self.winfo_toplevel().geometry("350x150+500+200")
		f = tk.Frame(self, bg='white')

		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedDeviceName}?", bg="white", fg="black")
		self.deleteDevButton = tk.Button(f, text="Delete Device", height=2, width=10, command = lambda : self.deleteDevice())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteDevButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)
		self.after(500, lambda: self.focus_force())

	@property
	def application(self):
		return self._application

	def deleteDevice(self):
		deviceID = self.deviceDictReversed[self.selectedDeviceName]
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID
		deviceObject = self._currentUserObject.getDevice(int(deviceID))
		driveObjects = deviceObject.drives
		driveObjectItems = [(item[0], item[1]) for item in driveObjects.items()]

		#notify user of deletion attempt.
		self.application.outputManager.broadcast(f"Attempting to delete device {self.selectedDeviceName}.")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			for eachDriveObject in driveObjectItems:
				driveID = eachDriveObject[1].driveID
				self.application.databaseOperator.queries.deleteDrive(driveID)

			#Remove collection from database
			self.application.databaseOperator.queries.deleteDevice(deviceID)

			self.application.outputManager.broadcast(f"   Device {self.selectedDeviceName} has been deleted from the database.")

			#Remove collection from object model
			self._currentUserObject.removeDevice(deviceID)
			result = ""
			try:
				result = self._currentUserObject.getDevice(deviceID)
			except KeyError:
				self.application.outputManager.broadcast(f"   Device {self.selectedDeviceName} deleted from Object Model.")
				self._treeViewFrame.tree.delete(self.iidFromTree)

			if result == None:
				self.application.outputManager.broadcast(f"   Device {self.selectedDeviceName} deleted from Object Model.")
				self._treeViewFrame.tree.delete(self.iidFromTree)

		self.winfo_toplevel().destroy()


	def kill(self):
		self.winfo_toplevel().destroy()
