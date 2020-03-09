import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from os import sep

class AddProcedureDialog(tk.Toplevel):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame
		self._operationObject = self.application.operationObject
		self._currentUser = self.application.objectModel.currentUser

		#Get dictionary of all collections belonging to current user
		collectionObjects = self._currentUser.collections

		#Obtain a dictionary with the key as the collection ID and value as the collection Name
		collectionObjItems = [(item[0],item[1]) for item in collectionObjects.items()]
		collectionNames = []
		collectionIDs = []
		self.collectionDict = {}
		self.collectionDictReversed = {}
		if len(collectionObjItems) > 0:
			for eachCollection in collectionObjItems:
				collItemName = eachCollection[1].collectionName
				collItemID = eachCollection[1].collectionID
				collectionNames.append(collItemName)
				collectionIDs.append(collItemID)
			self.collectionDict = dict(zip(collectionIDs, collectionNames))
			self.collectionDictReversed = {v: k for k, v in self.collectionDict.items()}

		currentlySelected = self._treeViewFrame.tree.selection()
		digits = ""
		selectedCollectionName = ""
		self.iidFromTree = ""
		if len(currentlySelected) > 0:
			self.iidFromTree = currentlySelected[0]
			for i in self.iidFromTree:
				if i.isdigit():
					digits = digits + i
			selectedCollectionName = self.collectionDict[int(digits)]



		tk.Toplevel.__init__(self)
		self.title("Add Procedure")
		self.geometry("600x250+400+200")
		#tk.Tk.__init__(self)
		#self.winfo_toplevel().title("Add Procedure")
		#self.winfo_toplevel().geometry("600x250+400+200")
		f = tk.Frame(self, bg='white')

		#Labels
		procNameLabel = tk.Label(f, text="Procedure Name:", bg="white", fg="black")
		procOpLabel = tk.Label(f, text="Operation:", bg='white', fg='black')
		procSourceLabel = tk.Label(f, text="Source:", bg='white', fg='black')
		procDestLabel = tk.Label(f, text="Destination:", bg='white', fg='black')
		procAssociatedCollectionLabel = tk.Label(f, text="Parent Collection:", bg="white", fg="black")
		procAppendLabel = tk.Label(f, text="Suffix:", bg='white', fg='black')
		
		#Entry Boxes
		self.procNameEntry = tk.Entry(f, width=30, borderwidth=2)
		self.procSourceEntry = tk.Entry(f, width=70, borderwidth=2)
		self.procDestEntry = tk.Entry(f, width=70, borderwidth=2)

		#Comboboxes
		procOperations = []
		for i in range(14):
			procOperations.append(self._operationObject.getOperationByNum(i))
		self.opsListBox = ttk.Combobox(f, values = procOperations)
		self.opsListBox.set(procOperations[0])

		self.collectionList = ttk.Combobox(f, values = collectionNames, state = 'readonly')
		if selectedCollectionName in collectionNames:
			self.collectionList.set(selectedCollectionName)
		else:
			self.collectionList.set(collectionNames[0])

		#Operation Code Name Appendage List
		self.multiFileValues = ["Basic", "Date", "Date-Time", "Time-Stamp"]
		self.singleFileValues = ["Basic", "Date", "Date-Time", "Time-Stamp", "Revision"]
		self.appendageList = ttk.Combobox(f, values = self.multiFileValues, state = 'readonly')
		self.appendageList.set(self.multiFileValues[0])

		#Add Buttons
		self.addProcedureButton = tk.Button(f, text="Add\nProcedure", height=2, width=10, command = lambda : self.addProcedure())
		self.sourceFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openSrcBrowser(self.opsListBox.get(), self.procSourceEntry))
		self.destFileBrowserButton = tk.Button(f, text="...", height=1, width=1, command = lambda : self.openDestBrowser(self.opsListBox.get(), self.procDestEntry))
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		#Place Labels
		procNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		procOpLabel.place(x=30, y=55, relx=0, rely=0, anchor='nw')
		procSourceLabel.place(x=30, y=90, relx=0, rely=0, anchor='nw')
		procDestLabel.place(x=30, y=125, relx=0, rely=0, anchor='nw')
		procAssociatedCollectionLabel.place(x=30, y = 160, relx = 0, rely = 0, anchor='nw')
		procAppendLabel.place(x=390, y=55, relx=0,rely=0,anchor='nw')
		
		#Place and configure Comboboxes
		self.opsListBox.place(x=135, y=55, relx=0, rely=0, anchor='nw')
		self.opsListBox.config(width=30)
		self.appendageList.place(x=440, y = 55, relx = 0, rely = 0, anchor='nw')
		self.appendageList.config(width=15)
		self.collectionList.place(x=135, y=160, relx=0, rely=0, anchor='nw')
		self.opsListBox.bind('<<ComboboxSelected>>', self.callback)
		self.opsListBox.config(state = 'readonly')
		self.collectionList.config(width = 50)

		#Place Entries
		self.procNameEntry.place(x=135, y=20, relx=0, rely=0, anchor='nw')
		self.procSourceEntry.place(x=135, y=90, relx=0, rely=0, anchor='nw')
		self.procDestEntry.place(x=135, y=125, relx=0, rely=0, anchor='nw')

		#Place Buttons
		self.sourceFileBrowserButton.place(x=555, y=88, relx=0, rely=0, anchor='nw')
		self.destFileBrowserButton.place(x=555, y=123, relx=0, rely=0, anchor='nw')
		self.addProcedureButton.place(x=160, y=200, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=360, y=200, relx=0, rely=0, anchor='nw')

		f.pack(fill='both', expand=1)
		self.after(500, lambda: self.focus_force())


	@property
	def application(self):
		return self._application

	def addProcedure(self):
		newProcedureName = self.procNameEntry.get()

		newProcedureOpCode = self.opsListBox.get()
		statedAppendage = self.appendageList.get()
		statedOpCode = self.opsListBox.get()
		if (self.appendageList.state()[0] == 'readonly' or self.appendageList.state()[0] == 'focus') and statedAppendage != "Basic":
			statedOpCode = statedOpCode + " (" + str(statedAppendage) + ")"
			newProcedureOpCode = statedOpCode

		procOpCodeID = int(self.application.operationObject.getOperationByString(newProcedureOpCode))
		newProcedureSource = self.procSourceEntry.get().replace(sep, '/')
		newProcedureDest = self.procDestEntry.get().replace(sep, '/')
		collectionName = self.collectionList.get()
		collectionID = self.collectionDictReversed[collectionName]
		infoSrc = self.application.informationSource.name
		currentUserObject = self._currentUser
		currentUserID = self.application.currentUserID
		currentUsername = self.application.currentUser

		self.application.outputManager.broadcast(f"Attempting to add Procedure {newProcedureName}")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Make sure procedure does not exist for this collection ID
			if self.application.databaseOperator.queries.checkDatabaseForProcedure(newProcedureName, collectionID):
				#Notify user the procedure already exists.
				self.application.outputManager.broadcast(f"   Procedure {newProcedureName} already exists for collection {collectionName}. Procedure not added.")
			else:
				#Add procedure to database
				procedureID = self.application.databaseOperator.queries.addProcedure(newProcedureName, newProcedureSource, newProcedureDest, collectionID, procOpCodeID)

				if procedureID is not None:
					#Notify user the procedure has been added to the database
					self.application.outputManager.broadcast(f"   Procedure {newProcedureName} has been added to database.")

					#Add to object model
					procID = self.application.objectModel.addProcedureToModel(procedureID, newProcedureName, newProcedureSource, newProcedureDest, collectionID, procOpCodeID)

					if procID is not None:
						self.application.outputManager.broadcast(f"   Procedure {newProcedureName} has been added to the object model.")

						self._treeViewFrame.mainWindow.mainFrame.idleConfigTree.insert("", "end", iid= f"proc{procID}", values = [f"{collectionName}", f"{newProcedureName}"])

						#Add Procedure to Idle TreeView
						self._treeViewFrame.tree.insert(self.iidFromTree, "end", iid=f"proc{procedureID}", text=f"{newProcedureName}")

						#Add procedure to run configuration dict
						self._treeViewFrame.application.configurationManager.updateRunConfig(procID, False)

		elif infoSrc == "SOURCE_CONFIG_NO_DB":
			self.application.outputManager(f"   Procedure '{newProcedureName}' cannot be added to configuration. Connect to database.")
		else:
			self.application.outputManager(f"   Procedure '{newProcedureName}' cannot be added to configuration. Connect to database.")
		
		#Close the window
		self.winfo_toplevel().destroy()

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

	def callback(self, event):
		self.procSourceEntry.delete(0, 'end')
		self.procDestEntry.delete(0, 'end')

		currOpSelected = self.opsListBox.get()

		if "Single File" in currOpSelected and "Overwrite" not in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.singleFileValues)
			self.appendageList.set(self.singleFileValues[0])
		elif "File Copy New" in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])
		elif "File Migrate New" in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])
		elif "Single Folder" in currOpSelected and "Overwrite" not in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.singleFileValues)
			self.appendageList.set(self.singleFileValues[0])
		elif "Folder Copy New" in currOpSelected:
			self.appendageList.config(state='readonly')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])
		else:
			self.appendageList.config(state='disabled')
			self.appendageList.config(values=self.multiFileValues)
			self.appendageList.set(self.multiFileValues[0])


	def kill(self):
		self.winfo_toplevel().destroy()
