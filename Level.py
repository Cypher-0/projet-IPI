# -*- coding: utf-8 -*-

"""File containing definition of a game Level """

from PyTry import *
import Player
import HUD
import Shot

import os
import time
import sys

dt = Object.dt

attributesList = ["bgItem0","bgItem1","fgItem0","fgItem1","playerItem","keyBinder","enemyList","HUD","playerScore"] #+Item.attributesList
#bgItem0 : Item : background of the level (part 1) #2 parts are used to allow a smooth screen renewal
#fgItem0 : Item : foreGround of the level (part 1)
#bgItem1 : Item : background of the level (part 2)
#fgItem1 : Item : foreGround of the level (part 2)

#playerItem : Player : player avatar
#keyBinder : KeyBinder : keybinder of a level
#enemyList : list of ? : list of all ennemys

"""
\"Level\" type attributes list
@type: list
"""

fgSpeed = -50

##########################
#
#	Constructor
#
##########################

def Level(folder,saveName):
	"""
	\"Level\" type constructor
	@param folder: Folder containing all informations about the level
	@type folder: str

	@param saveName: Path to save folder of current player
	@type saveName: str

	@return: Dictionnary containing all informations about level
	@rtype: dict
	"""
	assert type(folder) is str

	lsFiles = os.listdir(folder)
	assert "background.pic" in lsFiles, "Load level from %r failed : missing file : background.pic" % folder
	#assert "foreground.pic" in lsFiles, "Load level from %r failed : missing file : foreground.pic" % folder

	bgItem0 = Item.Item(Tools.createDatasFromPic("Levels/l0/background.pic",True),0,0,[70,70,70],fgSpeed+30)
	bgItem1 = Item.Item(Tools.createDatasFromPic("Levels/l0/background.pic",True),Item.getBaseWidth(bgItem0),0,[70,70,70],fgSpeed+30)

	fgItem0 = Item.Item(Tools.createDatasFromPic("Levels/l0/foreground.pic"),0,0,[0,170,0],fgSpeed)
	fgItem1 = Item.Item(Tools.createDatasFromPic("Levels/l0/foreground.pic"),Item.getBaseWidth(fgItem0)-1,0,[0,170,0],fgSpeed)

	playerItem = loadPlayer(saveName)

	hud = HUD.HUD(2000,Player.MAX_LIFE)

	object = {"bgItem0":bgItem0,"bgItem1":bgItem1,"fgItem0":fgItem0,"fgItem1":fgItem1,"playerItem":playerItem,"keyBinder":None,"enemyList":None,"HUD":hud,"playerScore":0}

	kb = KeyBinder.KeyBinder(folder[folder.rfind("/")+1:])
	KeyBinder.addAction(kb,"z",movePlayerUp,object)
	KeyBinder.addAction(kb,"q",movePlayerLeft,object)
	KeyBinder.addAction(kb,"s",movePlayerDown,object)
	KeyBinder.addAction(kb,"d",movePlayerRight,object)

	object["keyBinder"] = kb

	Item.setVX(object["playerItem"],2.)
	Item.setVY(object["playerItem"],1.)

	return object



##########################
#
#	Procedures
#	
##########################

def assertLevel(level):
	"""
	Assert level is at least corresponding to \"Level\" type criterias
	@param level: object to test
	@type level: dict
	@return: True if correct \"Level\" type. The procedure stop if it's not
	@rtype: bool
	"""
	assert type(level) is dict,"Current type is : %r" % type(level)
	for i in range(0,len(attributesList)):
		assert attributesList[i] in level.keys(),"\"Level\" type expect %r key."%attributesList[i]

	return True #return true if "object" is a correct "Level"

def show(lvl):
	"""
	Display level on screen
	@param lvl: Dictionnary containing all information about one \"Level\" object
	@type lvl: dict

	@return: -
	@rtype: void
	"""

	assertLevel(lvl)

	Object.show(lvl["bgItem0"])
	Object.show(lvl["bgItem1"])
	#showBackground(lvl,lvl["bgItem0"])
	#showBackground(lvl,lvl["bgItem1"])
	
	Object.show(lvl["fgItem0"])
	Object.show(lvl["fgItem1"])

	#for a in lvl["enemyList"]:
	#	Object.show(a)

	Player.show(lvl["playerItem"])

	HUD.show(lvl["HUD"])

	return

