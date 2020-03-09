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
import os
from tkinter import ttk

class LoadConfigurationDialog(tk.Tk):
	def __init__(self, applicationWindow):
		self._applicationWindow = applicationWindow
		self._json = self.applicationWindow.application.configurationManager.jsonOperator

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Load Configuration")
		self.winfo_toplevel().geometry("260x175+300+100")
		frame = tk.Frame(self, bg='white')

		runConfigPath = os.path.join(self.applicationWindow.application.configDirectory, "runcfgs")

		
		rcf_files = [f for f in os.listdir(runConfigPath) if f.lower().endswith('.rcf')]

		if len(rcf_files) == 0:
			rcf_files.append("")

		
		loadFileNameLabel = tk.Label(frame, text="Choose a Run Configuration to load:", bg="white", fg="black")
		self.loadFileList = ttk.Combobox(frame, values = rcf_files, state = 'readonly')
		self.loadFileList.set(rcf_files[0])
		
		self.loadFileButton = tk.Button(frame, text = "Load", height = 2, width = 10, command = lambda : self.load())
		self.closeButton = tk.Button(frame, text="Cancel", height=2, width=10, command = self.kill)

		
		loadFileNameLabel.place(x = 30, y = 20, relx = 0, rely = 0, anchor = 'nw')
		self.loadFileList.place(x = 30, y = 60, relx = 0, rely = 0, anchor = 'nw')
		self.loadFileButton.place(x = 25, y = 100, anchor = 'nw')
		self.closeButton.place(x = 150, y = 100, anchor = 'nw')

		self.loadFileList.config(width = 30)

		frame.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())

	@property
	def applicationWindow(self):
		return self._applicationWindow
	
	def load(self):
		self.applicationWindow.application.outputManager.broadcast("Loading run configuration . . .")
		currentUserObj = self.applicationWindow.application.objectModel.currentUser
		configManager = self.applicationWindow.application.configurationManager

		fileToLoad = self.loadFileList.get()
		if fileToLoad != "":
			loadFilePath = os.path.join(self.applicationWindow.application.configDirectory, f"runcfgs\\{fileToLoad}")
			self.applicationWindow.application.outputManager.broadcast(f"   Loading {fileToLoad} from path:")
			self.applicationWindow.application.outputManager.broadcast(f"   {loadFilePath}")

			cfgData = {}
			with open(loadFilePath, 'r') as lfp:
				cfgData = self._json.load(lfp)

			#Get keys in object model
			keyArrOBJ = [int(k) for k, v in configManager.runConfigurationDict.items()]

			#Get keys in run config file
			keyArrCFG = [int(k) for k,v in cfgData.items()]

			configOnlyProcedures = list(set(keyArrCFG).difference(keyArrOBJ))
			objectModelOnlyProcedures = list(set(keyArrOBJ).difference(keyArrCFG))

			if len(configOnlyProcedures) != 0 and len(objectModelOnlyProcedures) == 0:
				self.applicationWindow.application.outputManager.broadcast(f"   Cannot load file {fileToLoad}, there are procedures in the config file that are not in the object model.")
			elif len(configOnlyProcedures) == 0 and len(objectModelOnlyProcedures) != 0:
				self.applicationWindow.application.outputManager.broadcast(f"   Cannot load file {fileToLoad}, there are procedures in the object model that are not in the config file.")
			elif len(configOnlyProcedures) != 0 and len(objectModelOnlyProcedures) != 0:
				self.applicationWindow.application.outputManager.broadcast(f"   Cannot load file {fileToLoad}, too many differences between object model and configuration file.")
			elif len(configOnlyProcedures) == 0 and len(objectModelOnlyProcedures) == 0:
				newDict = {}
				newDict = {int(k): v for k, v in cfgData.items()}
				self.applicationWindow.application.configurationManager.runConfigurationDict = newDict

				collectionObjects = currentUserObj.collections
				newDictList = [(int(k), v) for k, v in newDict.items()]

				for configSetting in newDictList:
					procID = configSetting[0]
					procConfigSetting = configSetting[1]

					for collKey in collectionObjects:
						procedureObjects = collectionObjects[collKey].procedures
						procObjItems = [(item[0], item[1]) for item in procedureObjects.items()]

						for procedure in procObjItems:
							if int(procedure[0]) == int(procID):
								if procConfigSetting == True:
									collectionObjects[collKey].getProcedure(int(procedure[0])).selectForRunConfig()
								else:
									collectionObjects[collKey].getProcedure(int(procedure[0])).deselectForRunConfig()

				#Reset Tree
				self.applicationWindow.mainFrame.runConfigTree.delete(*self.applicationWindow.mainFrame.runConfigTree.get_children())
				self.applicationWindow.mainFrame.idleConfigTree.delete(*self.applicationWindow.mainFrame.idleConfigTree.get_children())
				self.applicationWindow.mainFrame.populateTreeviews()

				self.applicationWindow.application.outputManager.broadcast("   Success! Run configuration loaded into object model.")
			
			self.winfo_toplevel().destroy()

		else:
			self.applicationWindow.application.outputManager.broadcast("   No load files to choose from . . .")


	def kill(self):
		self.winfo_toplevel().destroy()

