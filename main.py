# -*- coding: utf-8 -*-

from PyTry import *
import Level

import time
import sys
import subprocess
import os
import shutil

dtShow = 0.07
"""dt used to refresh the screen """
dtCalc = Object.dt
"""dt used in calcs """

saveName = "1"
"""Loaded save name """

keyboard_default = None #var to save keyboard settings
"""Var used to save keyboard settings"""

currentScene = 0
"""Current scene displayed and calculated """
sceneId = {"Start Menu":0,"Select save":1,"level":2}
"""Id corresponding to each scene"""

menuList = []
"""Menu list containing all possibles menus"""

currentLevel = None
"""Level played (dict <=> type Level)"""

def init():
	global dtShow,keyboard_default,kb_global

	Tools.sysExec("python2.7 initTerm.py") #init terminal size

	keyboard_default = KeyBinder.initKbStgs()

	#--------------------------- Menus
	#Start Menu
	menuList.append(Menu.Menu("Start Menu"))
	Menu.addButton(menuList[0],Button.Button("START",-1,15,setSceneToSelectSave))
	Menu.addButton(menuList[0],Button.Button("AIDE ",-1,30,onHelpPressed))

	#Select save menu
	menuList.append(Menu.Menu("Select save"))
	Menu.addButton(menuList[1],Button.Button("Nouvelle partie",-1,42,onNewGamePressed))
	KeyBinder.addAction(Menu.getKeyBinder(menuList[1]),'A',setSceneToStartMenu) #shift+a is the key to go back in menus

	for i in range(0,len(menuList)):
		KeyBinder.addAction(Menu.getKeyBinder(menuList[i]),'ESC',quit) #Add help action to each menu
		KeyBinder.addAction(Menu.getKeyBinder(menuList[i]),'?',onHelpPressed)

	#level
	loadLevel("0","1")

	return 

def quit():
	global keyboard_default

	sys.stdout.write('\033[2J')
	sys.stdout.write("\033[38;2;255;255;255m") #text white color restoration
	sys.stdout.write('\033[0m')

	KeyBinder.restoreKbStgs(keyboard_default)

	sys.exit()

	return





def live():
	global dtShow,currentScene,sceneId,currentLevel

	#KeyBinder.interact(kb_global)

	if(currentScene == sceneId["level"]):
		if(currentLevel != None):
			if(Level.interact(currentLevel) != 0):
				currentLevel = None
				currentScene = 0
	
	elif(currentScene == sceneId["Start Menu"]):
		Menu.interact(menuList[0])
	elif(currentScene == sceneId["Select save"]):
		Menu.interact(menuList[1])

	return 





def show():
	global SCREEN_WIDTH,SCREEN_HEIGHT,currentScene,menuList,currentLevel

	Tools.sysExec("clear")

	if(currentScene == sceneId["level"]):
		if(currentLevel != None):
			Level.show(currentLevel)
	elif(currentScene == sceneId["Start Menu"]):
		Menu.show(menuList[0])
	elif(currentScene == sceneId["Select save"]):
		Menu.show(menuList[1])

	sys.stdout.write("\033[0;0H\n")

	return 





def main():
	global kb_global,keyboard_default

	init()

	i = 0 #variable d'incrémentation de test

	lastTimeShow = 0
	lastTimeCalc = 0


	while(True):

		if(time.time()-lastTimeCalc > dtCalc):
			live()
			lastTimeCalc = time.time()
			KeyBinder.clearBuffer()
		if(time.time()-lastTimeShow > dtShow):
			show()
			lastTimeShow = time.time()

	quit()

	return 0




def loadLevel(name,currentSave):
	"""
	@param name: Name of the level to load
	@type name: str

	@param currentSave: Current save loaded
	@type currentSave: str

	@return: -
	@rtype: void
	"""
	global currentLevel
	assert type(name) is str
	assert type(currentSave) is str

	currentLevel = Level.Level(name,currentSave)
	KeyBinder.addAction(Level.getKeyBinder(currentLevel),'ESC',quit) #Add quit action to keybinder
	KeyBinder.addAction(Level.getKeyBinder(currentLevel),'?',onHelpPressed) #Add help action to keybinder


	return

def onHelpPressed():
	"""
	Function called when a button "Aide" is pressed or key '?'
	@return: -
	@rtype: void
	"""
	Tools.sysExec("clear")

	#menu help
	if(currentScene == sceneId["Start Menu"]):
		Menu.printScreen("helpFiles/"+"StartMenu")
	elif(currentScene == sceneId["Select save"]):
		Menu.printScreen("helpFiles/"+"SelectSave")
	elif(currentScene == sceneId["level"]):
		Menu.printScreen("helpFiles/"+"level")
	else:
		return


	KeyBinder.waitForKeyPressed()

	return

def onNewGamePressed():
	"""
	Function called when user ask to create a new game
	@return: -
	@rtype: void
	"""
	global keyboard_default

	maxNameLength = 50
	
	KeyBinder.restoreKbStgs(keyboard_default)

	name = ""
	nameLength = 0
	
	while(nameLength > maxNameLength or nameLength == 0 or os.path.exists("Saves/"+name)):
		Menu.printScreen("Pictures/askName.pic")
		sys.stdout.write("\033[13;58H")
		name = raw_input()
		nameLength = len(name)

		if(nameLength == 0):
			sys.stdout.write("\033[27;0H\033[2K\033[26;0H\033[2K\033[25;0H\033[2K\033[24;0H\033[2K\033[23;0H\033[2K")
			Menu.printText("Merci de rentrer un nom un peu plus long ...")

		elif(nameLength > maxNameLength):
			sys.stdout.write("\033[27;0H\033[2K\033[26;0H\033[2K\033[25;0H\033[2K\033[24;0H\033[2K\033[23;0H\033[2K")
			Menu.printText("Merci de rentrer un nom un peu plus court ...")

		elif(os.path.exists("Saves/"+name)):
			sys.stdout.write("\033[27;0H\033[2K\033[26;0H\033[2K\033[25;0H\033[2K\033[24;0H\033[2K\033[23;0H\033[2K")
			Menu.printText("Cette sauvegarde existe deja ...")
	
	os.mkdir("Saves/"+name)

	KeyBinder.initKbStgs()

	return

def setSceneToStartMenu():
	"""
	Set current scene to the menu "Start Menu"
	@return: -
	@rtype: void
	"""
	global sceneId,currentScene
	currentScene = sceneId["Start Menu"]

	return

def setSceneToSelectSave():
	"""
	Set current scene to the menu "Select save"
	@return: -
	@rtype: void
	"""
	global sceneId,currentScene
	currentScene = sceneId["Select save"]

	return


if(__name__ == "__main__"):
	tmps1 = time.time()
	
	main()

	tmps2=time.time()-tmps1
	print(tmps2)