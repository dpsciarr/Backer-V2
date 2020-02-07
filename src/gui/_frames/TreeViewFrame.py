import tkinter as tk
from tkinter import ttk

class TreeViewFrame(tk.Frame):
	def __init__(self, application, mainWindow):
		self._application = application
		self._mainWindow = mainWindow
		self._tree = None
		self._currentTreeItemID = None
		
		tk.Frame.__init__(self, mainWindow, bg='WHITE', width=250)

	@property
	def application(self):
		return self._application

	@property
	def mainWindow(self):
		return self._mainWindow

	@property
	def tree(self):
		return self._tree

	@tree.setter
	def tree(self, value):
		self._tree = value

	@property
	def currentTreeItemID(self):
		return self._currentTreeItemID

	@currentTreeItemID.setter
	def currentTreeItemID(self, value):
		self._currentTreeItemID = value

	def showContextMenu(self, event):
		print("Context Menu appears")

	def tree_click_event(self, event):
		self.currentTreeItemID = self.tree.focus()
	
	def buildTreeView(self, userObject):
		self.tree = ttk.Treeview(self, selectmode='browse')

		self.tree.bind("<Button-3>", self.showContextMenu)
		self.tree.bind('<<TreeviewSelect>>', self.tree_click_event)
		self.tree.heading('#0', text='Configuration Tree')
		self.tree.insert("", "end", iid="user", text=f"User: {userObject.username}")
		


