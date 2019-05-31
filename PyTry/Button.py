# -*- coding: utf-8 -*-
#this type inherit of Item type (Item.py) proprieties
"""
File containing definition of type \"Button\" used for things like menus
"""

import Tools
import Object
import Item

import copy
import sys

attributesList = ["datas","x","y","width","height","color","vX","vY","aX","aY","sprites","text","unselectedColor","selectedColor","state","function"]
#text : str : Button text
#state : int : button state : 0 => normal; 1 => selected
#selectedColor : list : color list (rgb) corresponding to bg color when selected (only applied on frame) or pressed (applied everywhere)
	#button background is object sprite[0]
	#button frame is object sprite[1]
	#button text is object sprite[2]
#function : function : function associated to the button


"""
\"Button\" type attributes list
@type: list
"""

##########################
#
#	Constructor
#
##########################

def Button(txt,x,y,func = None,width = None,height = None):

	"""
	\"Button\" type constructor
	@param txt: Text displayed in the button
	@type txt: str

	@param x: Button x position on screen | set to -1 to center on screen
	@type x: float

	@param y: Button y position on screen | set to -1 to center on screen
	@type y: float

	@param func: Function associated to the Button
	@type func: function
	
	@param width: Button width (num of characters) Automatically defined by text length
	@type width: int

	@param height: Button height (num of characters) Automatically defined by number of lines in "text"
	@type height: int

	@return: dictionnary containing all informations of created object
	@rtype: dict
	"""

	txt = str(txt)
	assert type(width) is int or width == None
	assert type(height) is int or height == None

	maxLen = 0
	tempList = txt.split('\n')
	#calc max text width
	for i in range(0,len(tempList)):
		if(maxLen < len(tempList[i])):
			maxLen = len(tempList[i])

	#calc width and height
	if(width == None):
		width = maxLen+8
	else :
		width = width
	if(height == None):
		height = len(tempList)+4
	else :
		height = height

	dataBackground = []
	dataFrame = []

	tempList = []
	#create empty background
	for i in range(0,height):
		tempList = []
		for j in range(0,width):
			tempList.append(" ")
		dataBackground.append(tempList)
	dataBackground = copy.deepcopy(dataBackground)

	tempList = []
	#create frame
	for i in range(0,height):
		tempList2 = []
		for j in range(0,width):
			if(i == 0 or i == height-1): #if on first line or last one
				tempList2.append('#')
			else:
				tempList2.append(' ')
		tempList2[0] = '#' #change column 0
		tempList2[width-1] = '#' #change last column
		tempList.append(tempList2)
	#replace angles
	tempList[0][0] = '#'
	tempList[0][width-1] = '#'
	tempList[height-1][width-1] = '#'
	tempList[height-1][0] = '#'

	dataFrame = copy.deepcopy(tempList)

	#test if object have to be in the center of the screen
	SCREEN_WIDTH,SCREEN_HEIGHT = Object.SCREEN_WIDTH,Object.SCREEN_HEIGHT
	if(x == -1):
		x = (SCREEN_WIDTH/2.)-(width/2.)
	if(y == -1):
		y = (SCREEN_HEIGHT/2.)-(height/2.)

	baseObject = Item.Item(dataBackground,x,y)
	Item.addSprite(baseObject,dataFrame)

	Item.addSprite(baseObject,[list(txt)])

	baseObject["text"] = txt
	baseObject["selectedColor"] = [30,220,50]
	baseObject["unselectedColor"] = [220,50,30]

	baseObject["state"] = 0
	baseObject["function"] = func

	return baseObject

##########################
#
#	Procedures
#	
##########################

def assertButton(button):
	"""
	Assert button is at least corresponding to \"Button\" type criterias
	@param button: object to test
	@type button: dict
	@return: True if correct \"Button\" type. The procedure stop if it's not
	@rtype: bool
	"""
	assert type(button) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in button.keys(),"\"Button\" type expect %r key."%attributesList[i]

	return True #return true if "object" is a correct "Button"

