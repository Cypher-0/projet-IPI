# -*- coding: utf-8 -*-
"""
File containing some utilities functions
"""

import sys
import os
import time

def sysExec(command):

	"""
	Execute a system command
	@param command: String containing a system command
	@type command: str
	@return: -
	@rtype: void
	"""

	assert type(command) is str, "sysExec expect str input"
	os.system(command)

	return

def createDatasFromPic(filePath,keepSpaces = False):
	"""
	Create 2D array from a text file. Spaces and tabulations will be replaced by void character :\'\'
	@param filePath: Path to file containing datas to load
	@type filePath: str
	@param keepSpaces: Should spaces be kept during loading 
	@type keepSpaces: bool
	@return: 2D array containing data loaded. Access on data at (x,y) by list[y][x]
	@rtype: list
	"""

	assert type(filePath) is str

	file = open(filePath, "r")
	datas = file.read() 
	file.close()
	
	provStr = datas.split('\n')

	maxLen = 0
	i = 0
	for i in range(0,len(provStr)):
		if(maxLen < len(provStr[i-1])):
			maxLen = len(provStr[i-1])
	
	i = 0
	tab = []
	for i in range(0,len(provStr)):
		tab.append(list(provStr[i])+['']*(maxLen - len(provStr[i])))

	i,j=0,0
	if(keepSpaces == False):
		for i in range(len(tab)):
			for j in range(len(tab[i])):
				if(tab[i][j] == " " or tab[i][j] == "\t"):
					tab[i][j] = ''
	return tab

def resizeTerminal(x,y):
	"""
	Resize a terminal to get x characters on x axis and y characters on y axis
	@param x: Number of characters to display on x axis
	@type x: int
	
	@param y: Number of characters to display on x axis
	@type y: int

	@return: -
	@rtype: void
	"""

	assert type(x) is int
	assert type(y) is int

	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=y, cols=x))

	return

def getTerminalSize():
	"""
	Return terminal width and terminal height x,y (in number of characters which can be displayed)
	@return: SCREEN_WIDTH,SCREEN_HEIGHT : number of character displayable on : x,y axis
	@rtype: int,int
	"""

	rows, columns = os.popen('stty size', 'r').read().split()
	SCREEN_HEIGHT = int(rows)
	SCREEN_WIDTH = int(columns)
	return SCREEN_WIDTH,SCREEN_HEIGHT

def clearScreen():
	"""
	Clear all the terminal screen
	@return: -
	@rtype: void
	"""
	sys.stdout.write("\033[1;1H")
	sys.stdout.write("\033[2J")
	return


def goAt(X,Y):
	"""
	Set terminal cursor at (x,y)
	@param X: new X coordinates
	@type X: int
	@param Y: new Y coordinates
	@type Y: int
	@return: -
	@rtype: void
	"""

	assert type(X) is int
	assert type(Y) is int

	x=str(X)
	y=str(Y)
	txt='\033['+y+';'+x+'H'
	sys.stdout.write(txt)
	return

def debug(string,erase = False):
	"""
	Write debugs datas in a file named "DEBUG.TXT"
	@param string: Datas to write in debug file
	@type string: str
	@param erase: Erase file before writing \"string\"
	@type erase: bool
	@return: -
	@rtype: void
	"""
	string = str(string)
	if(erase == True):
		if(os.path.isfile("./DEBUG.txt")):
			sysExec("rm DEBUG.txt")
		file = open("./DEBUG.txt","w")
	else :
		file = open("./DEBUG.txt","a")
	file.write(string)
	file.write('\n')
	return

def prDly(string,dly=0.7): #print with delay for debug
	"""
	Print data for a determined time on terminal screen (used for debug)
	@param string: Datas to display on screen
	@type string: str
	@param dly: \"string\" will be displayed during \"dly\" s.
	@type dly: float
	@return: -
	@rtype: void
	"""
	print(string)
	time.sleep(dly)
	return