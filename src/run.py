import os
from gui.application_gui import ApplicationWindow


class Application:
	def __init__(self):
		print("Initializing Backer V2...")
		self._databaseName = "backer.db"

		self._srcDirectory = os.path.dirname(os.path.abspath(__file__))
		self._applicationDirectory = os.path.dirname(self._srcDirectory)
		self._databaseDirectory = os.path.join(self._srcDirectory, "_database")	

	@property
	def srcDirectory(self):
		return self._srcDirectory
	
	@property
	def applicationDirectory(self):
		return self._applicationDirectory
	
	@property
	def databaseDirectory(self):
		return self._databaseDirectory
	

if __name__ == '__main__':
	app = Application()