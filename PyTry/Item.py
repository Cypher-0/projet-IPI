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

def tryCollide(item1,item2,coordinatesCheckOnly = False):
	"""
	Is 2 items colliding ?
	@param item1: Object of type "Item"
	@type item1: dict

	@param item2: Object of type "Item"
	@type item2: dict

	@param coordinatesCheckOnly: Should we only analyse coordinates ? (faster but less precise)
	@type coordinatesCheckOnly: bool

	@return: Are item1 and item2 colliding ? Yes:True   No:False
	@rtype: bool
	"""

	#assertItem(item1)
	#assertItem(item2)

	width1 = Object.getWidth(item1)
	height1 = Object.getHeight(item1)
	x1 = Object.getX(item1)
	y1 = Object.getY(item1)

	width2 = Object.getWidth(item2)
	height2 = Object.getHeight(item2)
	x2 = Object.getX(item2)
	y2 = Object.getY(item2)

	"""tempList = [item1,item2]

	x1,y1 = int(round(Object.getX(item1))),int(round(Object.getY(item1)))
	x2,y2 = int(round(Object.getX(item2))),int(round(Object.getY(item2)))

	smallerIndex = 0 if width1*height1 < width2*height2 else 1 #search which item is the smaller """

	startX1,startX2,startY1,startY2 = 0,0,0,0
	endX1,endX2,endY1,endY2 = 0,0,0,0
	forWidth,forHeight = 0,0

	if((x1+width1 < x2) or (x2+width2 < x1)): #if objects are not colliding on xS
		return False

	#x tests
	#Tools.prDly("TESTS on X :")
	if(x2 <= x1 and x2+width2 <= x1+width1): #if object potentially collide on x  #CASE 1
		startX1=0;startX2=int(round(x1-x2))
		endX2=width2-1;endX1=width2-startX2-1
		forWidth = endX2-startX2
		#Tools.prDly("Cas 1 :\n"+str(startX1)+";"+str(endX1)+"\n"+str(startX2)+";"+str(endX2))
	elif(x2 <= x1 and x2+width2 >= x1+width1): #CASE 2
		startX1=0;startX2=int(round(x1-x2))
		endX1=width1-1;endX2=startX2+width1-1
		forWidth = width1-1
		#Tools.prDly("Cas 2 :\n"+str(startX1)+";"+str(endX1)+"\n"+str(startX2)+";"+str(endX2))
	elif(x2 >= x1 and x2+width2 >= x1+width1): #CASE 3
		startX1=int(round(x2-x1));startX2=0
		endX1=width1-1;endX2=width1-startX1-1
		forWidth = endX1-startX1
		#Tools.prDly("Cas 3 :\n"+str(startX1)+";"+str(endX1)+"\n"+str(startX2)+";"+str(endX2))
	elif(x2 >= x1 and x2+width2 <= x1+width1): #CASE 4
		startX2 = 0;endX2 = width2-1
		startX1 = int(round(x2-x1));endX1 = startX1+width2-1
		forWidth = width2-1
		#Tools.prDly("Cas 4 :\n"+str(startX1)+";"+str(endX1)+"\n"+str(startX2)+";"+str(endX2))
	else:
		return False


	#y tests
	#Tools.prDly("TESTS on Y :")
	if(y2 <= y1 and y2+height2 <= y1+height1): #if object potentially collide on x   #CASE 1
		startY1=0;startY2=int(round(y1-y2))
		endY2=height2-1;endY1=height2-startY2-1
		forHeight = endY2-startY2
		#Tools.prDly("Cas 1 :\n"+str(startY1)+";"+str(endY1)+"\n"+str(startY2)+";"+str(endY2))
	elif(y2 <= y1 and y2+height2 >= y1+height1): #CASE 2
		startY1=0;startY2=int(round(y1-y2))
		endY1=height1-1;endY2=startY2+height1-1
		forHeight = height1-1
		#Tools.prDly("Cas 2 :\n"+str(startY1)+";"+str(endY1)+"\n"+str(startY2)+";"+str(endY2))
	elif(y2 >= y1 and y2+height2 >= y1+height1): #CASE 3
		startY1=int(round(y2-y1));startY2=0
		endY1=height1-1;endY2=height1-startY1-1
		forHeight = endY1-startY1
		#Tools.prDly("Cas 3 :\n"+str(startY1)+";"+str(endY1)+"\n"+str(startY2)+";"+str(endY2))
	elif(y2 >= y1 and y2+height2 <= y1+height1): #CASE 4
		startY2 = 0;endY2 = height2-1
		startY1 = int(round(y2-y1));endY1 = startY1+height2-1
		forHeight = height2-1
		#Tools.prDly("Cas 4 :\n"+str(startY1)+";"+str(endY1)+"\n"+str(startY2)+";"+str(endY2))
	else:
		return False

	forWidth += 1 #correct the transition from coordinates to value
	forHeight += 1 #correct the transition from coordinates to value
	#Tools.prDly("\n\n"+str(forWidth)+";"+str(forHeight))

	if(forWidth != 0 and forHeight != 0):
		if(coordinatesCheckOnly):
			#Tools.prDly("CHECK COO ONLY")
			return True
		else:
			for i in range(0,forWidth):
				for j in range(0,forHeight):
					data1 = Object.getDataAt(item1,i+startX1,j+startY1)
					data2 = Object.getDataAt(item2,i+startX2,j+startY2)
					if(data1 != '' and data1 != ' ' and data2 != '' and data2 != ' '):
						return True

	return False


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

	#it = Item([[0,1,2,3,4,5],[1,0,0,0,0,1],[2,0,0,0,0,2],[3,0,0,0,0,3],[4,0,0,0,0,4],[5,0,0,0,0,5]],28,5,[255,255,255])
	#it = Item([[0,1,2,3,4,5]],28,5,[255,255,255])
	#it = Item([[0,'','','','',''],[1,0,'','','',''],[2,0,0,'2','',''],[3,0,0,0,'2',''],[4,0,0,0,0,'2'],[5,0,0,0,0,5]],28,5,[255,255,255])

	#it2 = Item([[0,1,2,3,4,5,6,7,8],[1,0,0,0,0,0,0,0,1],[2,0,0,0,0,0,0,0,2],[3,0,0,0,0,0,0,0,3]],29,4,[0,255,0])
	#it2 = Item([[0,1,2],[1,0,0]],30,8,[0,255,0])
	#it2 = Item([[0,1,2,3,4,5,6,7,8],['',0,0,0,0,0,0,0,1],['','',0,0,0,0,0,0,2],['','','',0,0,0,0,0,3]],28,4,[0,255,0])

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

	Tools.sysExec("clear")

	Object.show(it)
	Object.show(it2)
	Tools.goAt(1,1)
	print(tryCollide(it,it2))