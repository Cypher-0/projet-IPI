# -*- coding: utf-8 -*-

from PyTry import *
import Level
import Player

import time
import sys
import subprocess
import os
import shutil
import copy

dtShow = 0.07
"""dt used to refresh the screen """
dtCalc = Object.dt
"""dt used in calcs """

saveName = ""
"""Loaded save name """

keyboard_default = None #var to save keyboard settings
"""Var used to save keyboard settings"""

currentScene = 0
"""Current scene displayed and calculated """
sceneId = {"PyTry":0,"Select save":1,"Select level":2,"level":3}
"""Id corresponding to each scene"""

menuList = []
"""Menu list containing all possibles menus"""

currentLevel = None
"""Level played (dict <=> type Level)"""


MAX_SAVES_NUMBER,SAVES_BUTTONS_SPACE = 5,8

def init():
	global dtShow,keyboard_default,kb_global

	Tools.resizeTerminal(Object.SCREEN_WIDTH,Object.SCREEN_HEIGHT)

	keyboard_default = KeyBinder.initKbStgs()

	if(not(os.path.exists("Saves"))):
		os.mkdir("Saves")

	#--------------------------- Menus
	#PyTry
	menuList.append(Menu.Menu("PyTry"))
	Menu.addButton(menuList[0],Button.Button("START",-1,5,setSceneToSelectSave,40))
	Menu.addButton(menuList[0],Button.Button("AIDE ",-1,17,onHelpPressed,40))
	Menu.addButton(menuList[0],Button.Button("Quitter",-1,29,quit,40))
	KeyBinder.addAction(Menu.getKeyBinder(menuList[0]),'ESC',quit) #ESC is the key to go back in menus

	#Select save menu
	menuList.append(Menu.Menu("Select save"))
	if(countSaves() < MAX_SAVES_NUMBER):
		Menu.addButton(menuList[1],Button.Button("Nouvelle partie",10,42,onNewGamePressed))
	for i in range(0,countSaves()):
		Menu.addButton(menuList[1],Button.Button(os.listdir("Saves")[i],-1,5+i*SAVES_BUTTONS_SPACE,onSaveSelected,54))
	if(countSaves() > 0 and countSaves() < MAX_SAVES_NUMBER):
		Menu.setSelectedIndex(menuList[1],1)

	KeyBinder.addAction(Menu.getKeyBinder(menuList[1]),'ESC',setSceneToStartMenu) #ESC is the key to go back in menus
	KeyBinder.addAction(Menu.getKeyBinder(menuList[1]),'D',onDelSavePressed) #shift+d is the key to delete a save
	KeyBinder.addAction(Menu.getKeyBinder(menuList[1]),'N',onNewGamePressed) #shift+n is the key to add a save


	#Select level menu
	menuList.append(Menu.Menu("Select level"))
	KeyBinder.addAction(Menu.getKeyBinder(menuList[2]),'ESC',setSceneToSelectSave) #ESC is the key to go back in menus

	#all menus
	for i in range(0,len(menuList)):
		KeyBinder.addAction(Menu.getKeyBinder(menuList[i]),'Q',quit)
		KeyBinder.addAction(Menu.getKeyBinder(menuList[i]),'?',onHelpPressed)#Add help action to each menu

	return 

def quit():
	global keyboard_default

	Tools.sysExec("clear")
	sys.stdout.write("\033[38;2;180;20;20;1m")
	Menu.printScreen("Pictures/confirmQuitGame.pic")
	print("")
	key = ""
	while(key != "o" and key != "n"):
		key = KeyBinder.waitForKeyPressed()
	if(key == "n"):
		return

	sys.stdout.write('\033[2J')
	sys.stdout.write("\033[38;2;255;255;255m") #text white color restoration
	sys.stdout.write('\033[0m')

	KeyBinder.restoreKbStgs(keyboard_default)

	#Tools.sysExec("reset")

	sys.exit()

	return





