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
from PIL import Image, ImageTk

class ToolBarFrame(tk.Frame):
	def __init__(self, application, window):
		self._application = application
		self._window = window
		tk.Frame.__init__(self, self._window, bg='WHITE', height=25)


		addDeviceIconPath = os.path.join(self._application._imageDirectory,"addDevice.png")
		self.addDeviceImg = Image.open(addDeviceIconPath)
		self.addDeviceImg = self.addDeviceImg.resize((25,25))
		addDeviceImage = ImageTk.PhotoImage(self.addDeviceImg)
		addDeviceButton = tk.Button(self, image=addDeviceImage, relief="flat")
		addDeviceButton.image = addDeviceImage
		addDeviceButton.pack(side="left", padx=1, pady=1)
		addDeviceButton.configure(command= self._window.openNewDeviceDialog)
		ToolTip(addDeviceButton, "Add Device")

		addCollectionIconPath = os.path.join(self._application._imageDirectory, "addCollection.png")
		self.addCollectionImg = Image.open(addCollectionIconPath)
		self.addCollectionImg = self.addCollectionImg.resize((25,25))
		addCollectionImage = ImageTk.PhotoImage(self.addCollectionImg)
		addCollectionButton = tk.Button(self, image=addCollectionImage, relief="flat")
		addCollectionButton.image = addCollectionImage
		addCollectionButton.pack(side="left", padx=1, pady=1)
		addCollectionButton.configure(command= self._window.openNewCollectionDialog)
		ToolTip(addCollectionButton, "Add Collection")


		updateConfigFileIconPath = os.path.join(self._application._imageDirectory, "save.png")
		self.updateConfigFileImg = Image.open(updateConfigFileIconPath)
		self.updateConfigFileImg = self.updateConfigFileImg.resize((25,25))
		updateConfigFileImage = ImageTk.PhotoImage(self.updateConfigFileImg)
		updateConfigFileButton = tk.Button(self, image=updateConfigFileImage, relief="flat")
		updateConfigFileButton.image = updateConfigFileImage
		updateConfigFileButton.pack(side="left", padx=1, pady=1)
		updateConfigFileButton.configure(command= self._window.updateConfigFile)
		ToolTip(updateConfigFileButton, "Update Configuration File")


		loadRunConfigIconPath = os.path.join(self._application._imageDirectory, "loadRunConfig.png")
		self.loadRunConfigImg = Image.open(loadRunConfigIconPath)
		self.loadRunConfigImg = self.loadRunConfigImg.resize((25,25))
		loadRunConfigImage = ImageTk.PhotoImage(self.loadRunConfigImg)
		loadRunConfigButton = tk.Button(self, image=loadRunConfigImage, relief="flat")
		loadRunConfigButton.image = loadRunConfigImage
		loadRunConfigButton.pack(side="left", padx=1, pady=1)
		loadRunConfigButton.configure(command= self._window.loadRunConfiguration)
		ToolTip(loadRunConfigButton, "Load Run Configuration")


		saveRunConfigIconPath = os.path.join(self._application._imageDirectory, "saveRunConfig.png")
		self.saveRunConfigImg = Image.open(saveRunConfigIconPath)
		self.saveRunConfigImg = self.saveRunConfigImg.resize((25,25))
		saveRunConfigImage = ImageTk.PhotoImage(self.saveRunConfigImg)
		saveRunConfigButton = tk.Button(self, image=saveRunConfigImage, relief="flat")
		saveRunConfigButton.image = saveRunConfigImage
		saveRunConfigButton.pack(side="left", padx=1, pady=1)
		saveRunConfigButton.configure(command= self._window.saveRunConfiguration)
		ToolTip(saveRunConfigButton, "Save Run Configuration")
		

		runBackupIconPath = os.path.join(self._application._imageDirectory, "run.png")
		self.runBackupImg = Image.open(runBackupIconPath)
		self.runBackupImg = self.runBackupImg.resize((25,25))
		runBackupImage = ImageTk.PhotoImage(self.runBackupImg)
		runBackupButton = tk.Button(self, image=runBackupImage, relief="flat")
		runBackupButton.image = runBackupImage
		runBackupButton.pack(side="left", padx=1, pady=1)
		runBackupButton.configure(command= self._window.runConfiguration)
		ToolTip(runBackupButton, "Run Backup")
		


'''
ToolTip Class

Original Author: vegaseat 
Link: https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
'''
class ToolTip:
	def __init__(self, widget, text='widget_info'):
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.enter)
		self.widget.bind("<Leave>", self.close)

	def enter(self, event= None):
		x = y = 0
		x, y, cx, cy = self.widget.bbox("insert")
		x += self.widget.winfo_rootx() + 25
		y += self.widget.winfo_rooty() + 20

		self.tw = tk.Toplevel(self.widget)

		self.tw.wm_overrideredirect(True)
		self.tw.wm_geometry("+%d+%d" % (x, y))
		label = tk.Label(self.tw, text=self.text, justify='left', background='white', relief='solid', borderwidth=1)# font = ("times", "8", "normal"))
		label.pack(ipadx=1)

	def close(self, event=None):
		if self.tw:
			self.tw.destroy() 