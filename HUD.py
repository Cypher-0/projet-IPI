# -*- coding: utf-8 -*-

#file containing definition of "Item" type : base for all object which will move

from PyTry import *

attributesList = ["score","scoreObjective","pbLife","pbLevel"] #+Item.attributesList
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

HUD_COLOR = [0,0,220]

def HUD(scoreObjective):
	"""

	@param scoreObjective: Score to reach to finish level
	@type scoreObjective: int

	@return: dict containing all information about one "HUD" object
	@rtype: dict
	"""

	pbLife = ProgressBar.ProgressBar(70,35,43,HUD_COLOR)
	pbLevel = ProgressBar.ProgressBar(150,4,2,HUD_COLOR)
	hud = {"score":0,"scoreObjective":scoreObjective,"pbLife":pbLife,"pbLevel":pbLevel}



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
	@param hud: Dictionnary containing all information about one \"HUD\" object
	@type hud: dict

	@return: -
	@rtype: void
	"""

	Object.show(hud["pbLife"])
	Object.show(hud["pbLevel"])

	return