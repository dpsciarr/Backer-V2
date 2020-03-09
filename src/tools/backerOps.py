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

import backerTools as bats
import os.path as op
import os
from datetime import date
from datetime import datetime

'''
' fileCopyNew()
'
' Copies all files from the source directory to the destination directory.
' Files that exist only in the source directory are copied directly. Files
' that exist in both directories are appended with a suffix in the name, 
' determined by the 'token' attribute.
'
' 'token':
'    BASIC: A number is appended to the end of the filename.
'    TIME-STAMP: The current time and date is appended to the end of the 
'       filename, down to the second.
'    DATE-TIME: The current time and date is appended to the end of the 
'       filename, down to the minute.
'    DATE: The current date is appended to the end of the filename, in 
'       the format of YYYY-MM-DD
'
'''

def fileCopyNew(srcDir, destDir, token = 'BASIC'):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirReadPermissions
	
	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	returnListSrc = []
	returnListDest = []
	errors = []

	if srcOK and destOK:
		#get source-only files
		srcFilenames = bats.getSrcOnlyFiles(srcDir, destDir, absolute = False)
		srcOnlyFiles = [op.join(srcDir, srcFilenames[i]) for i in range(0, len(srcFilenames)) if bats.isFile(op.join(srcDir, srcFilenames[i]))]
		newDestFiles = [op.join(destDir, srcFilenames[i]) for i in range(0, len(srcFilenames)) if bats.isFile(op.join(srcDir, srcFilenames[i]))]

		#get common files
		commFilenames = bats.getCommonFiles(srcDir, destDir, absolute = 0)
		srcCommFiles = [op.join(srcDir, commFilenames[i]) for i in range(0, len(commFilenames)) if bats.isFile(op.join(srcDir, commFilenames[i]))]
		destCommFiles = [op.join(destDir, commFilenames[i]) for i in range(0, len(commFilenames)) if bats.isFile(op.join(srcDir, commFilenames[i]))]

		#copy source-only files into the destination directory
		for i in range(0, len(newDestFiles)):
			splitSrcDict = bats.splitFilePath(srcOnlyFiles[i])
			returnListSrc.append(srcOnlyFiles[i])

			splitDestDict = bats.splitFilePath(newDestFiles[i])

			if token == 'TIME-STAMP':
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm%Ss")
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dateTime) + " - " + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcOnlyFiles[i], newFileName))
			elif token == 'DATE-TIME':
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm")
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dateTime) + " - " + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcOnlyFiles[i], newFileName))
			elif token == 'DATE':
				today = date.today()
				dmy_date = today.strftime("%Y-%m-%d")
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dmy_date) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1	
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dmy_date) + " - " + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcOnlyFiles[i], newFileName))
			else:
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcOnlyFiles[i], newFileName))
			
			returnListDest.append(newFileName)
			#bats.createFile(newFileName)
			#bats.copyFileContent(srcOnlyFiles[i], newDestFiles[i])

		#compare common files to check if they have the same content
		for i in range(0, len(commFilenames)):
			returnListSrc.append(srcCommFiles[i])
			splitSrcDict = bats.splitFilePath(srcCommFiles[i])
			splitDestDict = bats.splitFilePath(destCommFiles[i])
			if token == 'TIME-STAMP':
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm%Ss")
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dateTime) + " - " + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcCommFiles[i], newFileName))
			elif token == 'DATE-TIME':
				#append a timestamp to the end
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm")
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dateTime) + " - " + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcCommFiles[i], newFileName))
			elif token == 'DATE':
				#append the date
				today = date.today()
				dmy_date = today.strftime("%Y-%m-%d")
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dmy_date) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1	
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dmy_date) + " - " + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcCommFiles[i], newFileName))
			else:
				#append a number
				newFileName = op.join(splitDestDict["root"], splitSrcDict["name"]) + splitSrcDict["ext"]
				j = 0
				while bats.isFile(newFileName) == True:
					j = j + 1
					newFileName = op.join(splitDestDict["root"], splitSrcDict["name"] + str(j) + splitSrcDict["ext"])
				bats.createFile(newFileName)
				print("Destination File: " + bats.copyFileContent(srcCommFiles[i], newFileName))
			returnListDest.append(newFileName)

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory not a valid directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return returnListSrc, returnListDest, errors


