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

class OutputFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._mainWindow = mainWindow
		self._application = application

		tk.Frame.__init__(self, mainWindow, bg='RED', height=30)

		broadcaster = application.outputManager
		self.outputTextBox = broadcaster.generateTextBox(self)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=0)
		self.grid_rowconfigure(0, weight=1)

		self.outputTextBox.grid(row=0, column=0, sticky='NEWS')
		broadcaster.scrollbar.grid(row=0, column=1, sticky='NS')

		self.printLine(f"Current User: {application.currentUser}")

	@property
	def application(self):
		return self._application
	
	@property
	def mainWindow(self):
		return self._mainWindow

	def printLine(self, text):
		self.application.outputManager.broadcast(text)