import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from os import sep

class EditProcedureDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame
		self._currentUserObject = self.application.objectModel.currentUser

		operations = []
		for i in range(len(self.application.operationObject.operationsNumToString)):
			operations.append(self.application.operationObject.getOperationByNum(i))

		procedureSelection = self._treeViewFrame.tree.selection()
		collectionDigits = ""
		procedureDigits = ""
		self.selectedProcedureName = ""
		self.procedureIIDfromTree = ""
		self.collectionIID = ""
		self.collectionObject = ""
		if len(procedureSelection) > 0:
			self.procedureIIDfromTree = procedureSelection[0]
			for j in self.procedureIIDfromTree:
				if j.isdigit():
					procedureDigits = procedureDigits + j

			self.collectionIID = self._treeViewFrame.tree.parent(self.procedureIIDfromTree)
			for i in self.collectionIID:
				if i.isdigit():
					collectionDigits = collectionDigits + i

			self.collectionObject = self._currentUserObject.getCollection(int(collectionDigits))
			self.procedureObject = self.collectionObject.getProcedure(int(procedureDigits))
			self.selectedProcedureName = self.procedureObject.procedureName

		procedureObjects = self.collectionObject.procedures
		procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]
		procedureNames = []
		procedureIDs = []
		self.procedureDict = {}
		self.procedureDictReversed = {}
		if len(procedureObjectItems) > 0:
			for eachProcedure in procedureObjectItems:
				procedureItemName = eachProcedure[1].procedureName
				procedureItemID = eachProcedure[1].procedureID
				procedureNames.append(procedureItemName)
				procedureIDs.append(procedureItemID)
			self.procedureDict = dict(zip(procedureIDs, procedureNames))
			self.procedureDictReversed = {v: k for k,v in self.procedureDict.items()}

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Edit Procedure")
		self.winfo_toplevel().geometry("600x250+400+200")
		f = tk.Frame(self, bg='white')

		procNameLabel = tk.Label(f, text="Procedure Name:", bg="white", fg="black")
		procOpLabel = tk.Label(f, text="Operation:", bg='white', fg='black')
		procSourceLabel = tk.Label(f, text="Source:", bg='white', fg='black')
		procDestLabel = tk.Label(f, text="Destination:", bg='white', fg='black')
		self.procNameEntry = tk.Entry(f, width=30, borderwidth=2)
		self.procNameEntry.insert(0, self.procedureObject.procedureName)
		self.opsListBox = ttk.Combobox(f, values = operations, state='readonly')
		self.currOpCode = self.application.operationObject.getOperationByNum(self.procedureObject.operationID)
		self.opsListBox.set(self.currOpCode)
		self.procSourceEntry = tk.Entry(f, width=70, borderwidth=2)
		self.procSourceEntry.insert(0, self.procedureObject.sourcePath)
		self.procDestEntry = tk.Entry(f, width=70, borderwidth=2)
		self.procDestEntry.insert(0, self.procedureObject.destinationPath)
		self.sourceFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openSrcBrowser(self.opsListBox.get(), self.procSourceEntry))
		self.destFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openDestBrowser(self.opsListBox.get(), self.procDestEntry))
		self.editProcedureButton = tk.Button(f, text="Edit\nProcedure", height=2, width=10, command = lambda : self.editProcedure())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		procNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		procOpLabel.place(x=30, y=55, relx=0, rely=0, anchor='nw')
		procSourceLabel.place(x=30, y=90, relx=0, rely=0, anchor='nw')
		procDestLabel.place(x=30, y=125, relx=0, rely=0, anchor='nw')
		self.procNameEntry.place(x=135, y=20, relx=0, rely=0, anchor='nw')
		self.opsListBox.place(x=135, y=55, relx=0, rely=0, anchor='nw')
		self.opsListBox.config(width=30)
		self.procSourceEntry.place(x=135, y=90, relx=0, rely=0, anchor='nw')
		self.procDestEntry.place(x=135, y=125, relx=0, rely=0, anchor='nw')
		self.sourceFileBrowserButton.place(x=555, y=88, relx=0, rely=0, anchor='nw')
		self.destFileBrowserButton.place(x=555, y=123, relx=0, rely=0, anchor='nw')
		self.editProcedureButton.place(x=160, y=200, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=360, y=200, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())


	@property
	def application(self):
		return self._application

	def openSrcBrowser(self, operation, entrybox):
		directoryName = ""
		if "Single File" in operation:
			directoryName = filedialog.askopenfilename(initialdir="/", title="Select File")
		else:
			directoryName = filedialog.askdirectory(initialdir="/", title="Select Folder")
		self.focus_force()
		self.grab_set()
		entrybox.delete(0, 'end')
		entrybox.insert(0, directoryName)

	def openDestBrowser(self, operation, entrybox):
		directoryName = filedialog.askdirectory(initialdir="/", title = "Select Folder")
		self.focus_force()
		self.grab_set()
		entrybox.delete(0, 'end')
		entrybox.insert(0, directoryName)

	def editProcedure(self):
		procedureID = self.procedureDictReversed[self.selectedProcedureName]
		infoSrc = self.application.informationSource.name
		currentUser = self.application.currentUser
		currentUserID = self.application.currentUserID

		#notify users of editing operation
		self.application.outputManager.broadcast(f"Attempting to edit procedure {self.selectedProcedureName}.")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			currProcName = self.procedureObject.procedureName
			currProcSrc = self.procedureObject.sourcePath
			currProcDest = self.procedureObject.destinationPath
			currProcOpCode = self.currOpCode #string representation

			enteredProcName = self.procNameEntry.get()
			enteredProcSrc = self.procSourceEntry.get()
			enteredProcDest = self.procDestEntry.get()
			enteredOpCode = self.opsListBox.get()

			enteredProcSrc = enteredProcSrc.replace(sep, '/')
			enteredProcDest = enteredProcDest.replace(sep, '/')

			procNameToSave = currProcName
			procNameChanged = False
			if currProcName != enteredProcName:
				procNameToSave = enteredProcName
				procNameChanged = True

			procSrcToSave = currProcSrc
			procSrcChanged = False
			if currProcSrc != enteredProcSrc:
				procSrcToSave = enteredProcSrc
				procSrcChanged = True

			procDestToSave = currProcDest
			procDestChanged = False
			if currProcDest != enteredProcDest:
				procDestToSave = enteredProcDest
				procDestChanged = True

			procOpCodeToSave = currProcOpCode
			procOpCodeChanged = False
			if currProcOpCode != enteredOpCode:
				procOpCodeToSave = enteredOpCode
				procOpCodeChanged = True

			procOpCodeToSave = self.application.operationObject.getOperationByString(procOpCodeToSave)

			if procNameChanged:
				#Update name in database
				self.application.databaseOperator.queries.updateProcedureName(procNameToSave, procedureID)
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} name changed to {procNameToSave} in database.")

				#Update name in object model
				self.procedureObject.procedureName = procNameToSave
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} name changed to {procNameToSave} in Object Model.")

				#Update Tree
				self._treeViewFrame.tree.item(self.procedureIIDfromTree, text = procNameToSave)

				if self._treeViewFrame.mainWindow.mainFrame.idleConfigTree.exists(self.procedureIIDfromTree):
					self._treeViewFrame.mainWindow.mainFrame.idleConfigTree.item(self.procedureIIDfromTree, values = [self.collectionObject.collectionName, procNameToSave])
				elif self._treeViewFrame.mainWindow.mainFrame.runConfigTree.exists(self.procedureIIDfromTree):
					self._treeViewFrame.mainWindow.mainFrame.runConfigTree.item(self.procedureIIDfromTree, values= [self.collectionObject.collectionName, procNameToSave])
					

			if procSrcChanged:
				#Update src in database
				self.application.databaseOperator.queries.updateProcedureSource(procSrcToSave, procedureID)
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} source changed in database to: \n{procSrcToSave}")

				#Update src in object model
				self.procedureObject.sourcePath = procSrcToSave
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} source changed in Object Model to: \n{procSrcToSave}")

			if procDestChanged:
				#Update dest in database
				self.application.databaseOperator.queries.updateProcedureDestination(procDestToSave, procedureID)
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} destination changed in database to: \n{procDestToSave}")

				#Update dest in object model
				self.procedureObject.destinationPath = procDestToSave
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} destination changed in Object Model to: \n{procDestToSave}")


			if procOpCodeChanged:
				#Update op code in database
				self.application.databaseOperator.queries.updateProcedureOpCode(procOpCodeToSave, procedureID)
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} operation code changed in database to {procOpCodeToSave}.")

				#Update op code in object model
				self.procedureObject.operationID = procOpCodeToSave
				self.application.outputManager.broadcast(f"   Procedure {self.selectedProcedureName} operation code changed in Object Model to {procOpCodeToSave}.")

			self.winfo_toplevel().destroy()

	def kill(self):
		self.winfo_toplevel().destroy()