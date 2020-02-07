def buildTree(self, objModel):
		userObj = objModel.getCurrentUserObject()
		#print(userObj)
		self.tree = ttk.Treeview(self, selectmode='browse')

		self.tree.bind("<Button-3>", self.popupMenu)
		self.tree.bind('<<TreeviewSelect>>', self.tree_click_event)

		#self.tree.bind("<Double-1>", self.OnDoubleClick)
		self.tree.heading('#0', text='Configuration Tree')
		self.tree.insert("", "end", iid="user", text=f"User: {userObj.getName()}")

		self.tree.insert("user", "end", iid="devices", text="Devices")
		devDict = userObj.getDevices()
		for devKey in devDict:
			devID = devDict[devKey].getID()
			devName = devDict[devKey].getName()
			self.tree.insert("devices","end", text=f"Device: {devName}", iid=f"dev{devID}")

			drvDict = devDict[devKey].getDrives()
			for (key, val) in drvDict.items():
				drvID = val.getID()
				drvName = val.getName()
				self.tree.insert(f"dev{devID}", "end", text=f"Drive: {drvName}", iid=f"drv{drvID}")

		self.tree.insert("user", "end", iid="collections", text="Collections")
		collDict = userObj.getCollections()
		for collKey in collDict:
			collID = collDict[collKey].getID()
			collName = collDict[collKey].getName()
			self.tree.insert("collections", "end", text=f"Collection: {collName}", iid=f"coll{collID}")
			
			procDict = collDict[collKey].getProcedures()
			for (key, val) in procDict.items():
				procID = val.getID()
				procName = val.getName()
				self.tree.insert(f"coll{collID}", "end", text=f"Procedure: {procName}", iid=f"proc{procID}")

		self.tree.pack(fill = 'both', expand = True)
