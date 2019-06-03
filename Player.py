# -*- coding: utf-8 -*-

"""File containing definition of a Player """

from PyTry import *
import Shot

import time
import sys
import os

attributesList = ["fireTimeSpace","lastShot","shotList","shotSpeed","life","maxLife","immuteTime","lastDmgTime","isImmute","damageValue","playerName"]#+item
#fireTimeSpace : float : time between 2 shots
#lastShot : float : time corresponding to last shot done
#shotList : list of objects of type "Shots" : all shots fired from the player. Each one is erase if it's out of the screen
#shotSpeed : float : player's shot speed on screen

#life : float : player's life min=0
#maxLife : float : player's life max value

#immuteTime : float : Player can't take damage during this time from "lastDmgTime"
#lastDmgTime : float : player last damage time, used to calculate immunity time
#isImmute : bool : can the player take damage ?
#damageValue : float : how much damage per shot
#playerName : str : save name of current player

"""
\"Player\" type attributes list
@type: list
"""

dt = Object.dt
"""dt used in calcs"""

##########################
#
#	Constructor
#
##########################

playerColor = [255,0,0]

def Player(datas,x,y,fireTimeSpace,maxLife,playerName):
	"""
	\"Player\" type constructor

	@param datas: Player appareance to display
	@type datas: list
	
	@param x: x start position 
	@type x: float

	@param y: y start position
	@type y: float

	@param fireTimeSpace: time between two shots fire
	@type fireTimeSpace: float

	@param playerName: Save name of the player. Used to know where to save player stats.
	@type playerName: str

	@return: Dictionnary containing all informations about player
	@rtype: dict
	"""

	assert type(fireTimeSpace) is float or int,"Current type is : %r, expected is : %r"%(type(fireTimeSpace),"float or int")
	assert type(maxLife) is float or int,"Current type is : %r, expected is : %r"%(type(maxLife),"float or int")
	assert type(playerName) is str,"Current type is : %r, expected is : %r"%(type(playerName),"str")

	object = Item.Item(datas,x,y,playerColor)
	object["fireTimeSpace"] = fireTimeSpace
	object["lastShot"] = 0
	object["shotList"] = []
	object["shotSpeed"] = 50
	object["life"] = maxLife
	object["maxLife"] = maxLife
	object["playerName"] = playerName

	object["immuteTime"] = 1
	object["lastDmgTime"] = 0
	object["isImmute"] = False
	object["damageValue"] = 0

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
		player["shotList"].append(Shot.Shot(Object.getX(player)+Item.getBaseWidth(player),Object.getY(player)+int(Item.getBaseHeight(player)/2),player["shotSpeed"],player["damageValue"],False,[255,0,255]))
		player["lastShot"] = time.time()


	for i in range(0,len(player["shotList"])):
		Item.move(player["shotList"][i],dt)

	for i in player["shotList"]:
		if(Object.getX(i) >= Object.SCREEN_WIDTH):
			player["shotList"].remove(i)
			del i

	if(player["isImmute"]):
		if(time.time() - player["lastDmgTime"] >= player["immuteTime"]):
			player["isImmute"] = False

	return

def giveImmute(player,timeL):
	"""
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param timeL: Player immunity time
	@type timeL: float

	@return: -
	@rtype: void
	"""
	player["lastDmgTime"] = time.time()
	player["immuteTime"] = timeL
	player["isImmute"] = True

	return


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

	if(player["isImmute"] == True):
		return

	assert type(amount) is int or type(amount) is float

	player["life"] -= amount
	if(player["life"] < 0):
		player["life"] = 0

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

	sys.stdout.write("\033[1m")
	for i in range(0,len(player["shotList"])):
		Object.show(player["shotList"][i])
	if(player["isImmute"]):
		sys.stdout.write("\033[0;5m")

	Object.show(player)
	sys.stdout.write("\033[0m")

	return

