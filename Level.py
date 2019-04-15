# -*- coding: utf-8 -*-

"""File containing definition of a game Level """

from PyTry import *
import os

attributesList = ["bgItem","fgItem","playerItem","keyBinder","enemyList"]
#bgItem : Item : background of the level
#fgItem : Item : foreGround of the level
#playerItem : Item : player avatar
#keyBinder : KeyBinder : keybinder of a level
#enemyList : list of ? : list of all ennemys

"""
\"Level\" type attributes list
@type: list
"""

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

	bgItem = Item.Item(Tools.createDatasFromPic("Levels/l0/background.pic"),0,0,[125,125,125],-5)
	fgItem =None# Item.Item(Tools.createDatasFromPic("Levels/l0/foreground.pic"),0,0,[0,255,0],-5)
	playerItem = Item.Item(Tools.createDatasFromPic("Pictures/player.pic"),0,21,[255,0,0])

	object = {"bgItem":bgItem,"fgItem":fgItem,"playerItem":playerItem,"keyBinder":None,"enemyList":None}

	kb = KeyBinder.KeyBinder(folder[folder.rfind("/")+1:])
	KeyBinder.addAction(kb,"z",movePlayerUp,object)
	KeyBinder.addAction(kb,"q",movePlayerLeft,object)
	KeyBinder.addAction(kb,"s",movePlayerDown,object)
	KeyBinder.addAction(kb,"d",movePlayerRight,object)

	object["keyBinder"] = kb

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
		Object.setX(lvl["playerItem"],x-1)

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
		Object.setX(lvl["playerItem"],x+1)

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
		Object.setY(lvl["playerItem"],y+1)

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
		Object.setY(lvl["playerItem"],y-1)

	return



##########################
#
#	Getters
#
##########################

def getPlayer(lvl):
	"""
	@param lvl: Dictionnary containing all information about one Level object
	@type lvl: dict

	@return: \"Player\" type object of the level under the form of a dict
	@rtype: dict
	"""


	return


if(__name__ == "__main__"):
	prov = Level("Levels/l0")
	movePlayerRight(prov)