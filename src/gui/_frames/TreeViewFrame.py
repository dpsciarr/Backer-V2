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
import sys
import os.path

framesDir = os.path.dirname(__file__)
dialogDir = os.path.join(framesDir, "_dialogs")

sys.path.append(dialogDir)

from AddCollectionDialog import AddCollectionDialog
from AddProcedureDialog import AddProcedureDialog
from DeleteCollectionDialog import DeleteCollectionDialog
from RenameCollectionDialog import RenameCollectionDialog
from EditProcedureDialog import EditProcedureDialog
from DeleteProcedureDialog import DeleteProcedureDialog
from AddDeviceDialog import AddDeviceDialog
from AddDriveDialog import AddDriveDialog
from RenameDeviceDialog import RenameDeviceDialog
from DeleteDeviceDialog import DeleteDeviceDialog
from EditDriveDialog import EditDriveDialog
from DeleteDriveDialog import DeleteDriveDialog

sys.path.remove(dialogDir)

class TreeViewFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._application = application
		self._mainWindow = mainWindow
		self._tree = None
		self._currentTreeItemID = None
		
		tk.Frame.__init__(self, mainWindow, bg='WHITE', width=250)

		#Collection Context Menu
		self.collectionsContextMenu = tk.Menu(self, tearoff=0)
		self.collectionsContextMenu.add_command(label="Add Collection", command = lambda : self.showDialog(AddCollectionDialog))

		self.collectionNameContextMenu = tk.Menu(self, tearoff=0)
		self.collectionNameContextMenu.add_command(label="Add Procedure", command=lambda : self.showDialog(AddProcedureDialog))
		#self.collectionNameContextMenu.add_command(label="Select for Run Configuration", command = self.selectCollectionForRunConfig)
		#self.collectionNameContextMenu.add_command(label="Deselect for Run Configuration", command = self.deselectCollectionForRunConfig)
		self.collectionNameContextMenu.add_command(label="Rename Collection", command=lambda : self.showDialog(RenameCollectionDialog))
		self.collectionNameContextMenu.add_command(label="Delete Collection", command=lambda : self.showDialog(DeleteCollectionDialog))

		self.procedureNameContextMenu = tk.Menu(self, tearoff=0)
		self.procedureNameContextMenu.add_command(label="Edit Procedure", command=lambda : self.showDialog(EditProcedureDialog))
		#self.procedureNameContextMenu.add_command(label="Select for Run Configuration", command= self.selectProcForRunConfig)
		#self.procedureNameContextMenu.add_command(label="Deselect for Run Configuration", command= self.deselectProcForRunConfig)
		self.procedureNameContextMenu.add_command(label="Delete Procedure", command=lambda : self.showDialog(DeleteProcedureDialog))

		self.devicesContextMenu = tk.Menu(self, tearoff=0)
		self.devicesContextMenu.add_command(label="Add Device", command=lambda : self.showDialog(AddDeviceDialog))

		self.deviceNameContextMenu = tk.Menu(self, tearoff=0)
		self.deviceNameContextMenu.add_command(label="Add Drive", command=lambda : self.showDialog(AddDriveDialog))
		self.deviceNameContextMenu.add_command(label="Rename Device", command=lambda : self.showDialog(RenameDeviceDialog))
		self.deviceNameContextMenu.add_command(label="Delete Device", command=lambda : self.showDialog(DeleteDeviceDialog))

		self.driveNameContextMenu = tk.Menu(self, tearoff=0)
		self.driveNameContextMenu.add_command(label="Edit Drive", command=lambda : self.showDialog(EditDriveDialog))
		self.driveNameContextMenu.add_command(label="Delete Drive", command=lambda : self.showDialog(DeleteDriveDialog))

	@property
	def application(self):
		return self._application

	@property
	def mainWindow(self):
		return self._mainWindow

	@property
	def tree(self):
		return self._tree

	@tree.setter
	def tree(self, value):
		self._tree = value

	@property
	def currentTreeItemID(self):
		return self._currentTreeItemID

	@currentTreeItemID.setter
	def currentTreeItemID(self, value):
		self._currentTreeItemID = value

	'''
	showDialog(function)

	'function' describes the Class of the tk.Window dialog.

	showDialog creates an instance of 'function' and runs it with mainloop()
	'''
	def showDialog(self, function):
		dialog = function(self)
		dialog.mainloop()

	'''
	showContextMenu(event)

	Handles the filtering of which context menu to show based on the "iid" of the 
	currently selected treeview.
	'''
	def showContextMenu(self, event):
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

	'''
	tree_click_event(event)

	Keeps track of the currently selected item in treeview with currentTreeItemID.
	'''
	def tree_click_event(self, event):
		self.currentTreeItemID = self.tree.focus()
	
	'''
	buildTreeView(userObject)

	Handles the high-level building of the TreeViewFrame's treeview.
	'''
	def buildTreeView(self, userObject):
		self.tree = ttk.Treeview(self, selectmode='browse')

		#Right Click binding
		self.tree.bind("<Button-3>", self.showContextMenu)

		#Selection binding
		self.tree.bind('<<TreeviewSelect>>', self.tree_click_event)

		#Set TreeView heading
		self.tree.heading('#0', text='Configuration Tree')

		#Insert User Root
		self.tree.insert("", "end", iid="user", text=f"User: {userObject.username}")
		
		#Insert Devices Root
		self.tree.insert("user", "end", iid="devices", text="Devices")

		devDict = userObject.devices
		for devKey in devDict:
			devID = devDict[devKey].deviceID
			devName = devDict[devKey].deviceName
			self.tree.insert("devices", "end", text=f"{devName}", iid=f"dev{devID}")

			drvDict = devDict[devKey].drives
			for (drvKey, drvVal) in drvDict.items():
				drvID = drvVal.driveID
				drvName = drvVal.driveName
				self.tree.insert(f"dev{devID}", "end", text=f"{drvName}", iid=f"drv{drvID}")


		#Insert Collections
		self.tree.insert("user", "end", iid="collections", text="Collections")

		collDict = userObject.collections
		for collKey in collDict:
			collID = collDict[collKey].collectionID
			collName = collDict[collKey].collectionName
			self.tree.insert("collections", "end", text=f"{collName}", iid=f"coll{collID}")

			procDict = collDict[collKey].procedures
			for (procKey, procVal) in procDict.items():
				procID = procVal.procedureID
				procName = procVal.procedureName
				self.tree.insert(f"coll{collID}", "end", text=f"{procName}", iid=f"proc{procID}")

		self.tree.pack(fill = 'both', expand = True)









