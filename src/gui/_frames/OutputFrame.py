import tkinter as tk

class OutputFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._mainWindow = mainWindow
		self._application = application

		tk.Frame.__init__(self, mainWindow, bg='RED', height=30)

		self.outputTextBox = tk.Text(self, height=7, width=100)
		self.outputTextBox.config(state = 'disabled')


		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=0)
		self.grid_rowconfigure(0, weight=1)

		self.scrollbar = tk.Scrollbar(self, command=self.outputTextBox.yview)
		self.outputTextBox['yscrollcommand'] = self.scrollbar.set


		self.outputTextBox.grid(row=0, column=0, sticky='NEWS')
		self.scrollbar.grid(row=0, column=1, sticky='NS')

		self.printLine(f"Current User: {application.currentUser}")

	@property
	def application(self):
		return self._application
	
	@property
	def mainWindow(self):
		return self._mainWindow

	def printLine(self, text):
		self.outputTextBox.config(state='normal')
		text = text + '\n'
		self.outputTextBox.insert(tk.END, text)
		self.outputTextBox.config(state='disabled')
		self.outputTextBox.yview_moveto(1)