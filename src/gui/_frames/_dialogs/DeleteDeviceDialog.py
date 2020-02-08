import tkinter as tk
from tkinter import ttk

class DeleteDeviceDialog(tk.Tk):
	def __init__(self, treeViewFrame):
		self._application = treeViewFrame.application

		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Delete Device")
		self.winfo_toplevel().geometry("350x150+500+200")
		frame = tk.Frame(self, bg='white')


	@property
	def application(self):
		return self._application