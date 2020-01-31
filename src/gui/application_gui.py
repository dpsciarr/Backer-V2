from tkinter import ttk
import sys
import os.path
import tkinter as tk

###############################################################################################################
###############################################################################################################

# Main Application tk Window

###############################################################################################################
###############################################################################################################

class ApplicationWindow(tk.Tk):
	def __init__(self, application):
		tk.Tk.__init__(self)
		self.winfo_toplevel().title("Backer V2")

		self.winfo_toplevel().geometry("585x550+50+10")
		self.resizable(0,0)

		self.mainloop()

	def kill(self):
		self.winfo_toplevel().destroy()