'''
' singleFileCopyNew()
'
' Copies a single file into the destination directory. If the file does not
' exist in the destination directory, then it is simply copied. If the file
' exists in the destination directory, then it is appended with a suffix 
' based on the 'token' attribute.
' 
' srcFile is assumed to be an absolute path.
'''

def singleFileCopyNew(srcFile, destDir, token='BASIC'):
	srcFileDict = bats.splitFilePath(srcFile)
	srcFileIsFile = bats.isFile(srcFile)
	srcDirReadPermissions = bats.checkReadPermissions(srcFileDict["root"])
	srcFileOK = srcFileIsFile and srcDirReadPermissions

	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destDirOK = destDirIsFolder and destDirReadPermissions and destDirWritePermissions

	returnSrcFileName = srcFile
	returnDestFileName = ""
	errors = []

	if srcFileOK and destDirOK:
		#convert the srcFile root to destFolder as root
		newDestFilename = op.join(destDir, srcFileDict["name"] + srcFileDict["ext"])
		newFileName = ""
		#append based on token
		if token == 'TIME-STAMP':
			today = datetime.now()
			dateTime = today.strftime("%Y-%m-%d %Hh%Mm%Ss")
			newFileName = op.join(destDir, srcFileDict["name"]) + " " + str(dateTime) + srcFileDict["ext"]
			j = 0
			while bats.isFile(newFileName) == True:
				j = j + 1
				newFileName = op.join(destDir, srcFileDict["name"]) + " " + str(dateTime) + " - " + str(j) + srcFileDict["ext"]
			bats.createFile(newFileName)
			bats.copyFileContent(srcFile, newFileName)
		elif token == 'DATE-TIME':
			today = datetime.now()
			dateTime = today.strftime("%Y-%m-%d %Hh%Mm")
			newFileName = op.join(destDir, srcFileDict["name"]) + " " + str(dateTime) + srcFileDict["ext"]
			j = 0
			while bats.isFile(newFileName) == True:
				j = j + 1
				newFileName = op.join(destDir, srcFileDict["name"]) + " " + str(dateTime) + " - " + str(j) + srcFileDict["ext"]
			bats.createFile(newFileName)
			bats.copyFileContent(srcFile, newFileName)
		elif token == 'DATE':
			today = date.today()
			dmy_date = today.strftime("%Y-%m-%d")
			newFileName = op.join(destDir, srcFileDict["name"]) + " " + str(dmy_date) + srcFileDict["ext"]
			j = 0
			while bats.isFile(newFileName) == True:
				j = j + 1
				newFileName = op.join(destDir, srcFileDict["name"]) + " " + str(dmy_date) + " - " + str(j) + srcFileDict["ext"]
			bats.createFile(newFileName)
			bats.copyFileContent(srcFile, newFileName)
		elif token == 'REV':
			newFileName = op.join(destDir, srcFileDict["name"]) + " - REV 0" + srcFileDict["ext"]
			j = 0
			while bats.isFile(newFileName) == True:
				j = j + 1
				newFileName = op.join(destDir, srcFileDict["name"]) + " - REV " + str(j) + srcFileDict["ext"]
			bats.createFile(newFileName)
			bats.copyFileContent(srcFile, newFileName)
		else:
			newFileName = op.join(destDir, srcFileDict["name"]) + srcFileDict["ext"]
			j = 0
			while bats.isFile(newFileName) == True:
				j = j + 1
				newFileName = op.join(destDir, srcFileDict["name"]) + " - " + str(j) + srcFileDict["ext"]
			bats.createFile(newFileName)
			bats.copyFileContent(srcFile, newFileName)

		returnDestFileName = newFileName

	else:
		if srcFileIsFile == False:
			errors.append("Source File not a valid file...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source file parent directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return returnSrcFileName, returnDestFileName, errors

'''
' fileCopyOverwrite()
'
' Copies all files from the source directory to the destination directory.
' Files that exist only in the source directory are copied directly. Files
' that exist in both directories are compared. If they have the same content
' then nothing happens. If their content differs, then the contents of the
' file in the destination directory is overwritten with the contents in the
' source directory.
'
'''
def fileCopyOverwrite(srcDir, destDir):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirReadPermissions
	
	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	returnSrcFiles = []
	returnDestFiles = []
	errors = []

	if srcOK and destOK:
		#get source-only files
		srcFilenames = bats.getSrcOnlyFiles(srcDir, destDir, absolute = False)
		srcOnlyFiles = [op.join(srcDir, srcFilenames[i]) for i in range(0, len(srcFilenames)) if bats.isFile(op.join(srcDir, srcFilenames[i]))]
		newDestFiles = [op.join(destDir, srcFilenames[i]) for i in range(0, len(srcFilenames)) if bats.isFile(op.join(srcDir, srcFilenames[i]))]

		#get common files
		commFilenames = bats.getCommonFiles(srcDir, destDir, absolute = 0)
		srcCommFiles = [op.join(srcDir, commFilenames[i]) for i in range(0, len(commFilenames)) if bats.isFile(op.join(srcDir, commFilenames[i]))]
		destCommFiles = [op.join(destDir, commFilenames[i]) for i in range(0, len(commFilenames)) if bats.isFile(op.join(srcDir, commFilenames[i]))]

		#filter out the files in comm files that actually require an overwrite
		filesForOverwrite = []
		for i in range(0, len(commFilenames)):
			if bats.compareFiles(srcCommFiles[i], destCommFiles[i]) == False:
				filesForOverwrite.append(commFilenames[i])
		
		#copy over the files in source directory to the destination directory
		for i in range(0, len(srcFilenames)):
			bats.createFile(newDestFiles[i])
			bats.copyFileContent(srcOnlyFiles[i], newDestFiles[i])
			returnSrcFiles.append(srcOnlyFiles[i])
			returnDestFiles.append(newDestFiles[i])

		#overwrite the common files
		for i in range(0, len(filesForOverwrite)):
			srcFileToOverwrite = op.join(srcDir, filesForOverwrite[i])
			destFileForOverwrite = op.join(destDir, filesForOverwrite[i])
			bats.copyFileContent(srcFileToOverwrite, destFileForOverwrite)
			returnSrcFiles.append(srcFileToOverwrite)
			returnDestFiles.append(destFileForOverwrite)

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory not a valid directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return returnSrcFiles, returnDestFiles, errors

'''
' singleFileCopyOverwrite()
'
' Copies a single source file to destination directory. If file exists,
' it is compared. If the contents are not equal, then the contents are 
' overwritten. If file does not exist, the file is copied into the 
' destination directory.
'''

def singleFileCopyOverwrite(srcFile, destDir):
	srcFileDict = bats.splitFilePath(srcFile)
	srcFileIsFile = bats.isFile(srcFile)
	srcDirReadPermissions = bats.checkReadPermissions(srcFileDict["root"])
	srcFileOK = srcFileIsFile and srcDirReadPermissions

	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destDirOK = destDirIsFolder and destDirReadPermissions and destDirWritePermissions

	returnSrcFile = ""
	returnDestFile = ""
	errors = []

	if srcFileOK and destDirOK:
		newDestFilename = op.join(destDir, srcFileDict["name"] + srcFileDict["ext"])
		if bats.isFile(newDestFilename):
			if bats.compareFiles(srcFile, newDestFilename) == False:
				bats.copyFileContent(srcFile, newDestFilename)
		else:
			bats.createFile(newDestFilename)
			bats.copyFileContent(srcFile, newDestFilename)
		returnSrcFile = srcFile
		returnDestFile = newDestFilename
	else:
		if srcFileIsFile == False:
			errors.append("Source File not a valid file...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source file parent directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return returnSrcFile, returnDestFile, errors

'''
' fileMigrateNew()
'
' Copies all files from the source to a destination directory via fileCopyNew()
'
' Deletes original source files.
'''

def fileMigrateNew(srcDir, destDir, token = 'BASIC'):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcDirWritePermissions = bats.checkWritePermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirWritePermissions and srcDirReadPermissions
	
	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	errors = []

	if srcOK and destOK:
		srcFilesCopied, destFilesCopied, err = fileCopyNew(srcDir, destDir, token)
		for i in range(0, len(srcFilesCopied)):
			if op.getsize(srcFilesCopied[i]) == op.getsize(destFilesCopied[i]):
				if bats.compareFiles(srcFilesCopied[i], destFilesCopied[i]):
					bats.deleteFile(srcFilesCopied[i])
				else:
					print("Source files not deleted.")
			else:
				print("Source file not deleted.")

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory not a valid directory...")
		if srcDirWritePermissions == False:
			errors.append("No permission to write to source directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")


	return "", "", errors

'''
' singleFileMigrateNew()
'
' Copies a single file into the destination directory via singleFileCopyNew().
' Deletes original files from source directory.
'''

def singleFileMigrateNew(srcFile, destDir, token = 'BASIC'):
	srcFileDict = bats.splitFilePath(srcFile)
	srcFileIsFile = bats.isFile(srcFile)
	srcDirReadPermissions = bats.checkReadPermissions(srcFileDict["root"])
	srcDirWritePermissions = bats.checkWritePermissions(srcFileDict["root"])
	srcFileOK = srcFileIsFile and srcDirWritePermissions and srcDirReadPermissions

	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	errors = []

	if srcFileOK and destOK:
		srcFileCopied, destFileCopied, err = singleFileCopyNew(srcFile, destDir, token)
		if op.getsize(srcFileCopied) == op.getsize(destFileCopied):
			if bats.compareFiles(srcFileCopied, destFileCopied):
				bats.deleteFile(srcFileCopied)
			else:
				print("Source file not deleted.")
		else:
			print("Source file wasn't deleted...")

	else:
		if srcFileIsFile == False:
			errors.append("Source File not a valid file...")
		if srcDirWritePermissions == False:
			errors.append("No perission to write to source directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return "", "", errors


'''
' fileMigrateOverwrite()
'
' Copies all files into the destination directory via fileCopyOverwrite().
' Deletes original copies in the source directory.
'''

def fileMigrateOverwrite(srcDir, destDir):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcDirWritePermissions = bats.checkWritePermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirWritePermissions and srcDirReadPermissions
	
	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	errors = []

	if srcOK and destOK:
		srcFilesList, destFilesList, err = fileCopyOverwrite(srcDir, destDir)

		for i in range(0, len(srcFilesList)):
			if op.getsize(srcFilesList[i]) == op.getsize(destFilesList[i]):
				if bats.compareFiles(srcFilesList[i], destFilesList[i]):
					bats.deleteFile(srcFilesList[i])
			else:
				print("Source file not deleted...")

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory not a valid directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if srcDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return "", "", errors


'''
' singleFileMigrateOverwrite()
'
' Copies a single file into the destination directory. Deletes original file 
' from the source directory.
'''

def singleFileMigrateOverwrite(srcFile, destDir):
	srcFileDict = bats.splitFilePath(srcFile)
	srcFileIsFile = bats.isFile(srcFile)
	srcDirReadPermissions = bats.checkReadPermissions(srcFileDict["root"])
	srcDirWritePermissions = bats.checkWritePermissions(srcFileDict["root"])
	srcFileOK = srcFileIsFile and srcDirWritePermissions and srcDirReadPermissions

	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	errors = []

	if srcFileOK and destOK:
		srcFileCopied, destFileCopied, err = singleFileCopyOverwrite(srcFile, destDir)

		if op.getsize(srcFileCopied) == op.getsize(destFileCopied):
			if bats.compareFiles(srcFileCopied, destFileCopied):
				bats.deleteFile(srcFileCopied)
			else:
				print("Source file not deleted")
		else:
			print("Source file wasn't deleted.")
	else:
		if srcFileIsFile == False:
			errors.append("Source File not a valid file...")
		if srcDirWritePermissions == False:
			errors.append("No perission to write to source directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return "", "", errors

'''
' folderCopyNew()
'
' Copies all folders in the source directory into the destination directory
'''

def folderCopyNew(srcDir, destDir, token='BASIC'):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirReadPermissions
	
	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	returnListSrc = []
	returnListDest = []
	errors = []

	if srcOK and destOK:
		#get source-only folder
		srcFolderNames = bats.getSrcOnlyFolders(srcDir, destDir, absolute = False)
		srcOnlyFolders = [op.join(srcDir, srcFolderNames[i]) for i in range(0, len(srcFolderNames)) if bats.isFolder(op.join(srcDir, srcFolderNames[i]))]
		newDestFolders = [op.join(destDir, srcFolderNames[i]) for i in range(0, len(srcFolderNames)) if bats.isFolder(op.join(srcDir, srcFolderNames[i]))]

		#get common folders
		commFolderNames = bats.getCommonFolders(srcDir, destDir, absolute = 0)
		srcCommFolders = [op.join(srcDir, commFolderNames[i]) for i in range(0, len(commFolderNames)) if bats.isFolder(op.join(srcDir, commFolderNames[i]))]
		destCommFolders = [op.join(destDir, commFolderNames[i]) for i in range(0, len(commFolderNames)) if bats.isFolder(op.join(srcDir, commFolderNames[i]))]

		#copy source-only folders into the destination directory
		for i in range(0, len(newDestFolders)):
			splitSrcDict = bats.splitFilePath(srcOnlyFolders[i])
			returnListSrc.append(srcOnlyFolders[i])

			splitDestDict = bats.splitFilePath(newDestFolders[i])
			if token == 'TIME-STAMP':
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm%Ss")
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime)
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime) + " - " + str(j)
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcOnlyFolders[i], newFolderName)
			elif token == 'DATE-TIME':
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm")
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime)
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime) + " - " + str(j)
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcOnlyFolders[i], newFolderName)
			elif token == 'DATE':
				today = date.today()
				dmy_date = today.strftime("%Y-%m-%d")
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dmy_date)
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dmy_date) + " - " + str(j)
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcOnlyFolders[i], newFolderName)
			else:
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"])
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(j)
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcOnlyFolders[i], newFolderName)

			returnListDest.append(newFolderName)

		#compare common folders to check if they have the same content
		for i in range(0, len(commFolderNames)):
			returnListSrc.append(srcCommFolders[i])
			splitSrcDict = bats.splitFilePath(srcCommFolders[i])
			splitDestDict = bats.splitFilePath(destCommFolders[i])
			if token == 'TIME-STAMP':
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm%Ss")
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dateTime))
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"]) + " " + str(dateTime) + " - " + str(j)
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcCommFolders[i], newFolderName)	
			elif token == 'DATE-TIME':
				today = datetime.now()
				dateTime = today.strftime("%Y-%m-%d %Hh%Mm")
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dateTime))
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dateTime) + " - " + str(j))
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcCommFolders[i], newFolderName)
			elif token == 'DATE':
				today = date.today()
				dmy_date = today.strftime("%Y-%m-%d")
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dmy_date))
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(dmy_date) + " - " + str(j))
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcCommFolders[i], newFolderName)
			else:
				newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"])
				j = 0
				while bats.isFolder(newFolderName) == True:
					j = j + 1
					newFolderName = op.join(splitDestDict["root"], splitSrcDict["name"] + " " + str(j))
				bats.createFolder(newFolderName)
				bats.copyFolderContent(srcCommFolders[i], newFolderName)

			returnListDest.append(newFolderName)

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory not a valid directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return returnListSrc, returnListDest, errors