def writePlayerStats(player,maxLvlUnlocked = None,addLvl = 0):
	"""
	Write player's stats in his stats file.
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param maxLvlUnlocked: Max unlocked level by the player.| If == None, it will not change | if == -1, maxLvlUnlocked will be incremented of \"addLvl\" from current player's maxLvlUnlocked
	@type maxLvlUnlocked: int

	@param addLvl: how many more levels the players should have access now  
	@type addLvl: int

	@return: 1 if file not found | 0 otherwise
	@rtype: void
	"""
	assertPlayer(player)
	assert maxLvlUnlocked == None or type(maxLvlUnlocked) is int,"Current type is : %r, expected is : %r"%(type(maxLvlUnlocked),"int")

	if(not(os.path.isfile("Saves/"+player["playerName"]+"/player.stats"))): #if file not found
		return

	if(maxLvlUnlocked == None):
		tmpMax = getMaxLvlUnlocked(player)
		maxLvlUnlocked = tmpMax if(tmpMax != -1) else 0
	elif(maxLvlUnlocked == -1):
		maxLvlUnlocked = getMaxLvlUnlocked(player)+1

	text = "fireTimeSpace = "+str(player["fireTimeSpace"])+"\n"
	text += "shotSpeed = "+str(player["shotSpeed"])+"\n"
	text += "life = "+str(player["maxLife"])+"\n"
	text += "damageValue = "+str(player["damageValue"])+"\n"
	text += "maxLvlUnlocked = "+str(maxLvlUnlocked)+"\n"


	file = open("Saves/"+player["playerName"]+"/player.stats","w")
	file.write(text)
	file.close()


	return 0


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

	@return: content of \"shotSpeed\" key from \"player\"
	@rtype: float
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

def getMaxLife(player):
	"""
	Get content of \"maxLife\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"maxLife\" key from \"player\"
	@rtype: float
	"""
	assertPlayer(player)

	return player["maxLife"]

def getShotList(player):
	"""
	Get content of \"shotList\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"shotList\" key from \"player\"
	@rtype: list
	"""
	assertPlayer(player)

	return player["shotList"]

def getDamageValue(player,):
	"""
	Get content of \"damageValue\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"damageValue\" key from \"player\"
	@rtype: float
	"""
	assertPlayer(player)

	return player["damageValue"]


def getPlayerName(player):
	"""
	Get content of \"playerName\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: content of \"playerName\" key from \"player\"
	@rtype: str
	"""
	assertPlayer(player)

	return player["playerName"]

def getMaxLvlUnlocked(player):
	"""
	Get how many levels the player unlocked
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@return: max level unlocked by the player | -1 if player's save not found or maxLvlUnlocked parameter not found
	@rtype: int
	"""
	assertPlayer(player)

	maxLvlUnlocked = 0

	if(not(os.path.isfile("Saves/"+player["playerName"]+"/player.stats"))): #if file not found
		return -1

	file = open("Saves/"+player["playerName"]+"/player.stats","r")
	content = file.read()
	file.close()

	#search maxLvlUnlocked in existing file
	if(content.find("maxLvlUnlocked") != -1):
		content = content[content.find("maxLvlUnlocked"):]
		content = content.replace(" ","")
		content = content.replace("\n","")
		content = content.replace("\r","")
		tmpList = content.split("=")
		maxLvlUnlocked = int(tmpList[1]) if(len(tmpList) == 2) else 0
	else:
		return -1

	return maxLvlUnlocked


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
	Set content of \"life\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param value: new value for the content of \"life\" key from \"player\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assert type(value) is float or int
	assertPlayer(player)
	assert value >= 0 and value <= player["maxLife"],"Life out of range"

	player["life"] = float(value)

	return

def setMaxLife(player,value):
	"""
	Set content of \"maxLife\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param value: new value for the content of \"maxLife\" key from \"player\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assert type(value) is float or int
	assert value >= 0
	assertPlayer(player)

	player["maxLife"] = float(value)

	return

def setDamageValue(player,value):
	"""
	Set content of \"damageValue\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param value: new value for the content of \"damageValue\" key from \"player\"
	@type value: float

	@return: -
	@rtype: void
	"""
	assert type(value) is float or int
	assertPlayer(player)

	player["damageValue"] = float(value)

	return

def setPlayerName(player,playerName):
	"""
	Set content of \"playerName\" key from \"player\"
	@param player: Dictionnary containing all information about one \"Player\" object
	@type player: dict

	@param playerName: New value for content of \"playerName\" key from \"player\"
	@type playerName: str

	@return: -
	@rtype: void
	"""
	assertPlayer(player)
	assert type(playerName) is str,"Current type is : %r, expected is : %r"%(type(playerName),"str")

	player["playerName"] = playerName