def show(button):
	"""
	Show button \"button\" on terminal screen
	@param button: Dictionnary containing all information about one Button object
	@type button: dict
	@return: -
	@rtype: void
	"""
	Object.show(button,True)#print background

	Item.setSprite(button,1)#select frame sprite
	tempStr = ""

	textColor = [0,0,0]
	
	if(button["state"] == 1): #if button selected
		tempStr+=('\033[5m')
		
		tempStr+=('\033[48;2;'+str(button["selectedColor"][0])+';'+str(button["selectedColor"][1])+';'+str(button["selectedColor"][2])+'m')
		
		textColor[0] = button["selectedColor"][0]-70 if(button["selectedColor"][0]-70 >= 0) else 0
		textColor[1] = button["selectedColor"][1]-70 if(button["selectedColor"][1]-70 >= 0) else 0
		textColor[2] = button["selectedColor"][2]-70 if(button["selectedColor"][2]-70 >= 0) else 0

		tempStr+=('\033[38;2;'+str(textColor[0])+';'+str(textColor[1])+';'+str(textColor[2])+'m')

		sys.stdout.write(tempStr)

	elif(button["state"] == 0): #if button selected
		
		tempStr+=('\033[48;2;'+str(button["unselectedColor"][0])+';'+str(button["unselectedColor"][1])+';'+str(button["unselectedColor"][2])+'m')
		
		textColor[0] = button["unselectedColor"][0]-70 if(button["unselectedColor"][0]-70 >= 0) else 0
		textColor[1] = button["unselectedColor"][1]-70 if(button["unselectedColor"][1]-70 >= 0) else 0
		textColor[2] = button["unselectedColor"][2]-70 if(button["unselectedColor"][2]-70 >= 0) else 0

		tempStr+=('\033[38;2;'+str(textColor[0])+';'+str(textColor[1])+';'+str(textColor[2])+'m')

		sys.stdout.write(tempStr)


	Object.show(button)#print selected sprite
	sys.stdout.write('\033[0m') #reset color parameters

	X = Object.getX(button)
	Y = Object.getY(button)
	Item.setSprite(button,2)#select text sprite
	Object.setX(button,X+(Item.getBaseWidth(button)/2.)-(len(button["text"])/2.))
	Object.setY(button,Y+int(Item.getBaseHeight(button)/2))
	Object.show(button)
	Object.setX(button,X)
	Object.setY(button,Y)

	Item.setSprite(button,0) #change item sprite to background

	sys.stdout.write('\033[0m') #reset color parameters

	button["state"] = 0

	return

##########################
#
#	Getters
#
##########################

def getState(button):
	"""
	Get button \"state\" attribute value : 0-Unselected | 1-Selected
	@param button: object of type \"Button\"
	@type button: dict
	@return: \"button\" state
	@rtype: int
	"""
	assertButton(button)

	return button["state"]

def getFunc(button):
	"""
	Get button \"function\" attribute value : function to call on button activated
	@param button: object of type \"Button\"
	@type button: dict
	@return: \"button\" linked function
	@rtype: function
	"""
	assertButton(button)
	return button["function"]

##########################
#
#	Setters
#
##########################

def setState(button,state):
	"""
	Set button \"state\" attribute value : 0-Unselected | 1-Selected
	@param button: object of type \"Button\"
	@type button: dict
	@param state: new \"state\" attribute value of \"button\"
	@type state: int
	@return: -
	@rtype: void
	"""
	assertButton(button)

	button["state"] = state
	return

def setSelectedColor(button,color):
	"""
	Set \"selectedColor\" attribute value of button \"button\"
	@param button: object of type \"Button\"
	@type button: dict
	@param color: New color of the selected button's frame defined by the following format : [r,g,b]. Each value have to be in [0;255]
	@type color: list
	@return: -
	@rtype: void
	"""
	assert type(color) is list #PERFORMANCE  --> comment this line to increase performances (use carefully)
	for i in range(0,3): #PERFORMANCE  --> comment this line to increase performances (use carefully)
		assert type(color[i]) is int 
		assert color[i] >= 0 and color[i] < 256,"color[%r] have to be in [0,255]" % i #assert every colors are in [0;255]
	assertButton(button) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	button["selectedColor"] = color

	return

def setUnselectedColor(button,color):
	"""
	Set \"unselectedColor\" attribute value of button \"button\"
	@param button: object of type \"Button\"
	@type button: dict
	@param color: New color of the selected button's frame defined by the following format : [r,g,b]. Each value have to be in [0;255]
	@type color: list
	@return: -
	@rtype: void
	"""
	assert type(color) is list #PERFORMANCE  --> comment this line to increase performances (use carefully)
	for i in range(0,3): #PERFORMANCE  --> comment this line to increase performances (use carefully)
		assert type(color[i]) is int 
		assert color[i] >= 0 and color[i] < 256,"color[%r] have to be in [0,255]" % i #assert every colors are in [0;255]
	assertButton(button) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	button["unselectedColor"] = color

	return