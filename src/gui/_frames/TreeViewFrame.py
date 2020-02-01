import tkinter as tk

class TreeViewFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._application = application
		self._mainWindow = mainWindow
		
		tk.Frame.__init__(self, mainWindow, bg='WHITE', width=250)

	@property
	def application(self):
		return self._application

	@property
	def mainWindow(self):
		return self._mainWindow
	
	
