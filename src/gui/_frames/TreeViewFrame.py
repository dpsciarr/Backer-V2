import tkinter as tk
from tkinter import ttk

class TreeViewFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._application = application
		self._mainWindow = mainWindow
		self._tree = None
		self._currentTreeItemID = None
		
		tk.Frame.__init__(self, mainWindow, bg='WHITE', width=250)

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

	def showContextMenu(self, event):
		print("Context Menu appears")

	def tree_click_event(self, event):
		self.currentTreeItemID = self.tree.focus()
	
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
			self.tree.insert("devices", "end", text=f"Device: {devName}", iid=f"dev{devID}")

			drvDict = devDict[devKey].drives
			for (drvKey, drvVal) in drvDict.items():
				drvID = drvVal.driveID
				drvName = drvVal.driveName
				self.tree.insert(f"dev{devID}", "end", text=f"Drive: {drvName}", iid=f"drv{drvID}")


		#Insert Collections
		self.tree.insert("user", "end", iid="collections", text="Collections")

		collDict = userObject.collections
		for collKey in collDict:
			collID = collDict[collKey].collectionID
			collName = collDict[collKey].collectionName
			self.tree.insert("collections", "end", text=f"Collection: {collName}", iid=f"coll{collID}")

			procDict = collDict[collKey].procedures
			for (procKey, procVal) in procDict.items():
				procID = procVal.procedureID
				procName = procVal.procedureName
				self.tree.insert(f"coll{collID}", "end", text=f"Procedure: {procName}", iid=f"proc{procID}")

		self.tree.pack(fill = 'both', expand = True)









