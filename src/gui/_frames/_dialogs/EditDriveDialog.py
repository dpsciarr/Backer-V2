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

import tkinter as tk
from tkinter import ttk

class EditDriveDialog(tk.Tk):
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
			self.driveObject = self.deviceObject.getDrive(int(driveDigits))
			self.selectedDriveName = self.driveObject.driveName

		driveObjects = self.deviceObject.drives
		driveObjectItems = [(item[0], item[1]) for item in driveObjects.items()]
		driveNames = []
		driveIDs = []
		self.driveDict = {}
		self.driveDictReversed = {}
		if len(driveObjectItems) > 0:
			for eachDrive in driveObjectItems:
				driveItemName = eachDrive[1].driveName
				driveItemID = eachDrive[1].driveID
				driveNames.append(driveItemName)
				driveIDs.append(driveItemID)
			self.driveDict = dict(zip(driveIDs, driveNames))
			self.driveDictReversed = {v: k for k, v in self.driveDict.items()}

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Edit Drive")
		self.winfo_toplevel().geometry("350x150+500+200")
		f = tk.Frame(self, bg='white')

		self.drvNameLabel = tk.Label(f, bg='white', text="Name:")
		self.drvNameEntry = tk.Entry(f, width = 28, borderwidth = 2)
		self.drvNameEntry.insert(0, self.driveObject.driveName)
		self.drvLetterLabel = tk.Label(f, bg='white', text="Letter:")
		self.drvLetterList = ttk.Combobox(f, values = self.application.objectModel.driveLetters, state='readonly')
		self.drvLetterList.set(self.driveObject.driveLetter)
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

		self.after(500, lambda: self.focus_force())


	@property
	def application(self):
		return self._application

	def editDrive(self):
		driveID = self.driveDictReversed[self.selectedDriveName]
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID

		self.application.outputManager.broadcast(f"Attempting to edit Drive {self.selectedDriveName}.")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			currentDriveName = self.driveObject.driveName
			currentDriveLetter = self.driveObject.driveLetter
			enteredDriveName = self.drvNameEntry.get()
			enteredDriveLetter = self.drvLetterList.get()

			driveLetterToSave = currentDriveLetter
			letterChanged = False
			if currentDriveLetter != enteredDriveLetter:
				driveLetterToSave = enteredDriveLetter
				letterChanged = True

			driveNameToSave = currentDriveName
			nameChanged = False
			if currentDriveName != enteredDriveName:
				driveNameToSave = enteredDriveName
				nameChanged = True

			if nameChanged == True:
				#SQL for changing the name
				self.application.databaseOperator.queries.updateDriveName(driveNameToSave, driveID)
				self.application.outputManager.broadcast(f"   Drive renamed from {self.selectedDriveName} to {driveNameToSave} in database.")

				#object model
				self.driveObject.driveName = driveNameToSave
				self.application.outputManager.broadcast(f"   Drive renamed from {self.selectedDriveName} to {driveNameToSave} in Object Model.")

				#Update Tree
				self._treeViewFrame.tree.item(self.driveIIDfromTree, text = driveNameToSave)

			if letterChanged == True:
				#SQL for changing the letter
				self.application.databaseOperator.queries.updateDriveLetter(driveLetterToSave, driveID)
				self.application.outputManager.broadcast(f"   Drive letter changed from {currentDriveLetter} to {driveLetterToSave} in database.")

				#object model
				self.driveObject.driveLetter = driveLetterToSave
				self.application.outputManager.broadcast(f"   Drive letter changed from {currentDriveLetter} to {driveLetterToSave} in Object Model.")

			self.winfo_toplevel().destroy()


	def kill(self):
		self.winfo_toplevel().destroy()