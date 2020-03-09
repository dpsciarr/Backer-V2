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

		addCollectionIconPath = os.path.join(self._application._imageDirectory, "addCollection.png")
		self.addCollectionImg = Image.open(addCollectionIconPath)
		self.addCollectionImg = self.addCollectionImg.resize((25,25))
		addCollectionImage = ImageTk.PhotoImage(self.addCollectionImg)
		addCollectionButton = tk.Button(self, image=addCollectionImage, relief="flat")
		addCollectionButton.image = addCollectionImage
		addCollectionButton.pack(side="left", padx=1, pady=1)
		addCollectionButton.configure(command= self._window.openNewCollectionDialog)


		updateConfigFileIconPath = os.path.join(self._application._imageDirectory, "save.png")
		self.updateConfigFileImg = Image.open(updateConfigFileIconPath)
		self.updateConfigFileImg = self.updateConfigFileImg.resize((25,25))
		updateConfigFileImage = ImageTk.PhotoImage(self.updateConfigFileImg)
		updateConfigFileButton = tk.Button(self, image=updateConfigFileImage, relief="flat")
		updateConfigFileButton.image = updateConfigFileImage
		updateConfigFileButton.pack(side="left", padx=1, pady=1)
		updateConfigFileButton.configure(command= self._window.updateConfigFile)


		loadRunConfigIconPath = os.path.join(self._application._imageDirectory, "loadRunConfig.png")
		self.loadRunConfigImg = Image.open(loadRunConfigIconPath)
		self.loadRunConfigImg = self.loadRunConfigImg.resize((25,25))
		loadRunConfigImage = ImageTk.PhotoImage(self.loadRunConfigImg)
		loadRunConfigButton = tk.Button(self, image=loadRunConfigImage, relief="flat")
		loadRunConfigButton.image = loadRunConfigImage
		loadRunConfigButton.pack(side="left", padx=1, pady=1)
		loadRunConfigButton.configure(command= self._window.loadRunConfiguration)
		

		saveRunConfigIconPath = os.path.join(self._application._imageDirectory, "saveRunConfig.png")
		self.saveRunConfigImg = Image.open(saveRunConfigIconPath)
		self.saveRunConfigImg = self.saveRunConfigImg.resize((25,25))
		saveRunConfigImage = ImageTk.PhotoImage(self.saveRunConfigImg)
		saveRunConfigButton = tk.Button(self, image=saveRunConfigImage, relief="flat")
		saveRunConfigButton.image = saveRunConfigImage
		saveRunConfigButton.pack(side="left", padx=1, pady=1)
		saveRunConfigButton.configure(command= self._window.saveRunConfiguration)
		


		