'''
' singleFolderCopyNew()
'
' Makes a new copy of a srcFolder and saves it to a destination directory.
'''

def singleFolderCopyNew(srcFolder, destDir, token='BASIC'):
	srcFolderDict = bats.splitFilePath(srcFolder)
	srcFolderIsFolder = bats.isFolder(srcFolder)
	srcDirReadPermissions = bats.checkReadPermissions(srcFolderDict["root"])
	srcFolderOK = srcFolderIsFolder and srcDirReadPermissions

	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	errors = []

	if srcFolderOK and destOK:
		destFolderDict = bats.splitFilePath(destDir)

		if token == 'REV':
			newFolderName = op.join(destDir, srcFolderDict["name"]) + " REV 0"
			j = 0
			while bats.isFolder(newFolderName):
				j = j + 1
				newFolderName = op.join(destDir, srcFolderDict["name"]) + " REV " + str(j)
			bats.createFolder(newFolderName)
			try:
				bats.copyFolderContent(srcFolder, newFolderName)
			except Exception as e:
				errors.append(e.args)
		elif token == 'TIME-STAMP':
			today = datetime.now()
			dateTime = today.strftime("%Y-%m-%d %Hh%Mm%Ss")
			newFolderName = op.join(destDir, srcFolderDict["name"]) + " " + str(dateTime)
			j = 0
			while bats.isFolder(newFolderName):
				j = j + 1
				newFolderName = op.join(destDir, srcFolderDict["name"]) + " " + str(dateTime) + " - " + str(j)
			bats.createFolder(newFolderName)
			try:
				bats.copyFolderContent(srcFolder, newFolderName)
			except Exception as e:
				errors.append(e.args)
		elif token == 'DATE-TIME':
			today = datetime.now()
			dateTime = today.strftime("%Y-%m-%d %Hh%Mm")
			newFolderName = op.join(destDir, srcFolderDict["name"]) + " " + str(dateTime)
			j = 0
			while bats.isFolder(newFolderName):
				j = j + 1
				newFolderName = op.join(destDir, srcFolderDict["name"]) + " " + str(dateTime) + " - " + str(j)
			bats.createFolder(newFolderName)
			try:
				bats.copyFolderContent(srcFolder, newFolderName)
			except Exception as e:
				errors.append(e.args)
		elif token == 'DATE':
			today = date.today()
			dmy_date = today.strftime("%Y-%m-%d")
			newFolderName = op.join(destDir, srcFolderDict["name"]) + " " + str(dmy_date)
			j = 0
			while bats.isFolder(newFolderName):
				j = j + 1
				newFolderName = op.join(destDir, srcFolderDict["name"]) + " " + str(dmy_date) + " - " + str(j)
			bats.createFolder(newFolderName)
			try:
				bats.copyFolderContent(srcFolder, newFolderName)
			except Exception as e:
				errors.append(e.args)
		else:
			newFolderName = op.join(destDir, srcFolderDict["name"])
			j = 0
			while bats.isFolder(newFolderName):
				j = j + 1
				newFolderName = op.join(destDir, srcFolderDict["name"]) + " " - str(j)
			bats.createFolder(newFolderName)
			try:
				bats.copyFolderContent(srcFolder, newFolderName)
			except Exception as e:
				errors.append(e.args)

	else:
		if srcFolderIsFolder == False:
			errors.append("Source Folder is not a valid folder...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")


	return "", "", errors

