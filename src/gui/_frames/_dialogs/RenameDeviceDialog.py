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

class RenameDeviceDialog(tk.Tk):
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
		self.winfo_toplevel().title("Rename Device")
		self.winfo_toplevel().geometry("350x150+500+200")
		f = tk.Frame(self, bg='white')


		self.renameDevLabel = tk.Label(f, bg='white', text=f"Rename device '{self.selectedDeviceName}' to:")
		self.renameDevEntry = tk.Entry(f, width = 28, borderwidth = 2)
		self.renameDevButton = tk.Button(f, text="Rename\nDevice", height=2, width=10, command = lambda : self.renameDevice())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		self.renameDevLabel.place(x=10, y=20, relx=0, rely=0, anchor='nw')
		self.renameDevEntry.place(x=160, y=20, relx=0, rely=0, anchor='nw')
		self.renameDevButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')


		f.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())

	@property
	def application(self):
		return self._application

	def renameDevice(self):
		deviceID = self.deviceDictReversed[self.selectedDeviceName]
		newDeviceName = self.renameDevEntry.get()
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Notify user of renaming request
			self.application.outputManager.broadcast(f"Attempting to rename {self.selectedDeviceName} to {newDeviceName}")

			#Rename the Device in the database
			self.application.databaseOperator.queries.renameDevice(deviceID, newDeviceName)

			#Notify user of database rename
			self.application.outputManager.broadcast(f"   Device {self.selectedDeviceName} renamed to {newDeviceName} in database.")

			#Rename in object model.
			deviceObject = self._currentUserObject.getDevice(deviceID)
			deviceObject.deviceName = newDeviceName

			self.application.outputManager.broadcast(f"   Device {self.selectedDeviceName} renamed to {newDeviceName} in Object Model.")

			#Rename the device in the tree
			self._treeViewFrame.tree.item(self.iidFromTree, text = newDeviceName)

			self.winfo_toplevel().destroy()



	def kill(self):
		self.winfo_toplevel().destroy()

