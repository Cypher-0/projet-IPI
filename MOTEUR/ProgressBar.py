# -*- coding: utf-8 -*-

"""
File containing definition of type \"ProgressBar\"
Use Object.show(obj) to display a ProgressBar
"""
#this type inherits of "Object"

import Object
import Item
import Tools

import copy

attributesList = copy.deepcopy(Item.attributesList);attributesList.append("progression");attributesList.append("gutsCount")#progression : int : current progression of the progress bar
#gutsCount : int : how many character represent the progression

"""
\"ProgressBar\" type attributes list
@type: list
"""

def ProgressBar(width,posX,posY,color = [255,255,255]):
	"""
	\"ProgressBar\" type constructor
	@param width: Number of gutsCount availables on the progress bar
	@type width: int

	@param posX: Position of progress bar on X axis
	@type posX: float

	@param posY: Position of progress bar on Y axis
	@type posY: float

	@param color: progressbar color, defined by following format : [r,g,b]. Each value have to be in [0;255] type(r,g,b) is int
	@type color: list

	@return: dictionnary containing all informations of created object
	@rtype: dict
	"""

	topList = []
	for i in range(0,width):
		topList.append("_")
	topList.insert(0,'')
	topList.append('')

	bottomList = list("_"*width)
	bottomList.insert(0,'|')
	bottomList.append('|')

	refList = [topList,bottomList]

	baseObject = Item.Item(copy.deepcopy(refList),posX,posY,color)

	for i in range(0,width):
		refList[1][i+1] = "#"
		Item.addSprite(baseObject,copy.deepcopy(refList))

	#Item.setSprite(baseObject,width) = max | Item.setSprite(baseObject,0) = min 

	baseObject["progression"] = 0
	baseObject["gutsCount"] = width

	return baseObject

##########################
#
#	Procedures
#
##########################

def assertProgressBar(pb):
	"""
	Assert pb is at least corresponding to \"ProgressBar\" type criterias
	@param pb: object to test
	@type pb: dict
	@return: True if correct \"ProgressBar\" type. The procedure stop if it's not
	@rtype: bool
	"""
	global attributesList
	assert type(pb) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in pb.keys(),"\"ProgressBar\" type expect %r key."%attributesList[i]

	return True #return true if "object" is a correct "ProgressBar"


##########################
#
#	Setters
#
##########################

def getGutsCount(progressBar):
	"""
	Get number of guts in \"progressBar\" object
	@param progressBar: object of type \"ProgressBar\"
	@type progressBar: dict

	@return: Number of guts in \"progressBar\" object
	@rtype: int
	"""
	assertProgressBar(progressBar)

	return progressBar["gutsCount"]

def getProgression(progressBar):
	"""
	Get number progression value of \"progressBar\" object
	@param progressBar: object of type \"ProgressBar\"
	@type progressBar: dict

	@return: Number progression value of \"progressBar\" object
	@rtype: int
	"""
	assertProgressBar(progressBar)

	return progressBar["progression"]


##########################
#
#	Setters
#
##########################

def setProgression(progressBar,value):
	"""
	Set \"progressBar\" progression value to \"value\"
	@param progressBar: object of type \"ProgressBar\"
	@type progressBar: dict

	@param value: value to set progressBar progression
	@type value: int

	@return: -
	@rtype: void
	"""
	assertProgressBar(progressBar)
	assert type(value) is int
	assert value >= 0, "value parameter have to be in [0,%r], current value is : %r" % (progressBar["gutsCount"],value)
	assert value <= progressBar["gutsCount"], "value parameter have to be in [0,%r], current value is : %r" % (progressBar["gutsCount"],value)

	progressBar["progression"] = value
	Item.setSprite(progressBar,value)

	return

def setProgressionPercent(progressBar,value):
	"""
	Set \"progressBar\" progression to a value corresponding to \"value\" in percents (0-100%)
	@param progressBar: object of type \"ProgressBar\"
	@type progressBar: dict

	@param value: value to set progressBar progression in percent (0-100%)
	@type value: int

	@return: -
	@rtype: void
	"""
	assertProgressBar(progressBar)
	assert type(value) is int
	assert value >= 0, "value parameter have to be in [0,100], current value is : %r" % (value)
	assert value <= 100, "value parameter have to be in [0,100], current value is : %r" % (value)

	value = int(round(value/100.*progressBar["gutsCount"]))

	progressBar["progression"] = value
	Item.setSprite(progressBar,value)

	return



##########################
#
#	Internal tests
#
##########################

if(__name__ == "__main__"):
	pb0 = ProgressBar(10,60,3,[0,0,255])
	Tools.clearScreen()
	Object.show(pb0)

	Object.setY(pb0,Object.getY(pb0)+2)
	setProgression(pb0,3)
	Object.show(pb0)

	Object.setY(pb0,Object.getY(pb0)+2)
	setProgressionPercent(pb0,50)
	Object.show(pb0)

	Tools.goAt(0,51)