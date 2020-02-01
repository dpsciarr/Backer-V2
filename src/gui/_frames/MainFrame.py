import tkinter as tk

class MainFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._application = application
		self._mainWindow = mainWindow
		background = 'black'
		foreground = 'white'

		tk.Frame.__init__(self, mainWindow, bg=background, width = 500)

		# DEFINING LABELS
		runConfigLabel = tk.Label(self, text="RUN CONFIGURATION", bg=background, fg=foreground, font='Helvetica 10 bold')
		idleProcsLabel = tk.Label(self, text="IDLE PROCEDURES", bg=background, fg=foreground, font='Helvetica 10 bold')
		selectedProcProps = tk.Label(self, text="SELECTED PROCEDURE PROPERTIES:", bg=background, fg=foreground, font='Helvetica 9 bold')
		procSrcLabel = tk.Label(self, text="Source Path: ", bg=background, fg=foreground)
		operationLabel = tk.Label(self, text="Operation: ", bg=background, fg=foreground)
		procDestLabel = tk.Label(self, text="Destination Path: ", bg=background, fg=foreground)

		self.currInfoSrcLabel = tk.Label(self, text=f"Info Source: ", bg=background, fg=foreground)

		self.srcDisplayLabel = tk.Label(self, text="", bg=background, fg=foreground)
		self.operationDisplayLabel = tk.Label(self, text="", bg=background, fg=foreground)
		self.destDisplayLabel = tk.Label(self, text="", bg=background, fg=foreground)
		

		# PLACING LABELS
		runConfigLabel.place(x=340, y=10, anchor='nw')
		idleProcsLabel.place(x=715, y=10, anchor='nw')
		selectedProcProps.place(x=20, y=250, anchor='nw')
		procSrcLabel.place(x=20, y = 270, anchor='nw')
		operationLabel.place(x=20, y = 290, anchor='nw')
		procDestLabel.place(x=20, y = 310, anchor='nw')

		self.currInfoSrcLabel.place(x=20, y = 125, anchor = 'nw')

		self.srcDisplayLabel.place(x=125, y = 270, anchor='nw')
		self.operationDisplayLabel.place(x=125, y = 290, anchor='nw')
		self.destDisplayLabel.place(x=125, y = 310, anchor='nw')

	@property
	def application(self):
		return self._application
	
	@property
	def mainWindow(self):
		return self._mainWindow
	