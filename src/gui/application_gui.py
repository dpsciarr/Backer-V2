from tkinter import ttk
import sys
import os.path
import tkinter as tk

srcDir = os.path.dirname(__file__)
frameDir = os.path.join(srcDir, "_frames")
dialogsDir = os.path.join(frameDir, "_dialogs")

sys.path.append(frameDir)

from TreeViewFrame import TreeViewFrame
from MainFrame import MainFrame
from OutputFrame import OutputFrame
from ToolBarFrame import ToolBarFrame

sys.path.remove(frameDir)

sys.path.append(dialogsDir)

from AddCollectionDialog import AddCollectionDialog
from AddDeviceDialog import AddDeviceDialog
from SaveConfigurationDialog import SaveConfigurationDialog
from LoadConfigurationDialog import LoadConfigurationDialog

sys.path.remove(dialogsDir)


###############################################################################################################
###############################################################################################################

# Main Application tk Window

###############################################################################################################
###############################################################################################################

class ApplicationWindow(tk.Tk):
	def __init__(self, application):
		self._application = application	
		
		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Backer - Backup Management Tool")
		self.winfo_toplevel().geometry("1200x600+10+10")

		menubar = MainMenuBar(self)
		self.toolbar = ToolBarFrame(self._application, self)

		#INIT TREEVIEW FRAME (FORMERLY CONFIGURATION FRAME)
		self.treeFrame = TreeViewFrame(self._application, self)

		#INIT MAIN FRAME (FORMERLY DISPLAY FRAME)
		self.mainFrame = MainFrame(self._application, self)

		#INIT OUTPUT FRAME
		self.outputFrame = OutputFrame(self._application, self)


		self.grid_columnconfigure(0, minsize=10, weight=1)
		self.grid_columnconfigure(1, minsize=100, weight=2)
		self.grid_columnconfigure(2, minsize=100, weight=1)

		self.grid_rowconfigure(0, minsize=25, weight=0)
		self.grid_rowconfigure(1, minsize=100, weight=2)
		self.grid_rowconfigure(2, minsize=20, weight=1)

		self.toolbar.grid(row = 0, column = 0, columnspan=3, rowspan = 1, sticky="NEWS")
		self.treeFrame.grid(row=1, column=0, columnspan=1, rowspan=2, sticky="NEWS")
		self.mainFrame.grid(row=1, column=1, rowspan=1, columnspan=2, sticky="NEWS")
		self.outputFrame.grid(row=2, column=1, rowspan=1, columnspan=2, sticky="NEWS")

		self.after(500, lambda: self.focus_force())

		self.application.initializeApplication()
		self.treeFrame.buildTreeView(self.application.objectModel.currentUser)
		self.mainFrame.populateTreeviews()

		icon = tk.PhotoImage(file=os.path.join(self._application.imageDirectory,'Backer_Logo.png'))
		self.call('wm', 'iconphoto', self._w, icon)

		self.mainloop()

	@property
	def application(self):
		return self._application
	




	def kill(self):
		self.winfo_toplevel().destroy()

	def openNewDeviceDialog(self):
		AddDeviceDialog(self.treeFrame)

	def openNewCollectionDialog(self):
		AddCollectionDialog(self.treeFrame)

	def exitApplication(self):
		self.kill()

	def runConfiguration(self):
		print("Run Config")

	def updateConfigFile(self):
		self.application.outputManager.broadcast("Updating Configuration File . . .")
		JSONfromDatabase = self.application.configurationManager.jsonOperator.buildJSONFromDatabase(self.application.currentUserID, self.application.databaseOperator)
		
		jsonFileName = os.path.join(self.application.configDirectory, "config.cfg")
		with open(jsonFileName, 'w') as dumpFile:
			self.application.configurationManager.jsonOperator.dump(JSONfromDatabase, dumpFile)

		self.application.sourceCongruencyCheck()

	'''
	saveRunConfiguration

	Saves the run configuration for user CurrentUser.
	'''
	def saveRunConfiguration(self):
		saveDialog = SaveConfigurationDialog(self)
		saveDialog.mainloop()

	'''
	loadRunConfiguration

	Loads a configuration for user CurrentUser
	'''
	def loadRunConfiguration(self):
		loadDialog = LoadConfigurationDialog(self)
		loadDialog.mainloop()








class MainMenuBar(tk.Menu):
	def __init__(self, applicationWindow):
		self.menubar = tk.Menu(applicationWindow)
		applicationWindow.config(menu=self.menubar)

		self.fileMenu = tk.Menu(self.menubar, tearoff=0)
		self.fileMenu.add_command(label="New Device...", command=applicationWindow.openNewDeviceDialog)
		self.fileMenu.add_command(label="New Collection...", command=applicationWindow.openNewCollectionDialog)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Save Run Configuration...", command=applicationWindow.saveRunConfiguration)
		self.fileMenu.add_command(label="Load Run Configuration...", command=applicationWindow.loadRunConfiguration)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=applicationWindow.exitApplication)

		self.toolMenu = tk.Menu(self.menubar, tearoff=0)
		self.toolMenu.add_command(label="Run Backup...", command=applicationWindow.runConfiguration)
		self.toolMenu.add_separator()
		self.toolMenu.add_command(label="Update Configuration File", command=applicationWindow.updateConfigFile)

		self.menubar.add_cascade(label="File", menu = self.fileMenu)
		self.menubar.add_cascade(label="Tools", menu = self.toolMenu)