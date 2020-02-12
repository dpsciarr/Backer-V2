import tkinter as tk
from tkinter import ttk

class MainFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._application = application
		self._mainWindow = mainWindow
		self._currentTreeItemID = ""
		background = 'black'
		foreground = 'white'

		tk.Frame.__init__(self, mainWindow, bg=background, width = 500)

		# DEFINING LABELS
		runConfigLabel = tk.Label(self, text="RUN CONFIGURATION", bg=background, fg=foreground, font='Helvetica 10 bold')
		idleProcsLabel = tk.Label(self, text="IDLE PROCEDURES", bg=background, fg=foreground, font='Helvetica 10 bold')
		selectedProcProps = tk.Label(self, text="SELECTED PROCEDURE PROPERTIES:", bg=background, fg=foreground, font='Helvetica 9 bold')
		procSrcLabel = tk.Label(self, text="Source Path: ", bg=background, fg=foreground)
		operationLabel = tk.Label(self, text="Operation: ", bg=background, fg=foreground)
		procDestLabel = tk.Label(self, text="Destination Path: ", bg=background, fg=foreground)

		self.currInfoSrcLabel = tk.Label(self, text=f"Info Source: ", bg=background, fg=foreground)

		self.srcDisplayLabel = tk.Label(self, text="", bg=background, fg=foreground)
		self.operationDisplayLabel = tk.Label(self, text="", bg=background, fg=foreground)
		self.destDisplayLabel = tk.Label(self, text="", bg=background, fg=foreground)
		
		# RUN CONFIG TREE
		self.runConfigTree = ttk.Treeview(self, selectmode='browse', columns=['#1','#2'])
		self.runConfigTree.bind('<<TreeviewSelect>>', self.runTreeSelectionListener)
		self.runConfigTree.heading('#1', text='Collection Name')
		self.runConfigTree.column('#1', width=150, minwidth=0)
		self.runConfigTree.heading('#2', text='Procedure Name')
		self.runConfigTree.column('#2', width=150, minwidth=0)
		self.runConfigTree.configure(show="headings")

		self.runConfigToIdleBtn = ttk.Button(self, text=">", width = 1, command= lambda : self.configToIdle())
		self.idleToRunCfgBtn = ttk.Button(self, text="<", width = 1, command= lambda : self.idleToConfig())

		#self.runBackupConfigBtn = ttk.Button(self, text="RUN CONFIGURATION", width = 25, command = lambda : self.runBackupConfiguration())

		self.idleConfigTree = ttk.Treeview(self, selectmode='browse', columns=['#1','#2'])
		self.idleConfigTree.bind('<<TreeviewSelect>>', self.idleTreeSelectionListener)
		self.idleConfigTree.heading('#1', text='Collection Name')
		self.idleConfigTree.column('#1', width=150, minwidth=0)
		self.idleConfigTree.heading('#2', text='Procedure Name')
		self.idleConfigTree.column('#2', width=150, minwidth=0)
		self.idleConfigTree.configure(show="headings")




		# PLACING LABELS
		runConfigLabel.place(x=340, y=10, anchor='nw')
		idleProcsLabel.place(x=715, y=10, anchor='nw')
		selectedProcProps.place(x=20, y=250, anchor='nw')
		procSrcLabel.place(x=20, y = 270, anchor='nw')
		operationLabel.place(x=20, y = 290, anchor='nw')
		procDestLabel.place(x=20, y = 310, anchor='nw')

		self.currInfoSrcLabel.place(x=20, y = 125, anchor = 'nw')

		self.srcDisplayLabel.place(x=125, y = 270, anchor='nw')
		self.operationDisplayLabel.place(x=125, y = 290, anchor='nw')
		self.destDisplayLabel.place(x=125, y = 310, anchor='nw')

		self.runConfigTree.place(x=255, y=35, anchor='nw')

		self.runConfigToIdleBtn.place(x = 585, y = 120, anchor='nw')
		self.idleToRunCfgBtn.place(x = 585, y = 155, anchor='nw')
		
		self.idleConfigTree.place(x=625, y=35, anchor='nw')

		self.after(50, lambda: self.setupDiagnostics())
		

	@property
	def application(self):
		return self._application
	
	@property
	def mainWindow(self):
		return self._mainWindow
	
	


	def setupDiagnostics(self):
		infoSrc = self.application.informationSource.name

		if infoSrc == "NO_SOURCE":
			self.currInfoSrcLabel['text'] = "Info Source:   No Source"
		elif infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			self.currInfoSrcLabel['text'] = "Info Source:   SQL Database"
		else:
			self.currInfoSrcLabel['text'] = "Info Source:   Configuration File"


	def populateTreeviews(self):
		currentUserObj = self.application.objectModel.currentUser

		collectionObjects = currentUserObj.collections
		collectionObjectItems = [(item[0], item[1]) for item in collectionObjects.items()]
	
		runConfigProcedures = []
		idleProcedures = []
		for collection in collectionObjectItems:
			procedureObjects = collection[1].procedures
			procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]
			for procedure in procedureObjectItems:
				procedureID = procedure[0]
				procedureObject = procedure[1]
				if procedureObject.selectedForRunConfig == True:
					runConfigProcedures.append(procedureObject)
					self.runConfigTree.insert("", "end", values=[f"{collection[1].collectionName}", f"{procedureObject.procedureName}"], iid=f"proc{procedureObject.procedureID}")
				else:
					idleProcedures.append(procedureObject)
					self.idleConfigTree.insert("", "end", values=[f"{collection[1].collectionName}", f"{procedureObject.procedureName}"], iid=f"proc{procedureObject.procedureID}")



	def runTreeSelectionListener(self, event):
		self._currentTreeItemID = self.runConfigTree.focus()

		digits = ""
		for c in self._currentTreeItemID:
			if c.isdigit():
				digits = digits + c

		collectionObjects = self.application.objectModel.currentUser.collections
		collectionObjectItems = [(item[0], item[1]) for item in collectionObjects.items()]
		for collection in collectionObjectItems:
			procedureObjects = collection[1].procedures
			procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]

			for procedure in procedureObjectItems:
				procID = procedure[0]
				procedureObject = procedure[1]
				if procID == int(digits):
					self.srcDisplayLabel['text'] = procedureObject.sourcePath
					self.destDisplayLabel['text'] = procedureObject.destinationPath
					procStr = self.application.operationObject.getOperationByNum(procedureObject.operationID)
					self.operationDisplayLabel['text'] = procStr

	def idleTreeSelectionListener(self, event):
			self._currentTreeItemID = self.idleConfigTree.focus()

			digits = ""
			for c in self._currentTreeItemID:
				if c.isdigit():
					digits = digits + c

			collectionObjects = self.application.objectModel.currentUser.collections
			collectionObjectItems = [(item[0], item[1]) for item in collectionObjects.items()]
			for collection in collectionObjectItems:
				procedureObjects = collection[1].procedures
				procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]

				for procedure in procedureObjectItems:
					procID = procedure[0]
					procedureObject = procedure[1]
					if procID == int(digits):
						self.srcDisplayLabel['text'] = procedureObject.sourcePath
						self.destDisplayLabel['text'] = procedureObject.destinationPath
						procStr = self.application.operationObject.getOperationByNum(procedureObject.operationID)
						self.operationDisplayLabel['text'] = procStr

	def configToIdle(self):
		self._currentTreeItemID = self.runConfigTree.focus()
		digits = ""
		for c in self._currentTreeItemID:
			if c.isdigit():
				digits = digits + c

			if digits != "":
				collectionObjects = self.application.objectModel.currentUser.collections
				collectionObjectItems = [(item[0], item[1]) for item in collectionObjects.items()]
			
				for collection in collectionObjectItems:
					collectionID = collection[1].collectionID
					procedureObjects = collection[1].procedures
					procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]

					for procedure in procedureObjectItems:
						procID = procedure[0]
						procObj = procedure[1]
						if procID == int(digits):
							procObj.deselectForRunConfig()
							self.application.configurationManager.updateRunConfig(procID, False)
							selectedItemDict = self.runConfigTree.item(self._currentTreeItemID)
							self.idleConfigTree.insert("", "end", iid=f"{self._currentTreeItemID}", text=selectedItemDict['text'], values=selectedItemDict['values'])
							self.runConfigTree.delete(self._currentTreeItemID)

	def idleToConfig(self):
		self._currentTreeItemID = self.idleConfigTree.focus()

		digits = ""
		for c in self._currentTreeItemID:
			if c.isdigit():
				digits = digits + c

		if digits != "":
				collectionObjects = self.application.objectModel.currentUser.collections
				collectionObjectItems = [(item[0], item[1]) for item in collectionObjects.items()]
				for collection in collectionObjectItems:
					collectionID = collection[1].collectionID
					procedureObjects = collection[1].procedures
					procedureObjectItems = [(item[0], item[1]) for item in procedureObjects.items()]

					for procedure in procedureObjectItems:
						procID = procedure[0]
						procObj = procedure[1]
						if procID == int(digits):
							procObj.selectForRunConfig()
							self.application.configurationManager.updateRunConfig(procID, True)
							selectedItemDict = self.idleConfigTree.item(self._currentTreeItemID)
							self.runConfigTree.insert("", "end", iid=f"{self._currentTreeItemID}", text=selectedItemDict['text'], values=selectedItemDict['values'])
							self.idleConfigTree.delete(self._currentTreeItemID)
