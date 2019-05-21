# -*- coding: utf-8 -*-

"""File containing definition of a Player """

from PyTry import *
import Shot

import time
import sys

attributesList = ["fireTimeSpace","lastShot","shotList","shotSpeed","life"]#+item
#fireTimeSpace : float : time between 2 shots
#lastShot : float : time corresponding to last shot done
#shotList : list of objects of type "Shots" : all shots fired from the player. Each one is erase if it's out of the screen
#shotSpeed : float : player's shot speed on screen

#life : float : player's life [0;100]
#startBlink : float : time when player started blinking
#blinkTime : float : player will blink during this time

"""
\"Player\" type attributes list
@type: list
"""

MAX_LIFE = 100

dt = Object.dt
"""dt used in calcs"""
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
	object["shotSpeed"] = 50
	object["life"] = 100

	return object

def takeDamage(player,amount):
	"""
	Inflict \"amount\" damages to \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param amount: amount of damage to apply
	@type amount: float

	@return: -
	@rtype: void
	"""

	assertPlayer(player)
	assert type(amount) is int or type(amount) is float

	player["life"] -= amount
	if(player["life"] < 0):
		player["life"] = 0

	return


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


	for i in range(0,len(player["shotList"])):
		Item.move(player["shotList"][i],dt)

	for i in player["shotList"]:
		if(Object.getX(i) >= Object.SCREEN_WIDTH):
			del i

	return

def delShotAt(player,index):
	"""
	Delete player's shot at specified index
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: -
	@rtype: void
	"""
	assertPlayer(player)
	assert type(index) is int

	del player["shotList"][i]


def show(player):
	"""
	Display player and his fires

	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: -
	@rtype: void
	"""
	assertPlayer(player)

	sys.stdout.write("\033[1m")
	for i in range(0,len(player["shotList"])):
		Object.show(player["shotList"][i])
	#sys.stdout.write("\033[0m")

	Object.show(player)

	return


##########################
#
#	Getters
#
##########################

def getfireTimeSpace(player):
	"""
	Get content of \"fireTimeSpace\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"fireTimeSpace\" key from \"player\"
	@rtype: float
	"""
	assertPlayer(player)

	return player["fireTimeSpace"]

def getShotSpeed(player):
	"""
	Get content of \"shotSpeed\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: -
	@rtype: void
	"""
	assertPlayer(player)

	return player["shotSpeed"]

def getLife(player):
	"""
	Get content of \"life\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"life\" key from \"player\"
	@rtype: float
	"""
	assertPlayer(player)

	return player["life"]

def getShotList(player):
	"""
	Get content of \"shotList\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: -
	@rtype: void
	"""
	assertPlayer(player)

	return player["shotList"]


##########################
#
#	Setters
#
##########################

def setFireTimeSpace(player,value):
	"""
	Set content of \"fireTimeSpace\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param value: new value for the content of \"fireTimeSpace\" key from \"player\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assertPlayer(player)
	assert type(value) is float or type(value) is int
	value = float(value)

	player["fireTimeSpace"] = value

	return

def setShotSpeed(player,value):
	"""
	Set content of \"shotSpeed\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param value: new value for the content of \"shotSpeed\" key from \"player\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assertPlayer(player)
	assert type(value) is float or type(value) is int
	value = float(value)

	player["shotSpeed"] = value

	return 

def setLife(player,value):
	"""
	Get content of \"life\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param value: new value for the content of \"life\" key from \"player\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assert type(value) is float
	assert value >= 0 and value <= 1000,"Life out of range"
	assertPlayer(player)

	player["life"] = value

	return