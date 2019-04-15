# -*- coding: utf-8 -*-

#file containing definition of "Item" type : base for all object which will move

#search for tag "#PERFORMANCE" to see which lines can be commented to increase performances

import Object #importation of base type
import Tools

import sys
import time


attributesList = ["datas","x","y","width","height","color","vX","vY","aX","aY","sprites"]
#datas,x,y,width,height,color : see Object.py
#vX : float : item x speed
#vY : float : item y speed
#aX : float : item x acceleration
#aY : float : item y acceleration
#sprites : list : list of 2D arrays to replace "datas" and print differents appearances function of state

##########################
#
#	Constructor
#
##########################

def Item(datas,x = 0, y = 0, color = None,vX=0,vY=0,aX=0,aY=0):
	assert type(vX) is float or type(vX) is int
	assert type(vY) is float or type(vY) is int
	assert type(aX) is float or type(aX) is int
	assert type(aY) is float or type(aY) is int

	base = Object.Object(datas,x,y,color)
	base["sprites"] = [datas] #sprites[0] will always be base data
	base["vX"] = float(vX)
	base["vY"] = float(vY)
	base["aX"] = float(aX)
	base["aY"] = float(aY)

	return base

##########################
#
#	Procedures
#
##########################

def assertItem(item):
	assert type(item) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in item.keys(),"\"Item\" type expect %r key."%attributesList[i]

	return True #return true if "item" is a correct "Item"

def move(item,dt): #procedure to define new position of the item
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)

	x = Object.getX(item) #get item X position
	y = Object.getY(item) #get item Y position

	#change item speed
	item["vX"] += dt*item["aX"]
	item["vY"] += dt*item["aY"]

	x+=dt*item["vX"] #set possible future object position
	y+=dt*item["vY"]

	Object.setX(item,x)#x changes
	Object.setY(item,y)#y changes


##########################
#
#	Getters
#
##########################

#----- Speed

def getVX(item): #get item x speed
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return item["vX"]

def getVY(item): #get item y speed
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return item["vY"]

#----- Acceleration

def getAX(item): #get item x acceleration
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return item["aX"]

def getAY(item): #get item y acceleration
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return item["aY"]

#----- Sprites

def getSprites(item): #get item list of sprites
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return item["sprites"]

def getSpritesCount(item):
	"""
	Get \"item\" number of sprites
	@param item: object of type \"Item\"
	@type item: dict

	@return: \"item\" number of sprites
	@rtype: int
	"""
	assertItem(item)

	return len(item["sprites"])

def getSpriteAt(item,index): #get item sprite at index "index" in ["sprites"] list attribute
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(index) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert index >=0 and index < len(item["sprites"]),"Index out of range. It have to be in [0;%r] and current try is : %r" % (len(item["sprites"]),index)
		   #PERFORMANCE  --> comment this line (upper) to increase performances (use carefully)
	return item["sprites"][index]

#----- Size

def getBaseWidth(item):
	"""
	@param item: Dictionnary containing all information about one Item object
	@type item: dict
	@return: Return width of sprite[0] <=> width of base datas
	@rtype: int
	"""

	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return len(item["sprites"][0][0])

def getBaseHeight(item):
	"""
	@param item: Dictionnary containing all information about one Item object
	@type item: dict
	@return: Return height of sprite[0] <=> height of base datas
	@rtype: int
	"""

	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return len(item["sprites"][0])


##########################
#
#	Setters
#
##########################

#----- Speed

def setVX(item,vX): #set item x speed
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(vX) is int or type(vX) is float #PERFORMANCE  --> comment this line to increase performances (use carefully)
	item["vX"] = float(vX)
	return 0

def setVY(item,vY): #set item y speed
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(vY) is int or type(vY) is float #PERFORMANCE  --> comment this line to increase performances (use carefully)
	item["vY"] = float(vY)
	return 0

#----- Acceleration

def setAX(item,aX): #set item x acceleration
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(aX) is int or type(aX) is float #PERFORMANCE  --> comment this line to increase performances (use carefully)
	item["aX"] = float(aX)
	return 0

def setAY(item,aY): #set item y acceleration
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(aY) is int or type(aY) is float #PERFORMANCE  --> comment this line to increase performances (use carefully)
	item["aY"] = float(aY)
	return 0

#----- Sprites

def addSprite(item,sprite): #add a sprite at the end of the sprite list
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	Object.assertDatas(sprite) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	item["sprites"].append(sprite) #add sprite at the list
	return 0

def removeSprite(item,index): #remove sprite designated in the list by index "index"
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(index) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert index >=0 and index < len(item["sprites"]),"Index out of range. It have to be in [0;%r] and current try is : %r" % (len(item["sprites"]),index)
		   #PERFORMANCE  --> comment this line (upper) to increase performances (use carefully)
	del item["sprites"][index]
	return 0

def setSprite(item,index): #set which sprite to be displayed on screen
	assertItem(item) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert type(index) is int #PERFORMANCE  --> comment this line to increase performances (use carefully)
	assert index >=0 and index < len(item["sprites"]),"Index out of range. It have to be in [0;%r] and current try is : %r" % (len(item["sprites"]),index)
		   #PERFORMANCE  --> comment this line (upper) to increase performances (use carefully)
	Object.setDatas(item,item["sprites"][index])
	return 0





##########################
#
#	internal tests
#
##########################

if(__name__ == "__main__"):

	it = Item([[0,0,0,0,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],10,5,[21,22,23],1.1,1,0.1,0.2)
	print("Is it a correct Item type ? : "+str(assertItem(it)))
	print("x speed : "+str(getVX(it)))
	print("y speed : "+str(getVY(it)))
	print("x acceleration : "+str(getAX(it)))
	print("y acceleration : "+str(getAY(it)))
	print("Sprite 0 = "+str(getSpriteAt(it,0))) #display base data
	move(it,0.08)
	print("")
	print("")
	print("x speed : "+str(getVX(it)))
	print("y speed : "+str(getVY(it)))
	print("x acceleration : "+str(getAX(it)))
	print("y acceleration : "+str(getAY(it)))
	print("Sprite 0 = "+str(getSpriteAt(it,0))) #display base data