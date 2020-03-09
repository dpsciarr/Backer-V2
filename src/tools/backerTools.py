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

'''
Houses supporting functions to backerOps
'''
import os.path as op
import filecmp as fc
import os
import shutil
from distutils.dir_util import copy_tree

'''
' isFolder()
'
' Returns True if path is a folder. Returns False otherwise.
'
'''
def isFolder(path):
	return op.isdir(path) if op.exists(path) else False

'''
' isFile()
'
' Returns True if path is a file. Returns False otherwise.
'
'''
def isFile(filepath):
	return op.isfile(filepath) if op.exists(filepath) else False

'''
' pathExists()
'
' Wrapper function for op.exists()
'''
def pathExists(path):
	return True if op.exists(filepath) else False

'''
' checkWritePermissions()
'
' Checks the write permission of the given folder path
'''
def checkWritePermissions(path):
	return os.access(path, os.W_OK)

'''
' checkReadPermissions()
'
' Checks the read permission of the given folder path
'''
def checkReadPermissions(path):
	return os.access(path, os.R_OK)

'''
' filenameValid()
'
' Tests if filename adheres to Windows naming convention
'
'''
def filenameValid(filename):
	invalidChars = '\\/:*?"<>|'
	for char in filename:
		if char in invalidChars:
			return False
	return True

'''
' foldernameValid()
'
' Tests if foldername adheres to Windows naming convention
'
'''
def foldernameValid(foldername):
	invalidChars = '\\/:*?"<>|'
	for char in foldername:
		if char in invalidChars:
			return False
	return True

'''
' getSrcOnlyItems()
'
' Returns a list of items only in the source directory. If absolute
' is True, returns the list of absolute paths.
' 
'''
def getSrcOnlyItems(srcPath, destPath, absolute = False):
	dc = fc.dircmp(srcPath, destPath)
	srcItems = dc.left_only
	if absolute == True:
		for i in range(0, len(srcItems)):
			srcItems[i] = op.join(srcPath, srcItems[i])
	return srcItems

'''
' getDestOnlyItems()
'
' Returns a list of items only in the destination directory. If 
' absolute is True, returns the list of absolute paths.
'''
def getDestOnlyItems(srcPath, destPath, absolute = False):
	dc = fc.dircmp(srcPath, destPath)
	destItems = dc.right_only
	if absolute == True:
		for i in range(0, len(destItems)):
			destItems[i] = op.join(destPath, destItems[i])
	return destItems

'''
' getCommonItems()
'
' Returns a list of items that are common between both 
' directories. If absolute is 1, returns a list of absolute
' paths with the source path as root. If absolute is 2
' returns a list of absolute paths with the destination path as root.
' If absolute is 0, returns a list without absolute paths.
'''
def getCommonItems(srcPath, destPath, absolute = 0):
	dc = fc.dircmp(srcPath, destPath)
	commItems = dc.common
	if absolute == 0:
		return commItems
	if absolute == 1:
		for i in range(0, len(commItems)):
			commItems[i] = op.join(srcPath, commItems[i])
	if absolute == 2:
		for i in range(0, len(commItems)):
			commItems[i] = op.join(destPath, commItems[i])
	return commItems

'''
' getSrcOnlyFiles()
'
' Returns a list of files that are only in the source
' directory. If absolute is true, returns a list with 
' absolute paths.
'
'''
def getSrcOnlyFiles(srcPath, destPath, absolute = False):
	srcItems = getSrcOnlyItems(srcPath, destPath, absolute)
	result = []
	for item in srcItems:
		if absolute == True:
			if isFile(item):
				result.append(item)
		else:
			srcName, srcExt = op.splitext(item)
			if srcExt != "" and srcExt != ".":
				result.append(item)
	return result

'''
' getDestOnlyFiles()
'
' Returns a list of files that are only in the destination
' directory. If absolute is True, returns a list with
' absolute paths.
'
'''
def getDestOnlyFiles(srcPath, destPath, absolute = False):
	destItems = getDestOnlyItems(srcPath, destPath, absolute)
	result = []
	for item in destItems:
		if absolute == True:
			if isFile(item):
				result.append(item)
		else:
			srcName, srcExt = op.splitext(item)
			if srcExt != "" and srcExt != ".":
				result.append(item)
	return result

'''
' getCommonFiles()
'
' Returns a list of files that are present in both directories. If
' absolute is 1, returns a list with sourcePath as the absolute path. 
' If absolute is 2, returns a list with destPath as the absolute path.
'
'''
def getCommonFiles(srcPath, destPath, absolute = 0):
	commItems = getCommonItems(srcPath, destPath, absolute)
	result = []
	for item in commItems:
		if absolute == 1 or absolute == 2:
			if isFile(item):
				result.append(item)
		else:
			if "." in item and ".pretty" not in item:
				result.append(item)
	return result

'''
' getSrcOnlyFolders()
'
' Returns a list of folders that are only in the source 
' directory. If absolute is True, returns a list with
' absolute paths.
'''
def getSrcOnlyFolders(srcPath, destPath, absolute = False):
	srcItems = getSrcOnlyItems(srcPath, destPath, absolute)
	result = []
	for item in srcItems:
		if absolute == True:
			if isFolder(item):
				result.append(item)
		else:
			if "." not in item:
				result.append(item)
			else:
				if ".pretty" in item:
					result.append(item)
	return result

