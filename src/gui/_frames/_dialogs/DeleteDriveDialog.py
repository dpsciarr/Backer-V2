import tkinter as tk
from tkinter import ttk

class DeleteDriveDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame

		self._currentUserObject = self.application.objectModel.currentUser

		driveSelection = self._treeViewFrame.tree.selection()
		deviceDigits = ""
		driveDigits = ""
		self.selectedDriveName = ""
		self.driveIIDfromTree = ""
		self.deviceIID = ""
		self.deviceObject = ""
		if len(driveSelection) > 0:
			self.driveIIDfromTree = driveSelection[0]
			for j in self.driveIIDfromTree:
				if j.isdigit():
					driveDigits = driveDigits + j

			self.deviceIID = self._treeViewFrame.tree.parent(self.driveIIDfromTree)
			for i in self.deviceIID:
				if i.isdigit():
					deviceDigits = deviceDigits + i
			self.deviceObject = self._currentUserObject.getDevice(int(deviceDigits))
			driveObject = self.deviceObject.getDrive(int(driveDigits))
			self.selectedDriveName = driveObject.driveName

		self.driveObjects = self.deviceObject.drives
		self.driveObjectItems = [(item[0], item[1]) for item in self.driveObjects.items()]
		driveNames = []
		driveIDs = []
		self.driveDict = {}
		self.driveDictReversed = {}
		if len(self.driveObjectItems) > 0:
			for eachDrive in self.driveObjectItems:
				driveItemName = eachDrive[1].driveName
				driveItemID = eachDrive[1].driveID
				driveNames.append(driveItemName)
				driveIDs.append(driveItemID)
			self.driveDict = dict(zip(driveIDs, driveNames))
			self.driveDictReversed = {v: k for k, v in self.driveDict.items()}

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Drive")
		self.winfo_toplevel().geometry("350x150+500+200")
		f = tk.Frame(self, bg='white')

		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedDriveName}?", bg="white", fg="black")
		self.deleteDrvButton = tk.Button(f, text="Delete Drive", height=2, width=10, command = lambda : self.deleteDrive())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteDrvButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)
		self.after(500, lambda: self.focus_force())

	@property
	def application(self):
		return self._application

	def deleteDrive(self):
		driveID = self.driveDictReversed[self.selectedDriveName]
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID

		#Notify user of deletion attempt
		self.application.outputManager.broadcast(f"Attempting to delete drive {self.selectedDriveName} . . .")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Remove drive from database...
			self.application.databaseOperator.queries.deleteDrive(driveID)

			self.application.outputManager.broadcast(f"   Drive {self.selectedDriveName} has been deleted from the database.")

			#Remove drive from object model
			self.deviceObject.removeDrive(driveID)
			result = ""
			try:
				result = self.deviceObject.getDrive(driveID)
			except KeyError:
				self.application.outputManager.broadcast(f"   Drive {self.selectedDriveName} deleted from Object Model.")
				self._treeViewFrame.tree.delete(self.driveIIDfromTree)

			if result == None:
				self.application.outputManager.broadcast(f"   Drive {self.selectedDriveName} deleted from Object Model.")
				self._treeViewFrame.tree.delete(self.driveIIDfromTree)

			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()