def interact(lvl):
	"""
	Interaction inside the level
	@param lvl: Dictionnary containing all information about one \"Level\" object
	@type lvl: dict

	@return: -
	@rtype: void
	"""

	assertLevel(lvl)

	KeyBinder.interact(lvl["keyBinder"])

	Item.move(lvl["bgItem0"],dt)
	Item.move(lvl["bgItem1"],dt)
	Item.move(lvl["fgItem0"],dt)
	Item.move(lvl["fgItem1"],dt)

	# ------- Manage background and foreground

	x = Object.getX(lvl["bgItem1"])
	baseWidth = Item.getBaseWidth(lvl["bgItem0"])
	#place part 1 of the background after the part 0
	if(x <= -baseWidth):
		Object.setX(lvl["bgItem1"],baseWidth)

	#place part 0 of the background after the part 1
	x = Object.getX(lvl["bgItem0"])
	if(x <= -baseWidth):
		Object.setX(lvl["bgItem0"],baseWidth)



	x = Object.getX(lvl["fgItem1"])
	baseWidth = Item.getBaseWidth(lvl["fgItem0"])
	#place part 1 of the background after the part 2
	if(x <= -baseWidth):
		Object.setX(lvl["fgItem1"],baseWidth)

	#place part 2 of the background after the part 1
	x = Object.getX(lvl["fgItem0"])
	if(x <= -baseWidth):
		Object.setX(lvl["fgItem0"],baseWidth)



	Player.interact(lvl["playerItem"])

	# ----------- Manage collisions
	if(Item.tryCollide(lvl["fgItem0"],lvl["playerItem"]) or Item.tryCollide(lvl["fgItem1"],lvl["playerItem"])):
		Player.takeDamage(lvl["playerItem"],20)

	for i in Player.getShotList(lvl["playerItem"]):
		Shot.assertShot(i)
		if(Item.tryCollide(lvl["fgItem0"],i) or Item.tryCollide(lvl["fgItem1"],i,True)):
			Player.getShotList(lvl["playerItem"]).remove(i)

	HUD.refreshValues(lvl["HUD"],Player.getLife(lvl["playerItem"]),lvl["playerScore"])

	return

def loadPlayer(saveName):
	"""
	Load player stats and image.
	
	@param saveName: Path to save folder of current player
	@type saveName: str

	@return: A dictionnary containing informations about one Player object
	@rtype: dict
	"""
	assert type(saveName) is str

	playerItem = Player.Player(Tools.createDatasFromPic("Pictures/player.pic"),0,21,0.5)
	
	file = open("Saves/"+saveName+"/player.stats","r")
	content = file.read()
	file.close()

	tempDict = {"fireTimeSpace":0,"shotSpeed":0,"life":0}

	lsLines = content.splitlines()
	for i in range(0,len(lsLines)):
		part1 = lsLines[i].split("=")[0]
		part2 = lsLines[i].split("=")[1]
		tempDict[part1] = float(part2)

	Player.setFireTimeSpace(playerItem,tempDict["fireTimeSpace"])
	Player.setShotSpeed(playerItem,tempDict["shotSpeed"])
	Player.setLife(playerItem,tempDict["life"])


	return playerItem

def movePlayerLeft(lvl):
	"""
	Make player move left from one gut
	@param lvl: Dictionnary containing all information about one \"Level\" object
	@type lvl: dict

	@return: -
	@rtype: void
	"""

	assertLevel(lvl)

	x = Object.getX(lvl["playerItem"])
	if(x > -10):
		Object.setX(lvl["playerItem"],x-Item.getVX(lvl["playerItem"]))

	return

def movePlayerRight(lvl):
	"""
	Make player move right from one gut
	@param lvl: Dictionnary containing all information about one \"Level\" object
	@type lvl: dict

	@return: -
	@rtype: void
	"""

	assertLevel(lvl)

	x = Object.getX(lvl["playerItem"])
	if(x < Object.SCREEN_WIDTH-10):
		Object.setX(lvl["playerItem"],x+Item.getVX(lvl["playerItem"]))

	return

def movePlayerDown(lvl):
	"""
	Make player move downward from one gut
	@param lvl: Dictionnary containing all information about one \"Level\" object
	@type lvl: dict

	@return: -
	@rtype: void
	"""

	assertLevel(lvl)

	y = Object.getY(lvl["playerItem"])
	if(y < Object.SCREEN_HEIGHT-4):
		Object.setY(lvl["playerItem"],y+Item.getVY(lvl["playerItem"]))

	return

def movePlayerUp(lvl):
	"""
	Make player move upward from one gut
	@param lvl: Dictionnary containing all information about one \"Level\" object
	@type lvl: dict

	@return: -
	@rtype: void
	"""

	assertLevel(lvl)

	y = Object.getY(lvl["playerItem"])
	if(y > 0):
		Object.setY(lvl["playerItem"],y-Item.getVY(lvl["playerItem"]))

	return



def showBackground(level,bg):
	"""
	Optimize Object.show() for background and foreground objects
	@param level: Dictionnary containing all information about one \"Level\" object
	@type level: dict

	@return: -
	@rtype: void
	"""

	temp = Object.getDatas(bg)
	tempstr= ""
	X = abs(Object.getX(bg))
	for i in range(0,len(temp)): #on parcourt l'axe Y du tableau
		tempstr+="".join(map(str,temp[i][int(X):int(Object.SCREEN_WIDTH-X)]))+"\n"
		#Tools.prDly(tempstr)
	Tools.goAt(0,0)
	sys.stdout.write(tempstr)


	return


##########################
#
#	Getters
#
##########################

def getPlayer(lvl):
	"""
	Return \"playerItem\" key value of the dict lvl (type : \"Level\")
	@param lvl: Dictionnary containing all information about one Level object
	@type lvl: dict

	@return: \"Item\" type object corresponding to the player of the level under the form of a dict
	@rtype: dict
	"""
	assertLevel(lvl)

	return lvl["playerItem"]


if(__name__ == "__main__"):
	prov = Level("Levels/l0")
	movePlayerRight(prov)
	Object.show(prov["playerItem"])
