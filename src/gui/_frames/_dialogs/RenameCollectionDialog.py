import tkinter as tk
from tkinter import ttk

class RenameCollectionDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame
		self._currentUserObject = self.application.objectModel.currentUser

		collectionObjects = self._currentUserObject.collections

		collectionObjectItems = [(item[0], item[1]) for item in collectionObjects.items()]
		collectionNames = []
		collectionIDs = []
		self.collectionDict = {}
		self.collectionDictReversed = {}
		if len(collectionObjectItems) > 0:
			for eachCollection in collectionObjectItems:
				collectionItemName = eachCollection[1].collectionName
				collectionItemID = eachCollection[1].collectionID
				collectionNames.append(collectionItemName)
				collectionIDs.append(collectionItemID)
			self.collectionDict = dict(zip(collectionIDs, collectionNames))
			self.collectionDictReversed = {v: k for k, v in self.collectionDict.items()}
		
		selection = self._treeViewFrame.tree.selection()
		digits = ""
		self.selectedCollectionName = ""
		self.iidFromTree = ""
		if len(selection) > 0:
			self.iidFromTree = selection[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			self.selectedCollectionName = self.collectionDict[int(digits)]


		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Rename Collection")
		self.winfo_toplevel().geometry("350x150+500+200")
		f = tk.Frame(self, bg='white')

		self.renameCollLabel = tk.Label(f, bg='white', text=f"Rename collection '{self.selectedCollectionName}' to:")
		self.renameCollEntry = tk.Entry(f, width = 40, borderwidth = 2)
		self.renameCollButton = tk.Button(f, text="Rename\nCollection", height=2, width=10, command = lambda : self.renameCollection())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		self.renameCollLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.renameCollEntry.place(x=30, y=50, relx=0, rely=0, anchor='nw')
		self.renameCollButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())


	@property
	def application(self):
		return self._application

	def renameCollection(self):
		print("Renaming")
		collectionID = self.collectionDictReversed[self.selectedCollectionName]
		newCollectionName = self.renameCollEntry.get()
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID


		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Notify user of renaming request
			self.application.outputManager.broadcast(f"Attempting to rename {self.selectedCollectionName} to {newCollectionName}")

			#Rename the Device in the database
			self.application.databaseOperator.queries.renameCollection(collectionID, newCollectionName)

			#Notify user of database rename
			self.application.outputManager.broadcast(f"   Collection {self.selectedCollectionName} renamed to {newCollectionName} in database.")

			#Rename in object model.
			collectionObject = self._currentUserObject.getCollection(collectionID)
			collectionObject.collectionName = newCollectionName

			self.application.outputManager.broadcast(f"   Collection {self.selectedCollectionName} renamed to {newCollectionName} in Object Model.")

			#Rename the device in the tree
			self._treeViewFrame.tree.item(self.iidFromTree, text = newCollectionName)

			mainFrame = self._treeViewFrame.mainWindow.mainFrame
			collObj = self.application.objectModel.currentUser.getCollection(collectionID)
			procObjs = collObj.procedures
			procObjItems = [(item[0], item[1]) for item in procObjs.items()]

			for eachProcObj in procObjItems:
				procName = eachProcObj.procedureName
				procID = eachProcObj.procedureID
				procStr = "proc" + str(procID)

				if mainFrame.idleConfigTree.exists(procStr):
					mainFrame.idleConfigTree.item(procStr, values=[newCollectionName, procName])
				elif mainFrame.runConfigTree.exists(procStr):
					mainFrame.runConfigTree.item(procStr, value=[newCollectionName, procName])
			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()


