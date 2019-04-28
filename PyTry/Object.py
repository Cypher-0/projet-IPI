# -*- coding: utf-8 -*-
"""
File containing definition of base type Object used almost everywhere in the project
"""
#search for tag "#PERFORMANCE" to see which lines can be commented to increase performances

import sys
import time
import Tools

attributesList = ["datas","x","y","width","height","color"]
#datas : 2D array : containing all object datas to be displayed on screen  
#x : float : object x position on screen
#y : float : object y position on screen
#width : int : object width
#height : int : object height
#color : list : list containing 3 values each ∈ [0;255] format [r,v,b]

"""
\"Object\" type attributes list
@type: list
"""

SCREEN_WIDTH = 166
"""Screen width in terms of characters used as reference in program"""
SCREEN_HEIGHT = 48
"""Screen height in terms of characters used as reference in program"""

dt = 0.03
"""dt used for all calcs"""

##########################
#
#	Constructor
#
##########################

def Object(datas,x = 0., y = 0., color = None):
	"""
	\"Object\" type constructor
	@param datas: 2D array containing object datas to display
	@type datas: list

	@param x: object x position on screen
	@type x: float

	@param y: object y position on screen
	@type y: float
	
	@param color: Object color, defined by following format : [r,g,b]. Each value have to be in [0;255] type(r,g,b) is int
	@type color: list

	@return: dictionnary containing all informations of created object
	@rtype: dict
	"""
	assert type(x) is float or type(x) is int
	assert type(y) is float or type(y) is int
	if(not(color == None)):
		assert type(color) is list and len(color) == 3, "Color is a 3 items list"
		for i in range(0,len(color)):
			assert type(color[i]) is int
			assert color[i] >= 0 and color[i] < 256,"color[%r] have to be in [0,255]" % i
	assertDatas(datas)
	#Tools.prDly(len(datas[0]),len(datas))

	return {"datas":datas,"x":float(x),"y":float(y),"width":len(datas[0]),"height":len(datas),"color":color}

##########################
#
#	Procedures
#
##########################

def assertObject(object):
	"""
	Assert object is at least corresponding to \"Object\" type criterias
	@param object: object to test
	@type object: dict
	@return: True if correct \"Object\" type. The procedure stop if it's not
	@rtype: bool
	"""
	assert type(object) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in object.keys(),"\"Object\" type expect %r key."%attributesList[i]

	return True #return true if "object" is a correct "Object"

def assertDatas(datas): #function to asser if datas is corresponding to all criterias of a 2D array destinated to be used in the program
	"""
	Assert datas is corresponding to all criterias required to be used as \"datas\" for an object
	@param datas: var to test
	@type datas: list
	@return: True if all criterias are met. The procedure stop if it's not
	@rtype: bool
	"""
	assert type(datas) is list
	height = len(datas)
	assert height > 0
	assert type(datas[0]) is list,"%r" % datas[0]
	width = len(datas[0])
	assert width > 0
	for i in range(1,height):
		assert len(datas[i]) == width,"datas have to be a rectangular 2D array. len(datas[%r]) != len(datas[0])" % i
	return True

def show(object,showSpaces = False):#showSpaces allow user to print spaces in place of don't pritn anything
	"""
	Display \"object\" on screen
	@param object: object of type \"Object\" to display
	@type object: dict
	@param showSpaces: should the procedure display sapce instead of replace them by void ?
	@type showSpaces: bool
	@return: -
	@rtype: void
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	X = object["x"]
	Y = object["y"]
	width = object["width"]
	height = object["height"]

	objectStr = ""
	#final text declaration
	if(object["color"] != None):
		objectStr = "\033[38;"+"2"+";"+str(object["color"][0])+";"+str(object["color"][1])+";"+str(object["color"][2])+"m"

	#definition of loop end
	difX = 0
	difY = 0

	if(X+width > SCREEN_WIDTH):
		difX = int(round(X))+width-SCREEN_WIDTH
	if(Y+height > SCREEN_HEIGHT):
		difY = int(round(Y))+height-SCREEN_HEIGHT

	limX = width-difX
	limY = height-difY


	#definition of loop start
	startX = 0
	startY = 0
	if(X < 0):
		startX = int(round(abs(X)))
	if(Y < 0):
		startY = int(round(abs(Y)))
	
	for i in range(startY,limY):
		for j in range(startX,limX):
			data = object["datas"][i][j]
			if(data != ''):
				if((data != ' ' and not(showSpaces))):
					objectStr += '\033['+str(i+int(round(Y))+1)+';'+str(j+int(round(X))+1)+'H'  #+1 because terminal 0 is at [1,1]
					objectStr += str(data)

	sys.stdout.write(objectStr)

	return

##########################
#
#	Getters
#
##########################

#----- Position

def getX(object): #get X position of the object on screen
	"""
	Get \"x\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object x position on screen
	@rtype: float
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["x"]

