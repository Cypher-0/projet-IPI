# -*- coding: utf-8 -*-

"""File containing definition of a enemy """

from PyTry import *
import Shot

import time
import sys
import random
from random import randint
from math import sin

attributesList = ["fireTimeSpace","lastShot","shotList","shotSpeed","life","scoreValue","moveFunction","startY","damageValue","isDead"]
#fireTimeSpace : float : time between 2 shots
#lastShot : float : time corresponding to last shot done
#shotList : list of objects of type "Shots" : all shots fired from the enemy. Each one is erase if it's out of the screen
#shotSpeed : float : enemy's shot speed on screen

#life : float : enemy's life [0;100]
#scoreValue : float : score to give to the player when enemy destroyed
#moveFunction : str : y = f(x)
#startY : float : enemy start point on y axis
#damageValue : float : how much damage per shot
#isDead : bool : is the enemy dead or not ? Used to keep shots on screen even if enemy killed

"""
\"Enemy\" type attributes list
@type: list
"""

RAND_INTERVAL  = 30
"""Enemy caracteristics can be +- RAND_INTERVAL % """

dt = Object.dt
"""dt used in calcs"""

##########################
#
#	Constructor
#
##########################

enemyColor = [255,150,0]

def Enemy(enemyName,yPos = None):
	"""
	\"Enemy\" type constructor

	@param enemyName: enemy name used to load from config file
	@type enemyName: str

	@param yPos: enemy y start position
	@type yPos: float

	@return: Dictionnary containing all informations about enemy
	@rtype: dict
	"""

	assert type(enemyName) is str


	startX = Object.SCREEN_WIDTH-2-30
	startY = int(round(Object.SCREEN_HEIGHT/2))
	
	datas = Tools.createDatasFromPic("Enemys/"+enemyName+"/image.pic")
	object = Item.Item(datas)

	Object.setColor(object,enemyColor)
	

	object["lastShot"] = 0
	object["shotList"] = []

	file = open("Enemys/"+enemyName+"/config","r")
	content = file.read()
	file.close()
	exec(content)

#datas loaded from "exec" command
	#enemy proprieties
	object["fireTimeSpace"] = fireTimeSpace+random.random()*RAND_INTERVAL/100*fireTimeSpace
	object["shotSpeed"] = shotSpeed+random.random()*RAND_INTERVAL/100*shotSpeed
	object["life"] = life
	object["scoreValue"] = scoreValue
	object["damageValue"] = damageValue+random.random()*RAND_INTERVAL/100*damageValue
	object["moveFunction"] = moveFunction
	object["startY"] = startY
	object["isDead"] = False
	#enemy position
	Object.setX(object,startX)
	if(yPos != None):
		startY = yPos
	Object.setY(object,startY)
	#enemy speed and acceleration
	Item.setVX(object,vX+random.random()*RAND_INTERVAL/100*vX)
	Item.setVY(object,vY+random.random()*RAND_INTERVAL/100*vY)
	Item.setAX(object,aX+random.random()*RAND_INTERVAL/100*aX)
	Item.setAY(object,aY+random.random()*RAND_INTERVAL/100*aY)

	return object


#def EnemyMan(datas,x,y,fireTimeSpace):
	"""
	\"Enemy\" type constructor, to used "manually"

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

#	assert type(fireTimeSpace) is int or float

#	object = Item.Item(datas,x,y,enemyColor)
#	object["fireTimeSpace"] = float(fireTimeSpace)
#	object["lastShot"] = 0
#	object["shotList"] = []
#	object["shotSpeed"] = 50
#	object["life"] = 100

#	return object

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
	assert type(enemy) is dict,"Current is : %r" % enemy
	for i in range(0,len(attributesList)):
		assert attributesList[i] in enemy.keys(),"\"Enemy\" type expect %r key."%attributesList[i]

	return

def interact(enemy):
	"""
	Manage interactions and movements of enemy and his fires
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@return: Have the enemy to be removed from the enemyList or not
	@rtype: bool
	"""
	assertenemy(enemy)

	if(time.time()-enemy["lastShot"] > enemy["fireTimeSpace"] and not(enemy["isDead"])):
		enemy["shotList"].append(Shot.Shot(Object.getX(enemy),Object.getY(enemy)+int(Item.getBaseHeight(enemy)/2),enemy["shotSpeed"],enemy["damageValue"]))
		enemy["lastShot"] = time.time()


	for i in range(0,len(enemy["shotList"])):
		Item.move(enemy["shotList"][i],dt)

	for i in enemy["shotList"]:
		if(Object.getX(i) <= 0):
			enemy["shotList"].remove(i)
			del i

	Item.move(enemy,dt)
	if(enemy["moveFunction"] != None):
		nextY = enemy["startY"]+eval(enemy["moveFunction"])
		if(nextY < Object.SCREEN_HEIGHT-6 and nextY > 4):
			Object.setY(enemy,nextY)

	return enemy["isDead"] and len(enemy["shotList"]) == 0

def kill(enemy):
	"""
	Virtually kill \"enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict
	"""
	assertenemy(enemy)

	enemy["isDead"] = True

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

	if(not(enemy["isDead"])):
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

def getShotList(enemy):
	"""
	Get content of \"shotList\" key from \"enemy\"
	@param enemy: Dictionnary containing all information about one \"enemy\" object
	@type enemy: dict

	@return: -
	@rtype: void
	"""
	assertenemy(enemy)

	return enemy["shotList"]

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


def getDamageValue(enemy):
	"""
	Get content of \"damageValue\" key from \"enemy\"
	@param enemy: Dictionnary containing all information about one \"enemy\" object
	@type enemy: dict

	@return: content of \"damageValue\" key from \"enemy\"
	@rtype: float
	"""
	assertenemy(enemy)

	return enemy["damageValue"]

def getScoreValue(enemy):
	"""
	Get content of \"scoreValue\" key from \"enemy\"
	@param enemy: Dictionnary containing all information about one \"enemy\" object
	@type enemy: dict

	@return: content of \"scoreValue\" key from \"enemy\"
	@rtype: float
	"""
	assertenemy(enemy)

	return enemy["scoreValue"]

def getIsDead(enemy):
	"""
	Get content of \"isDead\" key from \"enemy\"
	@param enemy: Dictionnary containing all information about one \"enemy\" object
	@type enemy: dict

	@return: content of \"isDead\" key from \"enemy\"
	@rtype: bool
	"""
	assertenemy(enemy)

	return enemy["isDead"]

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


def setMoveFunction(enemy,value):
	"""
	Get content of \"life\" key from \"Enemy\"
	@param enemy: Dictionnary containing all information about one \"Enemy\" object
	@type enemy: dict

	@param value: new value for the content of \"life\" key from \"Enemy\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assert type(value) is str
	assertenemy(enemy)

	enemy["moveFunction"] = value

	return

def setDamageValue(enemy,value):
	"""
	Set content of \"damageValue\" key from \"enemy\"
	@param enemy: Dictionnary containing all information about one \"enemy\" object
	@type enemy: dict

	@param value: new value for the content of \"damageValue\" key from \"enemy\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assert type(value) is float or int
	assertenemy(enemy)

	enemy["damageValue"] = float(value)

	return


##########################
#
#	Internale tests
#
##########################

if(__name__ == "__main__"):
	Tools.sysExec("clear")
	e0 = Enemy("balloon")
	Object.show(e0)
	Tools.goAt(1,47)