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

class AddDeviceDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Add Device")
		self.winfo_toplevel().geometry("350x150+500+200")
		frame = tk.Frame(self, bg='white')


		devNameLabel = tk.Label(frame, text="Device Name: ", bg="white", fg="black")
		self.devNameEntry = tk.Entry(frame, width=35, borderwidth=2)
		self.addDeviceButton = tk.Button(frame, text="Add Device", height=2, width=10, command = lambda : self.addDevice())
		self.closeButton = tk.Button(frame, text="Cancel", height=2, width=10, command = self.kill)

		devNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.devNameEntry.place(x=110, y=20, relx=0, rely=0, anchor='nw')

		self.addDeviceButton.place(x=30, y = 80, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=80, relx=0, rely=0, anchor='nw')



		frame.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())


	@property
	def application(self):
		return self._application

	'''
	addDevice()

	Handles the high-level addition of a new Device to the system.
	'''
	def addDevice(self):
		newDeviceName = self.devNameEntry.get()

		infoSrc = self.application.informationSource.name
		currUser = self.application.currentUser
		currUserID = self.application.currentUserID

		#Notify User of add operation
		self.application.outputManager.broadcast(f"Attempting to add Device {newDeviceName} . . .")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Check whether the device is already in the database for currentUser
			deviceExists = self.application.databaseOperator.queries.checkDatabaseForDevice(newDeviceName, currUserID)

			if deviceExists == True:
				self.application.outputManager.broadcast(f"   Device {newDeviceName} already exists in database for user {currUser}. Could not add device.")
			else:
				#Add device to database
				deviceID = self.application.databaseOperator.queries.addDevice(newDeviceName, currUserID)
				
				if deviceID is not None:
					self.application.outputManager.broadcast(f"   Device '{newDeviceName}' added to database.")

					#Add device to object model.
					devID = self.application.objectModel.addDeviceToModel(deviceID, newDeviceName, currUserID)
					if devID is not None:
						self.application.outputManager.broadcast(f"   Device '{newDeviceName}' added to object model.")

						#Add device to TreeView
						self._treeViewFrame.tree.insert("devices", "end", iid=f"dev{devID}", text=f"{newDeviceName}")

		elif infoSrc == "SOURCE_CONFIG_NO_DB":
			self.application.outputManager(f"   Device '{newDeviceName}' cannot be added cto configuration. Connect to database.")
		else:
			self.application.outputManager(f"   Device '{newDeviceName}' cannot be added cto configuration. Connect to database.")
		
		#Close the window
		self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()
