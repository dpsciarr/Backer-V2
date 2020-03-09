'''
Backer Backup Management Software provides the ability to customize and streamline your backup process.

Copyright (C) 2020 Dominic P. Sciarrino

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see the source code at GitHub for
COPYING.txt file or contact the author at dominic.sciarrino@gmail.com.
'''

from tkinter import ttk
import tkinter as tk
import os

###############################################################################################################
###############################################################################################################

# Login Window

###############################################################################################################
###############################################################################################################

class LoginWindow(tk.Tk):
	def __init__(self, application):
		self._application = application
		tk.Tk.__init__(self)

		self.winfo_toplevel().geometry("350x170")
		self.resizable(0,0)

		self._frame = None
		self.switch_frame(LoginFrame)

		icon = tk.PhotoImage(file=os.path.join(self._application.imageDirectory,'Backer_Logo.png'))
		self.call('wm', 'iconphoto', self._w, icon)

		self.mainloop()

	@property
	def application(self):
		return self._application
	
	def switch_frame(self, frameClass):
		newFrame = frameClass(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = newFrame

	def kill(self):
		self.winfo_toplevel().destroy()


class LoginFrame(tk.Frame):
	def __init__(self, loginWindow):
		self._loginWindow = loginWindow
		loginWindow.winfo_toplevel().title("Backer - Login")

		tk.Frame.__init__(self, loginWindow, bg='white', width="350", height="170")

		usernameLabel = tk.Label(self, text="Username: ", bg="white", fg="black")
		self.usernameNotifierLabel = tk.Label(self, text="", bg="white", fg="red")
		passwordLabel = tk.Label(self, text="Password: ", bg="white", fg="black")
		self.passwordNotifierLabel = tk.Label(self, text="", bg="white", fg="red")

		self.usernameEntry = tk.Entry(self, width=35, borderwidth=2)
		self.passwordEntry = tk.Entry(self, show="*", width=35, borderwidth=2)

		loginButton = tk.Button(self, text="Login", height=2, width=10, command = self.login)
		newUserButton = tk.Button(self, text="New User", height=2, width=10, command = lambda : self.openNewUserDialog(loginWindow))
		closeButton = tk.Button(self, text="Cancel", height=2, width=10, command = loginWindow.kill)

		usernameLabel.place(x=30, y=10, relx=0, rely=0, anchor='nw')
		self.usernameNotifierLabel.place(x=30, y=30, relx=0, rely=0, anchor='nw')
		passwordLabel.place(x=30, y=50, relx=0, rely=0, anchor='nw')
		self.passwordNotifierLabel.place(x=30, y=70, relx=0, rely=0, anchor='nw')

		self.usernameEntry.place(x=110, y=10, relx=0, rely=0, anchor='nw')
		self.passwordEntry.place(x=110, y=50, relx=0, rely=0, anchor='nw')

		loginButton.place(x=30, y=100, relx=0, rely=0, anchor='nw')
		newUserButton.place(x=130, y = 100, relx=0, rely=0, anchor='nw')
		closeButton.place(x=230, y=100, relx=0, rely=0, anchor='nw')

		self.place(relx=0.5, rely=0.5, anchor='center')

	@property
	def loginWindow(self):
		return self._loginWindow

	def updateErrorMessages(self, usernameMessage, passcodeMessage):
		self.usernameNotifierLabel['text'] = usernameMessage
		self.passwordNotifierLabel['text'] = passcodeMessage
	

	def login(self):
		#Retrieve Database Operator
		dbOperator = self.loginWindow.application.databaseOperator

		#Get entered username and passcode
		user = self.usernameEntry.get()
		pw = self.passwordEntry.get()

		#initiate variables
		usernameValid = False
		userValidated = False
		usernameFromDatabase = ""
		passcodeFromDatabase = ""
		userNameErrorString = ""
		passcodeErrorString = ""

		#Check to see if username is valid
		usernameValid = dbOperator.checkInsertData(user)
		if usernameValid == False:
			userNameErrorString = "Username contains invalid characters. Stick to alphanumerics."
			passcodeErrorString = ""
			self.updateErrorMessages(userNameErrorString, passcodeErrorString)
		else:
			#Check to see if user is in database.
			try:
				dbOperator.openDatabase()
				sql = f"""SELECT user_name FROM users WHERE user_name = '{user}'"""
				dbOperator.setCursor()
				dbOperator.execute(sql)
				dbOperator.commit()
				data = dbOperator.fetchall()
				dbOperator.closeDatabase()
			except Exception as e:
				dbOperator.closeDatabase()
				userNameErrorString = "Database error..."
				passcodeErrorString = ""
				self.updateErrorMessages(userNameErrorString, passcodeErrorString)
				print(e)
			#if user is in database
			if len(data) > 0:
				usernameFromDatabase = data[0][0]

				#retrieve passcode from database
				try:
					dbOperator.openDatabase()
					sql = f"""SELECT passcode FROM users WHERE user_name = '{usernameFromDatabase}'"""
					dbOperator.setCursor()
					dbOperator.execute(sql)
					dbOperator.commit()
					data2 = dbOperator.fetchall()
					dbOperator.closeDatabase()
				except Exception as e:
					dbOperator.closeDatabase()
					userNameErrorString = ""
					passcodeErrorString = "Database error..."
					self.updateErrorMessages(userNameErrorString, passcodeErrorString)


				#if a passcode was found, store it
				if len(data2) > 0:
					passcodeFromDatabase = data2[0][0]
					userNameErrorString = ""
					passcodeErrorString = ""
					self.updateErrorMessages(userNameErrorString, passcodeErrorString)
				else:
					userNameErrorString = ""
					passcodeErrorString = "Password not setup in database."
					self.updateErrorMessages(userNameErrorString, passcodeErrorString)

				#validate the entered password with the one from the database
				if pw == passcodeFromDatabase:
					print(f"User '{user}' logging in...")
					userNameErrorString = ""
					passcodeErrorString = ""
					self.updateErrorMessages(userNameErrorString, passcodeErrorString)
					userValidated = True
				else:
					userNameErrorString = "User found!"
					passcodeErrorString = f"Wrong passcode entered for user '{user}'"
					self.updateErrorMessages(userNameErrorString, passcodeErrorString)

			else:
				dbOperator.closeDatabase()
				userNameErrorString = f"User {user} not found."
				passcodeErrorString = ""
				self.updateErrorMessages(userNameErrorString, passcodeErrorString)

		if userValidated == True:
			# update current user settings in application
			try:
				dbOperator.openDatabase()
				sql = f"""SELECT user_id FROM users WHERE user_name = '{user}'"""
				dbOperator.setCursor()
				dbOperator.execute(sql)
				dbOperator.commit()
				data3 = dbOperator.fetchall()
				dbOperator.closeDatabase()
			except Exception as e:
				dbOperator.closeDatabase()
				userValidated = False
				userNameErrorString = "Database error..."
				passcodeErrorString = "Database error..."
				self.updateErrorMessages(userNameErrorString, passcodeErrorString)

			if len(data3) > 0:
				userID = data3[0][0]
				self.loginWindow.application.currentUser = user
				self.loginWindow.application.currentUserID = userID
				self.loginWindow.kill()

	def openNewUserDialog(self, parent):
		parent.switch_frame(NewUserFrame)
















class NewUserFrame(tk.Frame):
	def __init__(self, loginWindow):
		tk.Frame.__init__(self, loginWindow, bg='white', width = "350", height = "170")
		self.winfo_toplevel().geometry("350x170")
		loginWindow.winfo_toplevel().title("Backer - New User")

		usernameLabel = tk.Label(self, text = "Username: ", bg = "white", fg = "black")
		self.usernameNotifierLabel = tk.Label(self, text="", bg="white", fg="red")
		passwordLabel1 = tk.Label(self, text="Password: ", bg = "white", fg= "black")
		passwordLabel2 = tk.Label(self, text="Verify: ", bg="white", fg="black")
		self.passwordNotifierLabel = tk.Label(self, text="", bg="white", fg="red")

		self.usernameEntry = tk.Entry(self, width=35, borderwidth=2)
		self.passwordEntry1 = tk.Entry(self, width=35, borderwidth=2, show="*")
		self.passwordEntry2 = tk.Entry(self, width=35, borderwidth=2, show="*")
		
		createUserButton = tk.Button(self, text="Create User", height=2, width=10, command = lambda : self.createUserRequest(loginWindow))
		loginButton = tk.Button(self, text="Login", height=2, width=10, command = lambda : self.openLoginDialog(loginWindow))
		closeButton = tk.Button(self, text="Close", height=2, width=10, command = loginWindow.kill)

		usernameLabel.place(x=30, y=10, relx=0, rely=0, anchor='nw')
		self.usernameNotifierLabel.place(x=30, y=30, relx=0, rely=0, anchor='nw')
		passwordLabel1.place(x=30, y=50, relx=0, rely=0, anchor='nw')
		passwordLabel2.place(x=50, y=70, relx=0, rely=0, anchor='nw')
		self.passwordNotifierLabel.place(x=30, y=90, relx=0, rely=0, anchor='nw')

		self.usernameEntry.place(x=110, y=10, relx=0, rely=0, anchor='nw')
		self.passwordEntry1.place(x=110, y=50, relx=0, rely=0, anchor='nw')
		self.passwordEntry2.place(x=110, y=70, relx=0, rely=0, anchor='nw')

		createUserButton.place(x=30, y=115, relx=0, rely=0, anchor='nw')
		loginButton.place(x=130, y=115, relx=0, rely=0, anchor='nw')
		closeButton.place(x=230, y=115, relx=0, rely=0, anchor='nw')

		self.place(relx=0.5, rely=0.5, anchor='center')

	def updateErrorMessages(self, usernameErrorString, passcodeErrorString):
		self.usernameNotifierLabel['text'] = usernameErrorString
		self.passwordNotifierLabel['text'] = passcodeErrorString

	def createUserRequest(self, loginWindow):
		#Retrieve Database Operator
		dbOperator = loginWindow.application.databaseOperator

		#initialize some variables
		passcodeMatch = False
		usernameTaken = True
		usernameErrorString = ""
		passcodeErrorString = ""

		#Get the entered passcodes
		pw1 = self.passwordEntry1.get()
		pw2 = self.passwordEntry2.get()

		#Compare passcodes
		if pw1 != pw2:
			userNameErrorString = ""
			passcodeErrorString = "Passwords don't match!"
			self.updateErrorMessages(userNameErrorString, passcodeErrorString)
			passcodeMatch = False
		else:
			userNameErrorString = ""
			passcodeErrorString = ""
			self.updateErrorMessages(userNameErrorString, passcodeErrorString)
			self.passwordNotifierLabel['text'] = ""
			passcodeMatch = True


		#Retrieve a possible username from the database
		user = self.usernameEntry.get()
		dbOperator.openDatabase()
		sql = f"""SELECT user_name FROM users WHERE user_name = '{user}'"""
		dbOperator.setCursor()
		dbOperator.execute(sql)
		data = dbOperator.fetchall()
		dbOperator.closeDatabase()

		if len(data) == 0:
			userNameErrorString = ""
			passcodeErrorString = ""
			self.updateErrorMessages(userNameErrorString, passcodeErrorString)
			usernameTaken = False
		else:
			userNameErrorString = "Username taken...try a new one!"
			passcodeErrorString = ""
			self.updateErrorMessages(userNameErrorString, passcodeErrorString)
			usernameTaken = True

		if usernameTaken == False and passcodeMatch == True:
			userNameErrorString = ""
			passcodeErrorString = ""
			self.updateErrorMessages(userNameErrorString, passcodeErrorString)
			
			try:
				#create user in model
				dbOperator.queries.addUser(user, pw1)

				dbOperator.openDatabase()
				sql = f"""SELECT user_name FROM users WHERE user_name = '{user}'"""
				dbOperator.setCursor()
				dbOperator.execute(sql)
				data = dbOperator.fetchall()
				dbOperator.closeDatabase()

				if len(data) == 0:
					userNameErrorString = "Something went wrong..."
					passcodeErrorString = "Unsuccessful user creation..."
					self.updateErrorMessages(userNameErrorString, passcodeErrorString)
				else:
					if data[0][0] == user:
						try:
							dbOperator.openDatabase()
							sql = f"""SELECT user_id FROM users WHERE user_name = '{user}'"""
							dbOperator.setCursor()
							dbOperator.execute(sql)
							dbOperator.commit()
							data3 = dbOperator.fetchall()
							dbOperator.closeDatabase()
						except Exception as e:
							dbOperator.closeDatabase()
							userValidated = False
							userNameErrorString = "Database error..."
							passcodeErrorString = "Database error..."
							self.updateErrorMessages(userNameErrorString, passcodeErrorString)

						if len(data3) > 0:
							userID = data3[0][0]
							loginWindow.application.currentUser = user
							loginWindow.application.currentUserID = userID

							loginWindow.application.currentUserID
							loginWindow.kill()
						else:
							print("Failed at user ID verification")

			except Exception as e:
				userNameErrorString = "Something went wrong..."
				passcodeErrorString = "Very wrong..."
				self.updateErrorMessages(userNameErrorString, passcodeErrorString)
				print(e)

			#check user exists in database


	def openLoginDialog(self, parent):
		parent.switch_frame(LoginFrame)
