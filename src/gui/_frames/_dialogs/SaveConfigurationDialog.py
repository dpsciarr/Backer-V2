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
import sys


class SaveConfigurationDialog(tk.Tk):
	def __init__(self, applicationWindow):
		self._applicationWindow = applicationWindow
		self._json = self.applicationWindow.application.configurationManager.jsonOperator


		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Save Configuration")
		self.winfo_toplevel().geometry("300x175+300+100")
		f = tk.Frame(self, bg='white')

		saveFileNameLabel = tk.Label(f, text="Choose a name for your Run Configuration:", bg="white", fg="black")
		self.saveFileEntry = tk.Entry(f, width=40, borderwidth=2)
		self.saveButton = tk.Button(f, text="Save", height=2, width = 10, command= lambda : self.save())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		saveFileNameLabel.place(x=30, y=20, relx=0, rely=0, anchor='nw')
		self.saveFileEntry.place(x=30, y=60, relx=0, rely=0, anchor='nw')
		self.saveButton.place(x=25, y = 100, anchor='nw')
		self.closeButton.place(x=200, y = 100, anchor='nw')

		f.pack(fill='both', expand=1)

		self.after(500, lambda: self.focus_force())

	@property
	def applicationWindow(self):
		return self._applicationWindow

	def kill(self):
		self.winfo_toplevel().destroy()

	def save(self):
		self.applicationWindow.application.outputManager.broadcast("Saving Run Configuration . . .")
		saveFileName = self.saveFileEntry.get()

		if saveFileName != "":
			runConfigDict = self.applicationWindow.application.configurationManager.runConfigurationDict

			runConfigFolder = os.path.join(self.applicationWindow.application.configDirectory, "runcfgs")
			runConfigFile = os.path.join(runConfigFolder, saveFileName + ".rcf")

			try:
				if os.path.exists(runConfigFile) == False:
					fileOpen = open(runConfigFile, 'w+')
					fileOpen.close()
				else:
					self.applicationWindow.application.outputManager.broadcast(f"   File {saveFileName} already exists in path.")
			

			except Exception as e:
				print(e)

			if os.path.exists(runConfigFile):
				if os.path.isfile(runConfigFile):
					with open(runConfigFile, 'w') as fp:
						self._json.dump(runConfigDict, fp)
				else:
					self.applicationWindow.application.outputManager.broadcast(f"   {runConfigFile} is not a file...")
			else:
				self.applicationWindow.application.outputManager.broadcast("   File not detected...")

			self.applicationWindow.application.outputManager.broadcast("   Run Configuration saved as:")
			self.applicationWindow.application.outputManager.broadcast(f"   {runConfigFile}")

			self.winfo_toplevel().destroy()
		else:
			self.applicationWindow.application.outputManager.broadcast(f"   Please specify a name for the configuration file...")

			
