# -*- coding: utf-8 -*-

"""File containing definition of a fired ammo """

from PyTry import *
import time

attributesList = ["isEnnemy"]
#isEnnemy : bool : is an ennemy fire

"""
\"Shot\" type attributes list
@type: list
"""

##########################
#
#	Constructor
#
##########################

shotColor = [255,0,255]

def Shot(x,y,vX,isEnnemy = True):
	"""
	\"Shot\" type constructor
	
	@param x: x start position 
	@type x: float

	@param y: y start position
	@type y: float

	@param vX: x speed of the shot
	@type vX: float

	@param isEnnemy: Is the shot from a friend or an ennemy
	@type isEnnemy: bool

	@return: Dictionnary containing all informations about shot
	@rtype: dict
	"""
	object = Item.Item([['*']],x,y,shotColor,vX)
	object["isEnnemy"] = isEnnemy

	return object


##########################
#
#	Procedures
#
##########################

def assertShot(shot):
	"""
	Assert shot is at least corresponding to \"Shot\" type criterias
	@param shot: object to test
	@type shot: dict
	@return: -
	@rtype: void
	"""
	assert type(shot) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in shot.keys(),"\"Shot\" type expect %r key."%attributesList[i]

	return

def delShot(shot):
	"""
	Delete designed shot
	@param shot: Dictionnary containing all information about one \"Shot\" object
	@type shot: dict
	@return: -
	@rtype: void
	"""
	assertShot(shot)
	del shot

##########################
#
#	Getters
#
##########################

def getIsEnnemy(shot):
	"""
	@param shot: Dictionnary containing all information about one \"Shot\" object
	@type shot: dict

	@return: content of \"isEnnemy\" key from \"shot\"
	@rtype: bool
	"""
	assertShot(shot)

	return shot["isEnnemy"]



##########################
#
#	Setters
#
##########################

def setIsEnnemy(shot,value):
	"""
	@param shot: Dictionnary containing all information about one \"Shot\" object
	@type shot: dict

	@return: content of \"isEnnemy\" key from \"shot\"
	@rtype: bool
	"""
	assertShot(shot)
	assert type(value) is bool,"Current type is : %r" % type(value)

	shot["isEnnemy"] = value

	return
