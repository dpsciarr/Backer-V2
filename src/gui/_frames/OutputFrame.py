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