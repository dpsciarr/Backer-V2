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

class DeleteCollectionDialog(tk.Tk):
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
		self.winfo_toplevel().title("Delete Collection")
		self.winfo_toplevel().geometry("350x150+500+200")
		f = tk.Frame(self, bg='white')

		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedCollectionName}?", bg="white", fg="black")
		self.deleteCollButton = tk.Button(f, text="Delete\nCollection", height=2, width=10, command = lambda : self.deleteCollection())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteCollButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)
		self.after(500, lambda: self.focus_force())

	@property
	def application(self):
		return self._application

	def deleteCollection(self):
		collectionID = self.collectionDictReversed[self.selectedCollectionName]
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID
		collectionObject = self._currentUserObject.getCollection(int(collectionID))
		procedureObjects = collectionObject.procedures
		procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]

		#Notify user of deletion attempt.
		self.application.outputManager.broadcast(f"Attempting to delete collection {self.selectedCollectionName}.")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			mainFrame = self._treeViewFrame.mainWindow.mainFrame
			#Remove procedures from treeviews and database:
			for eachProcObject in procedureObjectItems:
				procName = eachProcObject[1].procedureName
				procID = eachProcObject[1].procedureID
				procStr = "proc" + str(procID)

				if mainFrame.idleConfigTree.exists(procStr):
					mainFrame.idleConfigTree.delete(procStr)
				elif mainFrame.runConfigTree.exists(procStr):
					mainFrame.runConfigTree.delete(procStr)

				self.application.databaseOperator.queries.deleteProcedure(procID)


			#Remove collection from database
			self.application.databaseOperator.queries.deleteCollection(collectionID)

			self.application.outputManager.broadcast(f"   Collection {self.selectedCollectionName} has been deleted from the database.")

			#Remove collection from object model
			self._currentUserObject.removeCollection(collectionID)
			result = ""
			try:
				result = self._currentUserObject.getCollection(collectionID)
			except KeyError:
				self.application.outputManager.broadcast(f"   Collection {self.selectedCollectionName} deleted from Object Model.")
				self._treeViewFrame.tree.delete(self.iidFromTree)

			if result == None:
				self.application.outputManager.broadcast(f"   Collection {self.selectedCollectionName} deleted from Object Model.")
				self._treeViewFrame.tree.delete(self.iidFromTree)

				for eachProcObject in procedureObjectItems:
					procName = eachProcObject[1].procedureName
					procID = eachProcObject[1].procedureID
					procStr = "proc" + str(procID)

					if mainFrame.idleConfigTree.exists(procStr):
						mainFrame.idleConfigTree.delete(procStr)
					elif mainFrame.runConfigTree.exists(procStr):
						mainFrame.runConfigTree.delete(procStr)

		self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()