'''
' folderCopyOverwrite()
'
' Copies all folders in source directory to destination directory. Overwrites 
' the folders that are common to both directories.
'''

def folderCopyOverwrite(srcDir, destDir):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirReadPermissions
	
	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	errors = []

	if srcOK and destOK:
		#get source-only folder
		srcFolderNames = bats.getSrcOnlyFolders(srcDir, destDir, absolute = False)
		srcOnlyFolders = [op.join(srcDir, srcFolderNames[i]) for i in range(0, len(srcFolderNames)) if bats.isFolder(op.join(srcDir, srcFolderNames[i]))]
		newDestFolders = [op.join(destDir, srcFolderNames[i]) for i in range(0, len(srcFolderNames)) if bats.isFolder(op.join(srcDir, srcFolderNames[i]))]

		#get common folders
		commFolderNames = bats.getCommonFolders(srcDir, destDir, absolute = 0)
		srcCommFolders = [op.join(srcDir, commFolderNames[i]) for i in range(0, len(commFolderNames)) if bats.isFolder(op.join(srcDir, commFolderNames[i]))]
		destCommFolders = [op.join(destDir, commFolderNames[i]) for i in range(0, len(commFolderNames)) if bats.isFolder(op.join(srcDir, commFolderNames[i]))]

		#copy over the new incoming folders
		for i in range(0, len(srcFolderNames)):
			bats.createFolder(newDestFolders[i])
			bats.copyFolderContent(srcOnlyFolders[i], newDestFolders[i])

		for i in range(0, len(commFolderNames)):
			#print(f"SOURCE: {srcCommFolders[i]}")
			#print(f"DEST: {destCommFolders[i]}")
			#print(f"COMPARE: {bats.compareTrees(srcCommFolders[i], destCommFolders[i])}")
			if bats.compareTrees(srcCommFolders[i], destCommFolders[i]) == False:
				bats.deleteFolder(destCommFolders[i])
				bats.createFolder(destCommFolders[i])
				bats.copyFolderContent(srcCommFolders[i], destCommFolders[i])

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory not a valid directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return "", "", errors