def getY(object): #get Y position of the object on screen
	"""
	Get \"y\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object y position on screen
	@rtype: float
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["y"]

def getPosition(object): #return a list containing x and y position of the object x = return[0] and y = return[1]
	"""
	Get \"x\" and \"y\" attributes value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object position on screen in following format : [x,y]
	@rtype: list
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return [object["x"],object["y"]]

#----- Size

def getWidth(object): #get Y position of the object on screen
	"""
	Get \"width\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object width in number of characters
	@rtype: int
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["width"]

def getHeight(object): #get Y position of the object on screen
	"""
	Get \"height\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object height in number of characters
	@rtype: int
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["height"]

#----- Color

def getColor(object): #get object color on screen
	"""
	Get \"color\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object color in following format : [r,g,b]. Each value is in [0;255]
	@rtype: list
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["color"] #will return None if no color defined

def getColorRed(object): #get object red color component (on screen)
	"""
	Get red component value of \"color\" attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object red color component ∈ [0;255]
	@rtype: int
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert not(object["color"] == None),"No color defined in %r" % object #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["color"][0]

def getColorGreen(object): #get object green color component (on screen)
	"""
	Get green component value of \"color\" attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object green color component ∈ [0;255]
	@rtype: int
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert not(object["color"] == None),"No color defined in %r" % object #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["color"][1]

def getColorBlue(object): #get object blue color component (on screen)
	"""
	Get blue component value of \"color\" attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object blue color component ∈ [0;255]
	@rtype: int
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert not(object["color"] == None),"No color defined in %r" % object #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["color"][2]

#----- Datas

def getDatas(object): #get object datas
	"""
	Get \"datas\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object datas (2D array containing datas to display on screen)
	@rtype: list
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object["datas"]

def getDataAt(object,x,y): #get object data at [x,y]
	"""
	Get an element value at index [x,y] in 2D array \"datas\", attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: object data at coordinates [x,y] in \"datas\" attribute of \"Object\" type
	@rtype: str
	"""
	assert type(x) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(y) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return object[y][x]

##########################
#
#	Setters
#
##########################

#----- Position

def setX(object,x): #set object X position on screen
	"""
	Set \"x\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@param x: x axis new object position on screen
	@type x: float
	@return: -
	@rtype: void
	"""
	assert type(x) is float or type(x) is int ,"%r" % x #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	object["x"] = float(x)
	Tools.prDly
	
	return

def setY(object,y): #set object Y position on screen
	"""
	Set \"y\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@return: -
	@param y: y axis new object position on screen
	@type y: float
	@rtype: void
	"""
	assert type(y) is float or type(y) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	object["y"] = float(y)
	
	return

def setPosition(object,x,y): #set object position in one function
	"""
	Set \"x\" and \"y\" attributes value of object \"object\" ([x,y] new object position on screen)
	@param object: object of type \"Object\"
	@type object: dict
	@param x: x axis new object position on screen
	@type x: float
	@param y: y axis new object position on screen
	@type y: float
	@return: object position on screen in following format : [x,y]
	@rtype: list
	"""
	assert type(x) is float or type(x) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(y) is float or type(y) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)

	object["x"] = float(x)
	object["y"] = float(y)

	return

#----- Color

def setColor(object,color): #set object color on screen
	"""
	Set \"color\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@param color: New color of the object defined by the following format : [r,g,b]. Each value have to be in [0;255]
	@type color: list
	@return: -
	@rtype: void
	"""
	assert type(color) is list #PERFORMANCE  --> comment this line to increase performances (use carefully)
	for i in range(0,3): #PERFORMANCE  --> comment this line to increase performances (use carefully)
		assert type(color[i]) is int 
		assert color[i] >= 0 and color[i] < 256,"color[%r] have to be in [0,255]" % i #assert every colors are in [0;255]
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	object["color"] = color

	return

def setColorRed(object,value): #set red color component value. If no color defined before, others components take value 255
	"""
	Set red component value of \"color\" attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@param value: object new red color component ∈ [0;255]
	@type value: int
	@return: -
	@rtype: void
	"""
	assert type(value) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert value >= 0 and value < 256,"red have to be in [0,255], current value is %r" % i  #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	if(object["color"] == None): #assert object["color"] exist
		object["color"] = [255,255,255] #other, create it in color "white" by default

	object["color"][0] = value

	return

def setColorGreen(object,value): #set green color component value. If no color defined before, others components take value 255
	"""
	Set green component value of \"color\" attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@param value: object new green color component ∈ [0;255]
	@type value: int
	@return: -
	@rtype: void
	"""
	assert type(value) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert value >= 0 and value < 256,"green have to be in [0,255], current value is %r" % i  #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	if(object["color"] == None): #assert object["color"] exist
		object["color"] = [255,255,255] #other, create it in color "white" by default

	object["color"][1] = value

	return

def setColorBlue(object,value): #set blue color component value. If no color defined before, others components take value 255
	"""
	Set blue component value of \"color\" attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@param value: object new blue color component ∈ [0;255]
	@type value: int
	@return: -
	@rtype: void
	"""
	assert type(value) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert value >= 0 and value < 256,"blue have to be in [0,255], current value is %r" % i  #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	
	if(object["color"] == None): #assert object["color"] exist
		object["color"] = [255,255,255] #other, create it in color "white" by default

	object["color"][2] = value

	return

#----- Datas

def setDatas(object,datas):
	"""
	Set \"datas\" attribute value of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@param datas: New object datas (2D array containing datas to display on screen)
	@type datas: list
	@return: -
	@rtype: void
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)

	#PERFORMANCE --> Comment this paragraph to increase performances
	assert type(datas) is list
	height = len(datas)
	assert height > 0
	assert type(datas[0]) is list
	width = len(datas[0])
	assert width > 0
	for i in range(1,height):
		assert len(datas[i]) == width,"datas have to be a rectangular 2D array. len(datas[%r]) != len(datas[0])" % i

	object["width"] = width
	object["height"] = height
	object["datas"] = datas

	return

