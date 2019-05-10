# -*- coding: utf-8 -*-

"""File containing definition of a enemy """

from PyTry import *
import Shot

import time
import sys

attributesList = ["fireTimeSpace","lastShot","shotList","shotSpeed","life","scoreValue"]
#fireTimeSpace : float : time between 2 shots
#lastShot : float : time corresponding to last shot done
#shotList : list of objects of type "Shots" : all shots fired from the enemy. Each one is erase if it's out of the screen
#shotSpeed : float : enemy's shot speed on screen

#life : float : enemy's life [0;100]
#startBlink : float : time when enemy started blinking
#blinkTime : float : enemy will blink during this time

"""
\"Enemy\" type attributes list
@type: list
"""

dt = Object.dt

##########################
#
#	Constructor
#
##########################

enemyColor = [255,0,0]

def Enemy(datas,x,y,fireTimeSpace):
	"""
	\"Enemy\" type constructor

	@param datas: enemy appareance to display
	@type datas: list
	
	@param x: x start position 
	@type x: float

	@param y: y start position
	@type y: float

	@param fireTimeSpace: time between two shots fire
	@type type: float

	@return: Dictionnary containing all informations about enemy
	@rtype: dict
	"""
	object = Item.Item(datas,x,y,enemyColor)
	object["fireTimeSpace"] = fireTimeSpace
	object["lastShot"] = 0
	object["shotList"] = []
	object["shotSpeed"] = 50
	object["life"] = 100

	return object

def takeDamage(enemy,amount):
	"""
	Inflict \"amount\" damages to \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@param amount: amount of damage to apply
	@type amount: float

	@return: -
	@rtype: void
	"""

	assertenemy(enemy)
	assert type(amount) is int or type(amount) is float

	enemy["life"] -= amount
	if(enemy["life"] < 0):
		enemy["life"] = 0

	return


##########################
#
#	Procedures
#
##########################

def assertenemy(enemy):
	"""
	Assert enemy is at least corresponding to \"Enemy\" type criterias
	@param enemy: object to test
	@type enemy: dict
	@return: -
	@rtype: void
	"""
	assert type(enemy) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in enemy.keys(),"\"Enemy\" type expect %r key."%attributesList[i]

	return

def interact(enemy):
	"""
	Manage interactions and movements of enemy and his fires
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@return: -
	@rtype: void
	"""
	assertenemy(enemy)

	if(time.time()-enemy["lastShot"] > enemy["fireTimeSpace"]):
		enemy["shotList"].append(Shot.Shot(Object.getX(enemy)+Item.getBaseWidth(enemy),Object.getY(enemy)+int(Item.getBaseHeight(enemy)/2),enemy["shotSpeed"],False))
		enemy["lastShot"] = time.time()


	rmCount = 0
	for i in range(0,len(enemy["shotList"])):
		Item.move(enemy["shotList"][i],dt)
		if(Object.getX(enemy["shotList"][i]) > Object.SCREEN_WIDTH):
			rmCount += 1

	for i in range(0,rmCount):
		del enemy["shotList"][i]

	return


def show(enemy):
	"""
	Display enemy and his fires

	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@return: -
	@rtype: void
	"""
	assertenemy(enemy)

	sys.stdout.write("\033[1m")
	for i in range(0,len(enemy["shotList"])):
		Object.show(enemy["shotList"][i])
	#sys.stdout.write("\033[0m")

	Object.show(enemy)

	return


##########################
#
#	Getters
#
##########################

def getfireTimeSpace(enemy):
	"""
	Get content of \"fireTimeSpace\" key from \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@return: content of \"fireTimeSpace\" key from \"Enemy\"
	@rtype: float
	"""
	assertenemy(enemy)

	return enemy["fireTimeSpace"]

def getShotSpeed(enemy):
	"""
	Get content of \"shotSpeed\" key from \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@return: -
	@rtype: void
	"""
	assertenemy(enemy)

	return enemy["shotSpeed"]

def getLife(enemy):
	"""
	Get content of \"life\" key from \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@return: content of \"life\" key from \"Enemy\"
	@rtype: float
	"""
	assertenemy(enemy)

	return enemy["life"]



##########################
#
#	Setters
#
##########################

def setFireTimeSpace(enemy,value):
	"""
	Set content of \"fireTimeSpace\" key from \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@param value: new value for the content of \"fireTimeSpace\" key from \"Enemy\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assertenemy(enemy)
	assert type(value) is float or type(value) is int
	value = float(value)

	enemy["fireTimeSpace"] = value

	return

def setShotSpeed(enemy,value):
	"""
	Set content of \"shotSpeed\" key from \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@param value: new value for the content of \"shotSpeed\" key from \"Enemy\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assertenemy(enemy)
	assert type(value) is float or type(value) is int
	value = float(value)

	enemy["shotSpeed"] = value

	return 

def setLife(enemy,value):
	"""
	Get content of \"life\" key from \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@param value: new value for the content of \"life\" key from \"Enemy\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assert type(value) is float
	assert value >= 0 and value <= 1000,"Life out of range"
	assertenemy(enemy)

	enemy["life"] = value

	return