'''
' singleFolderCopyOverwrite()
'
' Copies a single folder in the source directory to destination directory.
' Overwrites the folders that are common to both directories.
'''
def singleFolderCopyOverwrite(srcFolder, destDir):
	srcFolderIsFolder = bats.isFolder(srcFolder)
	srcFolderReadPermissions = bats.checkReadPermissions(srcFolder)
	srcOK = srcFolderIsFolder and srcFolderReadPermissions
	
	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirWritePermissions and destDirReadPermissions

	errors = []

	if srcOK and destOK:
		srcFolderDict = bats.splitFilePath(srcFolder)
		destFolderDict = bats.splitFilePath(destDir)

		newFolderName = op.join(destDir, srcFolderDict["name"])
		if bats.isFolder(newFolderName) == False:
			bats.createFolder(newFolderName)
			try:
				bats.copyFolderContent(srcFolder, newFolderName)
			except Exception as e:
				errors.append(e.args)
		else:
			bats.deleteFolder(newFolderName)
			bats.createFolder(newFolderName)
			try:
				bats.copyFolderContent(srcFolder, newFolderName)
			except Exception as e:
				errors.append(e.args)
	else:
		if srcFolderIsFolder == False:
			errors.append("Source Folder is not a valid folder...")
		if srcFolderReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return "", "", errors


