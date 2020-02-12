import tkinter as tk

class SaveConfigurationDialog(tk.Tk):
	def __init__(self, applicationWindow):
		self._applicationWindow = applicationWindow

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Save Run Configuration")
		self.winfo_toplevel().geometry("300x200+300+100")
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

	@property
	def applicationWindow(self):
		return self._applicationWindow

	def kill(self):
		self.winfo_toplevel().destroy()


	def save(self):
		print("Saving")