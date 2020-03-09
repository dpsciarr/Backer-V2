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

class DeleteProcedureDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame

		#Get user object.
		self._currentUserObject = self.application.objectModel.currentUser

		procSel = self._treeViewFrame.tree.selection()
		collectionDigits = ""
		procedureDigits = ""
		self.selectedProcedureName = ""
		self.procedureIIDfromTree = ""
		self.collectionIID = ""
		self.collectionObject = ""
		if len(procSel) > 0:
			self.procedureIIDfromTree = procSel[0]
			for j in self.procedureIIDfromTree:
				if j.isdigit():
					procedureDigits = procedureDigits + j

			self.collectionIID = self._treeViewFrame.tree.parent(self.procedureIIDfromTree)
			for i in self.collectionIID:
				if i.isdigit():
					collectionDigits = collectionDigits + i
			self.collectionObject = self._currentUserObject.getCollection(int(collectionDigits))
			procedureObject = self.collectionObject.getProcedure(int(procedureDigits))
			self.selectedProcName = procedureObject.procedureName

		procedureObjects = self.collectionObject.procedures
		procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]
		procNames = []
		procIDs = []
		self.procDict = {}
		self.procDictReversed = {}
		if len(procedureObjectItems) > 0:
			for eachProcedure in procedureObjectItems:
				procItemName = eachProcedure[1].procedureName
				procItemID = eachProcedure[1].procedureID
				procNames.append(procItemName)
				procIDs.append(procItemID)
			self.procDict = dict(zip(procIDs, procNames))
			self.procDictReversed = {v: k for k, v in self.procDict.items()}

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Procedure")
		self.winfo_toplevel().geometry("350x150+500+200")
		f = tk.Frame(self, bg='white')

		firstLabel = tk.Label(f, text=f"Are you sure you want to delete: {self.selectedProcName}?", bg="white", fg="black")
		self.deleteProcButton = tk.Button(f, text="Delete\nProcedure", height=2, width=10, command = lambda : self.deleteProcedure())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		firstLabel.place(x=65, y=20, relx=0, rely=0, anchor='nw')
		self.deleteProcButton.place(x=30, y = 90, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=90, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)


	@property
	def application(self):
		return self._application

	def deleteProcedure(self):
		procID = self.procDictReversed[self.selectedProcName]
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID

		self.application.outputManager.broadcast(f"Attempting to delete procedure {self.selectedProcName} . . .")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Remove procedure from database.
			self.application.databaseOperator.queries.deleteProcedure(procID)

			self.application.outputManager.broadcast(f"   Procedure {self.selectedProcName} deleted from database.")

			#Remove from Object Model
			self.collectionObject.removeProcedure(procID)
			result = ""
			try:
				result = self.collectionObject.getProcedure(procID)
			except KeyError:
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcName} deleted from Object Model.")
				
				if self._treeViewFrame.mainWindow.mainFrame.idleConfigTree.exists(self.procedureIIDfromTree):
					self._treeViewFrame.mainWindow.mainFrame.idleConfigTree.delete(self.procedureIIDfromTree)
				elif self._treeViewFrame.mainWindow.mainFrame.runConfigTree.exists(self.procedureIIDfromTree):
					self._treeViewFrame.mainWindow.mainFrame.runConfigTree.delete(self.procedureIIDfromTree)
					

				self._treeViewFrame.tree.delete(self.procedureIIDfromTree)

			if result == None:
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcName} deleted from Object Model.")
				self._treeViewFrame.tree.delete(self.procedureIIDfromTree)

				if self._treeViewFrame.mainWindow.mainFrame.idleConfigTree.exists(self.procedureIIDfromTree):
					self._treeViewFrame.mainWindow.mainFrame.idleConfigTree.delete(self.procedureIIDfromTree)
				elif self._treeViewFrame.mainWindow.mainFrame.runConfigTree.exists(self.procedureIIDfromTree):
					self._treeViewFrame.mainWindow.mainFrame.runConfigTree.delete(self.procedureIIDfromTree)
					
			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()