'''
' directorySyncOverwrite()
'
' Syncronizes the items of two directories by overwriting common files and
' copying over source-only files into the destination directory and 
' sub-directories.
'
'''
def directorySyncOverwrite(srcDir, destDir):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirReadPermissions

	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirReadPermissions and destDirWritePermissions

	errors = []

	if srcOK and destOK:
		#overwrite copy files
		fileCopyOverwrite(srcDir, destDir)

		#get source-only folders
		srcFolderNames = bats.getSrcOnlyFolders(srcDir, destDir, absolute = False)
		srcOnlyFolders = [op.join(srcDir, srcFolderNames[i]) for i in range(0, len(srcFolderNames)) if bats.isFolder(op.join(srcDir, srcFolderNames[i]))]
		newDestFolders = [op.join(destDir, srcFolderNames[i]) for i in range(0, len(srcFolderNames)) if bats.isFolder(op.join(srcDir, srcFolderNames[i]))]

		#get common folders
		commFolderNames = bats.getCommonFolders(srcDir, destDir, absolute = 0)
		srcCommFolders = [op.join(srcDir, commFolderNames[i]) for i in range(0, len(commFolderNames)) if bats.isFolder(op.join(srcDir, commFolderNames[i]))]
		destCommFolders = [op.join(destDir, commFolderNames[i]) for i in range(0, len(commFolderNames)) if bats.isFolder(op.join(srcDir, commFolderNames[i]))]

		#Copy source-only folders
		for i in range(0, len(srcFolderNames)):
			bats.createFolder(newDestFolders[i])
			bats.copyFolderContent(srcOnlyFolders[i], newDestFolders[i])

		for i in range(0, len(commFolderNames)):
			if bats.compareTrees(srcCommFolders[i], destCommFolders[i]) == False:
				directorySyncOverwrite(srcCommFolders[i], destCommFolders[i])

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory is not a valid directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return "", "", errors

