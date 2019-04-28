# -*- coding: utf-8 -*-

"""File containing definition of a Player """

from PyTry import *
import Shot

import time

attributesList = ["fireTimeSpace","lastShot","shotList","shotSpeed"]
#fireTimeSpace : float : time between 2 shots
#lastShot : float : time corresponding to last shot done
#shotList : list of objects of type "Shots" : all shots fired from the player. Each one is erase if it's out of the screen
#shotSpeed : float : player's shot speed on screen

"""
\"Player\" type attributes list
@type: list
"""

dt = Object.dt

##########################
#
#	Constructor
#
##########################

playerColor = [255,0,0]

def Player(datas,x,y,fireTimeSpace):
	"""
	\"Player\" type constructor

	@param datas: Player appareance to display
	@type datas: list
	
	@param x: x start position 
	@type x: float

	@param y: y start position
	@type y: float

	@param fireTimeSpace: time between two shots fire
	@type type: float

	@return: Dictionnary containing all informations about player
	@rtype: dict
	"""
	object = Item.Item(datas,x,y,playerColor)
	object["fireTimeSpace"] = fireTimeSpace
	object["lastShot"] = 0
	object["shotList"] = []
	object["shotSpeed"] = 30

	return object


##########################
#
#	Procedures
#
##########################

def assertPlayer(player):
	"""
	Assert player is at least corresponding to \"Player\" type criterias
	@param player: object to test
	@type player: dict
	@return: -
	@rtype: void
	"""
	assert type(player) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in player.keys(),"\"Player\" type expect %r key."%attributesList[i]

	return

def interact(player):
	"""
	Manage interactions and movements of player and his fires
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: -
	@rtype: void
	"""
	assertPlayer(player)

	if(time.time()-player["lastShot"] > player["fireTimeSpace"]):
		player["shotList"].append(Shot.Shot(Object.getX(player)+Item.getBaseWidth(player),Object.getY(player)+int(Item.getBaseHeight(player)/2),player["shotSpeed"],False))
		player["lastShot"] = time.time()


	rmCount = 0
	for i in range(0,len(player["shotList"])):
		Item.move(player["shotList"][i],dt)
		if(Object.getX(player["shotList"][i]) > Object.SCREEN_WIDTH):
			rmCount += 1

	for i in range(0,rmCount):
		del player["shotList"][i]

	return


def show(player):
	"""
	Display player and his fires

	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: -
	@rtype: void
	"""
	assertPlayer(player)

	for i in range(0,len(player["shotList"])):
		Object.show(player["shotList"][i])

	Object.show(player)

	return


##########################
#
#	Getters
#
##########################

def getfireTimeSpace(player):
	"""
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"fireTimeSpace\" key from \"player\"
	@rtype: float
	"""
	assertPlayer(player)

	return player["fireTimeSpace"]



##########################
#
#	Setters
#
##########################

def getfireTimeSpace(player):
	"""
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"fireTimeSpace\" key from \"player\"
	@rtype: float
	"""
	assertPlayer(player)

	return player["fireTimeSpace"]