def live():
	global dtShow,currentScene,sceneId,currentLevel,saveName

	#KeyBinder.interact(kb_global)

	if(currentScene == sceneId["level"]):
		if(currentLevel != None):
			lvlState = Level.interact(currentLevel)

			if(lvlState != 0):
				setSceneToSelectLevel()
				if(lvlState == 2):#if player win
					if(int(Level.getLevelName(currentLevel))+1 > Player.getMaxLvlUnlocked(Level.getPlayer(currentLevel))):
						Player.writePlayerStats(Level.getPlayer(currentLevel),int(Level.getLevelName(currentLevel))+1)

				#reload level selection menu
				onSaveSelected()

				#clear currentLevel
				currentLevel = None


	
	elif(currentScene == sceneId["PyTry"]):
		Menu.interact(menuList[0])
	elif(currentScene == sceneId["Select save"]):
		Menu.interact(menuList[1])
	elif(currentScene == sceneId["Select level"]):
		Menu.interact(menuList[2])

	return 





def show():
	global SCREEN_WIDTH,SCREEN_HEIGHT,currentScene,menuList,currentLevel

	Tools.sysExec("clear")

	if(currentScene == sceneId["level"]):
		if(currentLevel != None):
			Level.show(currentLevel)
	elif(currentScene == sceneId["PyTry"]):
		Menu.show(menuList[0])
	elif(currentScene == sceneId["Select save"]):
		Menu.show(menuList[1])
	elif(currentScene == sceneId["Select level"]):
		Menu.show(menuList[2])

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
	KeyBinder.addAction(Level.getKeyBinder(currentLevel),'Q',quit) #Add quit action to keybinder
	KeyBinder.addAction(Level.getKeyBinder(currentLevel),'?',onHelpPressed) #Add help action to keybinder

	KeyBinder.addAction(Level.getKeyBinder(currentLevel),'ESC',quitLevel) #ESC is the key to go back in menus


	return

def quitLevel():
	"""
	Function called when user ask to quit level played to level selection menu

	@return: -
	@rtype: void
	"""

	Tools.sysExec("clear")
	sys.stdout.write("\033[38;2;180;20;20;1m")
	Menu.printScreen("Pictures/confirmQuitLevel.pic")
	print("")
	key = ""
	while(key != "o" and key != "n"):
		key = KeyBinder.waitForKeyPressed()
	if(key == "n"):
		return

	setSceneToSelectLevel()

	return

def onHelpPressed():
	"""
	Function called when a button "Aide" is pressed or key '?'
	@return: -
	@rtype: void
	"""
	Tools.sysExec("clear")

	#menu help
	if(currentScene == sceneId["PyTry"]):
		Menu.printScreen("helpFiles/"+"StartMenu")
	elif(currentScene == sceneId["Select save"]):
		Menu.printScreen("helpFiles/"+"SelectSave")
	elif(currentScene == sceneId["Select level"]):
		Menu.printScreen("helpFiles/"+"SelectLevel")
	elif(currentScene == sceneId["level"]):
		Menu.printScreen("helpFiles/"+"level")
	else:
		return


	KeyBinder.waitForKeyPressed()

	return

def onLevelSelected():
	"""
	Function called when a save is selected by the user 

	@return: -
	@rtype: void
	"""
	global saveName

	selectedLevel = Button.getText(Menu.getButtonAt(menuList[2],Menu.getSelectedIndex(menuList[2])))
	setSceneToLevel()
	loadLevel(str(selectedLevel),saveName)

	return

def onSaveSelected():
	"""
	Function called when a save is selected by the user 

	@return: -
	@rtype: void
	"""
	global saveName

	saveName = Button.getText(Menu.getButtonAt(menuList[1],Menu.getSelectedIndex(menuList[1])))

	setSceneToSelectLevel()
	
	file = open("Saves/"+saveName+"/player.stats","r")
	content = file.read()
	file.close()
	exec(content)

	Menu.removeAllButtons(menuList[2])

	xPos,yPos = 0,1
	for i in range(0,maxLvlUnlocked+1):
		if(str(i) in os.listdir("Levels")):
			Menu.addButton(menuList[2],Button.Button(str(i),xPos,yPos,onLevelSelected))
			yPos += 6
			if(yPos >= 6*7+1):
				yPos = 1
				xPos += 9+len(str(i))
	Menu.setSelectedIndex(menuList[2],Menu.getButtonsNumber(menuList[2])-1)

	return