'''
' fullDirectorySync()
'
' Syncronize the source and destination folders such that the destination
' directory "looks" or "mimics" exactly the source directory.
'''
def fullDirectorySync(srcDir, destDir):
	srcDirIsFolder = bats.isFolder(srcDir)
	srcDirReadPermissions = bats.checkReadPermissions(srcDir)
	srcOK = srcDirIsFolder and srcDirReadPermissions

	destDirIsFolder = bats.isFolder(destDir)
	destDirReadPermissions = bats.checkReadPermissions(destDir)
	destDirWritePermissions = bats.checkWritePermissions(destDir)
	destOK = destDirIsFolder and destDirReadPermissions and destDirWritePermissions

	errors = []

	if srcOK and destOK:
		fileCopyOverwrite(srcDir, destDir)
		folderCopyOverwrite(srcDir, destDir)

		#get destination-only files
		destFilenames = bats.getDestOnlyFiles(srcDir, destDir, absolute = False)
		destOnlyFiles = [op.join(destDir, destFilenames[i]) for i in range(0, len(destFilenames)) if bats.isFile(op.join(destDir, destFilenames[i]))]

		#get destination-only folders
		destFoldernames = bats.getDestOnlyFolders(srcDir, destDir, absolute = False)
		destOnlyFolders = [op.join(destDir, destFoldernames[i]) for i in range(0, len(destFoldernames)) if bats.isFolder(op.join(destDir, destFoldernames[i]))]

		#delete destination-only files
		for i in range(0, len(destFilenames)):
			bats.deleteFile(destOnlyFiles[i])

		#delete destination-only folders
		for i in range(0, len(destFoldernames)):
			bats.deleteFolder(destOnlyFolders[i])

	else:
		if srcDirIsFolder == False:
			errors.append("Source Directory is not a valid directory...")
		if srcDirReadPermissions == False:
			errors.append("No permission to read from source directory...")
		if destDirIsFolder == False:
			errors.append("Destination Directory not a valid directory...")
		if destDirWritePermissions == False:
			errors.append("No permission to write from destination directory...")
		if destDirReadPermissions == False:
			errors.append("No permission to read from destination directory...")

	return "", "", errors