def setDataAt(object,x,y,data):
	"""
	Set an element value at index [x,y] in 2D array \"datas\", attribute of object \"object\"
	@param object: object of type \"Object\"
	@type object: dict
	@param x: x coordinate of element to modify
	@type x: int
	@param y: y coordinate of element to modify
	@type y: int
	@param data: New object data at coordinates [x,y] in \"datas\" attribute of \"Object\" type
	@type data: str
	@return: -
	@rtype: void
	"""
	assertObject(object) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(x) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(y) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert x >= 0 and x < object["width"] #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(y) is float or type(y) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert y >= 0 and y < object["height"] #PERFORMANCE  --> comment this line to increase performances (use carefully)

	object["datas"][y][x] = data

	return



##########################
#
#	Internal tests
#
##########################

#uncomment line "ob = ..."
if(__name__ == "__main__"):

	print('GETTERS TEST\n')

	#ob = Object([[0,0,0,0,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],10,5,[21,22,23])
	print("x position : "+str(getX(ob)))
	print("y position : "+str(getY(ob)))
	print("position : "+str(getPosition(ob)))
	print("width : "+str(getWidth(ob)))
	print("height : "+str(getHeight(ob)))
	print("color : "+str(getColor(ob)))
	print("color Red = "+str(getColorRed(ob))+" | color Green = "+str(getColorGreen(ob))+" | color Blue = "+str(getColorBlue(ob)))
	print("datas : "+str(getDatas(ob)))


	print('\n\nSETTERS TEST\n')

	setDatas(ob,[[5,5,5,5,5],[5,5,8,5,5],[5,8,8,8,5],[5,5,8,5,5],[5,5,8,5,5],[8,8,8,8,8]])
	setDataAt(ob,2,0,0)
	setColor(ob,[0,0,0])
	print("color : "+str(getColor(ob)))
	setColorRed(ob,50)
	setColorGreen(ob,60)
	setColorBlue(ob,70)
	setX(ob,0)
	setY(ob,0)
	print("position : "+str(getPosition(ob)))
	setPosition(ob,100,100)
	print("position : "+str(getPosition(ob)))
	print("width : "+str(getWidth(ob)))
	print("height : "+str(getHeight(ob)))
	print("color : "+str(getColor(ob)))
	print("datas : "+str(getDatas(ob)))
