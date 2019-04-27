# -*- coding: utf-8 -*-

"""File containing definition of a game Level """

from PyTry import *
import os
import time
import sys




dt = 0.08 #à chhanger




attributesList = ["bgItem0","bgItem1","fgItem0","fgItem1","playerItem","keyBinder","enemyList"] #+Item.attributesList
#bgItem0 : Item : background of the level (part 1) #2 parts are used to allow a smooth screen renewal
#fgItem0 : Item : foreGround of the level (part 1)
#bgItem1 : Item : background of the level (part 2)
#fgItem1 : Item : foreGround of the level (part 2)

#playerItem : Item : player avatar
#keyBinder : KeyBinder : keybinder of a level
#enemyList : list of ? : list of all ennemys

"""
\"Level\" type attributes list
@type: list
"""

bgSpeed = -30

##########################
#
#	Constructor
#
##########################

def Level(folder):
	"""
	\"Level\" type constructor
	@param folder: Folder containing all informations about the level
	@type folder: str

	@return: Dictionnary containing all informations about level
	@rtype: dict
	"""
	assert type(folder) is str

	lsFiles = os.listdir(folder)
	assert "background.pic" in lsFiles, "Load level from %r failed : missing file : background.pic" % folder
	#assert "foreground.pic" in lsFiles, "Load level from %r failed : missing file : foreground.pic" % folder

	bgItem0 = Item.Item(Tools.createDatasFromPic("Levels/l0/background.pic",True),0,0,[125,125,125],bgSpeed)
	bgItem1 = Item.Item(Tools.createDatasFromPic("Levels/l0/background.pic",True),Item.getBaseWidth(bgItem0)+1,0,[125,125,125],bgSpeed)
	fgItem0 =None# Item.Item(Tools.createDatasFromPic("Levels/l0/foreground.pic"),0,0,[0,255,0],bgSpeed)
	fgItem1 =None# Item.Item(Tools.createDatasFromPic("Levels/l0/foreground.pic"),Item.getBaseWidth(fgItem0)+1,0,[0,255,0],bgSpeed)
	playerItem = Item.Item(Tools.createDatasFromPic("Pictures/player.pic"),0,21,[255,0,0])

	object = {"bgItem0":bgItem0,"bgItem1":bgItem1,"fgItem0":fgItem0,"fgItem1":fgItem1,"playerItem":playerItem,"keyBinder":None,"enemyList":None}

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

	#Object.show(lvl["bgItem0"])
	#Object.show(lvl["bgItem1"])
	showBackground(lvl,lvl["bgItem0"])
	showBackground(lvl,lvl["bgItem1"])
	#Object.show(lvl["fgItem0"])
	#Object.show(lvl["fgItem1"])

	#for a in lvl["enemyList"]:
	#	Object.show(a)

	Object.show(lvl["playerItem"])


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
	x = Object.getX(lvl["bgItem1"])
	#place part 1 of the background after the part 2
	if(x < 1 and x > 0):
		Object.setX(lvl["bgItem0"],Item.getBaseWidth(lvl["bgItem0"])+1)
	#place part 2 of the background after the part 1
	x = Object.getX(lvl["bgItem0"])
	if(x < 1 and x > 0):
		Object.setX(lvl["bgItem1"],Item.getBaseWidth(lvl["bgItem1"])+1)

	#Item.move(lvl["fgItem0"],dt)


	return

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
	if(x > 0):
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
	if(x < Object.SCREEN_WIDTH-1):
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
	if(y < Object.SCREEN_HEIGHT-1):
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
		tempstr+"".join(map(str,temp[int(X):int(Object.SCREEN_WIDTH-X)]))+"\n"
		Tools.prDly(tempstr)
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