'''
' getDestOnlyFolders()
'
' Returns a list of folders that are only in the destination
' directory. If absolute is True, returns a list with 
' absolute paths
'''
def getDestOnlyFolders(srcPath, destPath, absolute = False):
	destItems = getDestOnlyItems(srcPath, destPath, absolute)
	result = []
	for item in destItems:
		if absolute == True:
			if isFolder(item):
				result.append(item)
		else:
			if "." not in item:
				result.append(item)
			else:
				if ".pretty" in item:
					result.append(item)
	return result

'''
' getCommonFolders()
'
' Returns a list of folders that are present in both directories. If
' absolute is 1, returns a list with sourcePath as the absolute path. 
' If absolute is 2, returns a list with destPath as the absolute path.
'
'''
def getCommonFolders(srcPath, destPath, absolute = 0):
	commItems = getCommonItems(srcPath, destPath, absolute)
	result = []
	for item in commItems:
		if absolute == True:
			if isFolder(item):
				result.append(item)
		else:
			if "." not in item:
				result.append(item)
			else:
				if ".pretty" in item:
					result.append(item)
	return result

'''
' compareFiles()
'
' Compares two files based on filecmp cmp function. Assumes absolute paths.
'''
def compareFiles(srcFile, destFile):
	if isFile(srcFile) and isFile(destFile):
		return fc.cmp(srcFile, destFile, shallow=False)
	return False

'''
' compareTrees()
'
' Compares contents of two directories.
'''
def compareTrees(dir1, dir2):
	dirs_cmp = fc.dircmp(dir1, dir2)
	if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0:
		return False
	(_, mismatch, errors) = fc.cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow = False)
	if len(mismatch) > 0 or len(errors) > 0:
		return False
	for common_dir in dirs_cmp.common_dirs:
		new_dir1 = op.join(dir1, common_dir)
		new_dir2 = op.join(dir2, common_dir)
		if not compareTrees(new_dir1, new_dir2):
			return False
	return True


'''
' createFile()
'
' Creates the file specified by 'filename'. Assumes an absolute path.
'
'
'''
def createFile(filename):
	if isFile(filename) == False:
		try:
			print("Filename: " + filename)
			fileOpen = open(filename, 'w+')
		except Exception as e:
			print("Exception: " + str(e.args[0]) + ',' + e.args[1])
			return None
		fileOpen.close()
	else:
		print("File already exists in path " + filename)
		return None
	return filename

'''
' createFolder()
'
' Creates a folder specified by 'folderName'. Assumes an absolute path.
'
'''

def createFolder(folderName):
	if isFolder(folderName) == False:
		try:
			os.makedirs(folderName)
		except Exception as e:
			print(e.args[0])
			return ""
	else:
		print("Folder already exists...")
		return ""

	return folderName

'''
' copyFileContent()
'
' Copies the contents of a source file into a destination file.
'''
def copyFileContent(srcFile, destFile):
	srcFileOK = isFile(srcFile)
	destFileOK = isFile(destFile)

	if srcFileOK and destFileOK:
		return shutil.copy2(srcFile, destFile)
	else:
		print("SRC: " + str(srcFileOK))
		print("DEST: " + str(destFileOK))
		return None

'''
' copyFolderContent()
'
' Copies the contents of a source folder into a destination folder.
'''
def copyFolderContent(srcFolder, destFolder):
	srcFolderOK = isFolder(srcFolder)
	destFolderOK = isFolder(destFolder)

	if srcFolderOK and destFolderOK:
		items = os.listdir(srcFolder)
		for item in items:
			if isFolder(os.path.join(srcFolder, item)) == True:
				print("FOLDER: " + str(item))
				newFolder = createFolder(os.path.join(destFolder, item))
				copyFolderContent(os.path.join(srcFolder, item), newFolder)

			elif isFile(os.path.join(srcFolder, item)) == True:
				createFile(os.path.join(destFolder, item))
				copyFileContent(os.path.join(srcFolder, item), os.path.join(destFolder, item))
			else:
				print(item)

		#x = copy_tree(srcFolder, destFolder)
		#x = shutil.move(srcFolder, destFolder)
		#print(x)
		return None
	else:
		print("Problem with copyFolderContent")
		return None

'''
' splitFilePath()
'
' Takes in an absolute file path, splits it into its' constituents and
' returns a dictionary of said constituents:
' 
' root = the root path of the file
' name = the name of the file
' ext = the extension
'''

def splitFilePath(filepath):
	root, head = op.split(filepath)
	name, ext = op.splitext(head)
	
	splitDict = {}
	splitDict['root'] = root
	splitDict['name'] = name
	splitDict['ext'] = ext

	return splitDict

'''
' deleteFile()
'
' Takes in absolute path of a file to be removed and deletes file.
'''
def deleteFile(filePath):
	if isFile(filePath):
		try:
			os.remove(filePath)
		except Exception as e:
			print(e.args[0])
	else:
		print("File does not exist.")

'''
' deleteFolder()
'
' Takes in absolute path of a folder to be removed and deletes folder.
'''
def deleteFolder(folderPath):
	if isFolder(folderPath):
		try:
			shutil.rmtree(folderPath)
		except Exception as e:
			print(e.args[0])