def onNewGamePressed():
	"""
	Function called when user ask to create a new game
	@return: -
	@rtype: void
	"""
	global keyboard_default,menuList

	maxNameLength = 50
	
	KeyBinder.restoreKbStgs(copy.deepcopy(keyboard_default))

	name = ""
	nameLength = 0
	
	while(nameLength > maxNameLength or nameLength == 0 or os.path.exists("Saves/"+name) or "/" in name or name == "Nouvelle partie"):
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

		elif(os.path.exists("Saves/"+name) or name == "Nouvelle partie"):
			sys.stdout.write("\033[27;0H\033[2K\033[26;0H\033[2K\033[25;0H\033[2K\033[24;0H\033[2K\033[23;0H\033[2K")
			Menu.printText("Cette sauvegarde existe deja ...")

		elif("/" in name):
			sys.stdout.write("\033[27;0H\033[2K\033[26;0H\033[2K\033[25;0H\033[2K\033[24;0H\033[2K\033[23;0H\033[2K")
			Menu.printText("Navré mais il va falloir recnoncer à utiliser \"/\"")
	
	os.mkdir("Saves/"+name)
	shutil.copyfile("baseFiles/player.stats","Saves/"+name+"/player.stats")

	if(countSaves() == MAX_SAVES_NUMBER):
		Menu.removeButton(menuList[1],"Nouvelle partie")

	Menu.addButton(menuList[1],Button.Button(name,-1,5+(countSaves()-1)*SAVES_BUTTONS_SPACE,onSaveSelected,54))

	reOrganizeSaveButtons()

	if(countSaves() != MAX_SAVES_NUMBER):
		Menu.setSelectedIndex(menuList[1],countSaves())
	else:
		Menu.setSelectedIndex(menuList[1],MAX_SAVES_NUMBER-1)

	KeyBinder.initKbStgs()

	return

def onDelSavePressed():
	""" 
	Function called when user ask to delete a save
	@return: -
	@rtype: void
	"""
	global menuList

	buttonText = Button.getText(Menu.getButtonAt(menuList[1],Menu.getSelectedIndex(menuList[1])))

	if(buttonText != "Nouvelle partie"):
		Tools.sysExec("clear")
		Menu.printScreen("Pictures/comfirmDeleteSave.pic")
		sys.stdout.write("\033[16;"+str(int(round((Object.SCREEN_WIDTH/2)-(len(str(buttonText))/2))))+"H"+'\033[53;4;1m\033[38;2;200;0;0m'+buttonText)
		print("")
		key = ""
		while(key != "o" and key != "n"):
			key = KeyBinder.waitForKeyPressed()
		if(key == "o"):
			Menu.removeButton(menuList[1],buttonText)

			if(countSaves() == MAX_SAVES_NUMBER):
				Menu.addButton(menuList[1],Button.Button("Nouvelle partie",10,42,onNewGamePressed),0)
			
			shutil.rmtree("Saves/"+buttonText)

			reOrganizeSaveButtons()

			Menu.setSelectedIndex(menuList[1],0)
			return

		elif(key == "n"):
			return

	return

def reOrganizeSaveButtons():
	"""
	Re-organize all buttons of the level selection menu 

	@return: -
	@rtype: void
	"""

	saveButtonsPassed = 0 #how many buttons are already placed in the for
	for i in range(0,Menu.getButtonsNumber(menuList[1])):
		currentButton = Menu.getButtonAt(menuList[1],i)
		if(Button.getText(currentButton) != "Nouvelle partie"):
			Button.setPos(currentButton,-1,5+saveButtonsPassed*SAVES_BUTTONS_SPACE)
			saveButtonsPassed += 1

	return

def setSceneToStartMenu():
	"""
	Set current scene to the menu "PyTry"
	@return: -
	@rtype: void
	"""
	global sceneId,currentScene
	currentScene = sceneId["PyTry"]

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

def setSceneToSelectLevel():
	"""
	Set current scene to the menu "Select level"
	@return: -
	@rtype: void
	"""
	global sceneId,currentScene
	currentScene = sceneId["Select level"]

	return

def setSceneToLevel():
	"""
	Set current scene to the real game, the \"level\"
	@return: -
	@rtype: void
	"""
	global sceneId,currentScene
	currentScene = sceneId["level"]

	return

def countSaves():
	"""
	Count how many saves exists

	@return: Number of existings saves
	@rtype: int
	"""
	
	count = len(os.listdir("Saves/"))

	return count


if(__name__ == "__main__"):
	
	main()