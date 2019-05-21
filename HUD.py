# -*- coding: utf-8 -*-

#file containing definition of "Item" type : base for all object which will move

from PyTry import *

import sys

attributesList = ["score","scoreObjective","playerMaxLife","pbLife","pbLevel"] #+Item.attributesList
#score : int : player score in current level
#scoreObjcetive : int : player objective to finish the level
#pbLife : ProgressBar : player's life
#pbLevel : ProgressBar : player's progression in level

"""
\"HUD\" type attributes list
@type: list
"""

##########################
#
#	Constructor
#
##########################

HUD_COLOR = [50,200,220]

def HUD(scoreObjective,playerMaxLife):
	"""
	\"HUD\" type constructor
	@param scoreObjective: Score to reach to finish level
	@type scoreObjective: int

	@param playerMaxLife: float
	@type playerMaxLife: float

	@return: dict containing all information about one "HUD" object
	@rtype: dict
	"""

	assert type(scoreObjective) is int

	pbLife = ProgressBar.ProgressBar(70,48,46,HUD_COLOR)
	pbLevel = ProgressBar.ProgressBar(150,7,0,HUD_COLOR)
	hud = {"score":0,"scoreObjective":scoreObjective,"playerMaxLife":playerMaxLife,"pbLife":pbLife,"pbLevel":pbLevel}



	return hud

##########################
#
#	Procedures
#
##########################

def assertHUD(HUD):
	"""
	Assert HUD is at least corresponding to \"HUD\" type criterias
	@param HUD: object to test
	@type HUD: dict
	@return: -
	@rtype: void
	"""
	assert type(HUD) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in HUD.keys(),"\"HUD\" type expect %r key."%attributesList[i]

	return

def show(hud):
	"""
	Display the HUD
	@param hud: Dictionnary containing all information about one \"HUD\" object
	@type hud: dict

	@return: -
	@rtype: void
	"""
	assertHUD(hud)

	Object.show(hud["pbLife"])
	Object.show(hud["pbLevel"])
	sys.stdout.write("\033[47;80H\033[48;2;0;0;220m\033[38;5;255;255;240m"+str(hud["score"])+"\033[0m")

	return

def refreshValues(hud,life,score):
	"""
	Refresh values of the HUD
	@param hud: Dictionnary containing all information about one \"HUD\" object
	@type hud: dict

	@param life: Player's life
	@type life: float

	@param score: Player's score
	@type score: int
	"""

	assertHUD(hud)
	assert type(life) is float or int
	assert type(score) is int

	sys.stdout.write("\033[1m")
	ProgressBar.setProgressionPercent(hud["pbLife"],int(round(100*life/hud["playerMaxLife"])))
	ProgressBar.setProgressionPercent(hud["pbLevel"],int(round(100*score/hud["scoreObjective"])))

	return