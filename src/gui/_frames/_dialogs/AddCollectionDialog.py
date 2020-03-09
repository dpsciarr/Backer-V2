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

class AddCollectionDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application
		self._treeViewFrame = treeViewFrame

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Add Collection")
		self.winfo_toplevel().geometry("350x150+500+200")
		frame = tk.Frame(self, bg='white')


		collNameLabel = tk.Label(frame, text="Collection Name:", bg="white", fg="black")
		self.collNameEntry = tk.Entry(frame, width=30, borderwidth=2)
		self.addCollectionButton = tk.Button(frame, text="Add\nCollection", height=2, width=10, command = lambda : self.addCollection())
		self.closeButton = tk.Button(frame, text="Cancel", height=2, width=10, command = self.kill)

		collNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.collNameEntry.place(x=135, y=20, relx=0, rely=0, anchor='nw')

		self.addCollectionButton.place(x=30, y = 80, relx=0, rely=0, anchor='nw')
		self.closeButton.place(x=230, y=80, relx=0, rely=0, anchor='nw')



		frame.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())

	@property
	def application(self):
		return self._application

	'''
	addCollection()
	
	Handles the high-level addition of a new Collection to the system.
	'''
	def addCollection(self):
		newCollectionName = self.collNameEntry.get()
		
		infoSrc = self.application.informationSource.name
		currUser = self.application.currentUser
		currUserID = self.application.currentUserID

		#Notify User of add operation
		self.application.outputManager.broadcast(f"Attempting to add Collection {newCollectionName} . . .")

		if infoSrc == "SOURCE_DATABASE" or infoSrc == "SOURCE_DATABASE_NO_CFG":
			#Check whether the collection is already in the database for currentUser
			collectionExists = self.application.databaseOperator.queries.checkDatabaseForCollection(newCollectionName, currUserID)

			if collectionExists == True:
				self.application.outputManager.broadcast(f"   Collection {newCollectionName} already exists in database for user {currUser}. Could not add collection.")
			else:
				#Add collection to database
				collectionID = self.application.databaseOperator.queries.addCollection(newCollectionName, currUserID)

				if collectionID is not None:
					self.application.outputManager.broadcast(f"   Collection '{newCollectionName}' added to database.")

					#Add collection to object model.
					collID = self.application.objectModel.addCollectionToModel(collectionID, newCollectionName, currUserID)
					if collID is not None:
						self.application.outputManager.broadcast(f"   Collection '{newCollectionName}' added to object model.")

						#Add collection to TreeView
						self._treeViewFrame.tree.insert("collections", "end", iid=f"coll{collID}", text=f"{newCollectionName}")

		elif infoSrc == "SOURCE_CONFIG_NO_DB":
			self.application.outputManager(f"   Collection '{newCollectionName}' cannot be added to configuration. Connect to database.")
		else:
			self.application.outputManager(f"   Collection '{newCollectionName}' cannot be added to configuration. Connect to database.")
		
		#Close the window
		self.winfo_toplevel().destroy()

	'''
	kill()

	Kills Add Collection window.
	'''
	def kill(self):
		self.winfo_toplevel().destroy()