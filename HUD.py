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




	return

##########################
#
#	Procedures
#
##########################

