import tkinter as tk

class LoadConfigurationDialog(tk.Tk):
	def __init__(self, applicationWindow):
		self._applicationWindow = applicationWindow

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Load Run Configuration")
		self.winfo_toplevel().geometry("250x200+300+100")
		f = tk.Frame(self, bg='white')

		'''
		rcf_files = [f for f in listdir(rootPath) if f.lower().endswith('.rcf')]

		if len(rcf_files) == 0:
			rcf_files.append("")

		'''
		loadFileNameLabel = tk.Label(f, text="Choose a Run Configuration to load:", bg="white", fg="black")
		#self.loadFileList = ttk.Combobox(f, values = rcf_files, state = 'readonly')
		#self.loadFileList.set(rcf_files[0])
		
		self.loadFileButton = tk.Button(f, text = "Load", height = 2, width = 10, command = lambda : self.load())
		self.closeButton = tk.Button(f, text="Cancel", height=2, width=10, command = self.kill)

		
		loadFileNameLabel.place(x = 30, y = 20, relx = 0, rely = 0, anchor = 'nw')
		#self.loadFileList.place(x = 30, y = 60, relx = 0, rely = 0, anchor = 'nw')
		self.loadFileButton.place(x = 25, y = 100, anchor = 'nw')
		self.closeButton.place(x = 150, y = 100, anchor = 'nw')

		#self.loadFileList.config(width = 30)


		f.pack(fill='both', expand=1)

	@property
	def applicationWindow(self):
		return self._applicationWindow
	
	def load(self):
		print("Loading")

	def kill(self):
		self.winfo_toplevel().destroy()

