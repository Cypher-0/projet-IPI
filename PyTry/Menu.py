# -*- coding: utf-8 -*-

"""
File containing definition of type \"Menu\" used to defined menus containing only buttons
And statics procedures used to print pass screen
"""
import Button
import KeyBinder
import Item
import Object

import sys
import Tools
import time

attributesList = ["title","keyBinder","buttonList","currentIndex","lastIndex"]
#title : str : this string will be displayed at the top of the screen as a "title" for the menu
#keyBinder : KeyBinder : to manage keyboard interactions
#buttonList : list : list of buttons actives on screen
#currentIndex : int : index of selected button
#lastIndex : int : index of last selected button
"""
\"Menu\" type attributes list
@type: list
"""



##########################
#
#	Constructor
#
##########################

def Menu(title):
	"""
	\"Menu\" type constructor
	@param title: menu title (printed on top)
	@type title: str
	@return: new menu object of type \"Menu\"
	@rtype: dict
	"""

	assert type(title) is str

	kb = KeyBinder.KeyBinder("menuDefault")
	obj = {"title":title,"keyBinder":kb,"buttonList":[],"currentIndex":0,"lastIndex":0}
	KeyBinder.addAction(kb,'z',upIndex,obj)
	KeyBinder.addAction(kb,'s',downIndex,obj)
	KeyBinder.addAction(kb,'\n',onEnter,obj)

	return obj


##########################
#
#	Procedures
#
##########################

def assertMenu(menu):
	"""
	Assert menu is at least corresponding to \"Menu\" type criterias
	@param menu: object to test
	@type menu: dict
	@return: True if correct \"Menu\" type. The procedure stop if it's not
	@rtype: bool
	"""
	assert type(menu) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in menu.keys(),"\"Button\" type expect %r key."%attributesList[i]

	return True #return true if "object" is a correct "Button"

def interact(menu): #main function which is managing keyboard events for the menu
	"""
	MAIN function to call before show(). It manage interactions between keyboard and menu
	@param menu: object of type \"Menu\"
	@type menu: dict
	@return: -
	@rtype: void
	"""
	assertMenu(menu)
	#set buttons state
	if(len(menu["buttonList"]) > 0):
		if(menu["lastIndex"] in range(0,len(menu["buttonList"]))):
			Button.setState(menu["buttonList"][menu["lastIndex"]],0)
		if(menu["currentIndex"] in range(0,len(menu["buttonList"]))):
			Button.setState(menu["buttonList"][menu["currentIndex"]],1)

	KeyBinder.interact(menu["keyBinder"])

	return

def show(menu):
	"""
	Display the menu on screen
	@param menu: object of type \"Menu\"
	@type menu: dict

	@return: -
	@rtype: void
	"""
	#display every buttons

	SCREEN_WIDTH,SCREEN_HEIGHT = Object.SCREEN_WIDTH,Object.SCREEN_HEIGHT
	x = int(round((SCREEN_WIDTH/2.)-(len(menu["title"])/2.)))
	Tools.goAt(x+1,0)
	sys.stdout.write('\033[53;4;1m\033[38;2;200;0;0m'+menu["title"]+'\033[0m')
	#53:overlined
	#4:Underline
	#1:Bold
	#7:reverse color

	for i in range(0,len(menu["buttonList"])):
		Button.show(menu["buttonList"][i])

	return

def upIndex(menu):
	"""
	Function called when up key is pressed on \"Menu\" menu
	@param menu: object of type \"Menu\"
	@type menu: dict
	@return: -
	@rtype: void
	"""

	assertMenu(menu)
	if(menu["buttonList"] != None):
		if(len(menu["buttonList"]) > 0):
			menu["lastIndex"] = menu["currentIndex"]
			menu["currentIndex"] -= 1
			menu["currentIndex"] %= len(menu["buttonList"])

	return

def downIndex(menu):
	"""
	Function called when down key is pressed on \"Menu\" menu
	@param menu: object of type \"Menu\"
	@type menu: dict
	@return: -
	@rtype: void
	"""

	assertMenu(menu)
	if(menu["buttonList"] != None):
		if(len(menu["buttonList"]) > 0):
			menu["lastIndex"] = menu["currentIndex"]
			menu["currentIndex"] += 1
			menu["currentIndex"] %= len(menu["buttonList"])

	return


def onEnter(menu):
	"""
	Function called when ENTER is pressed to activate 
	@param menu: object of type \"Menu\" to test when ENTER is pressed
	@type menu: dict
	@return: return of selected button linked function
	@rtype: unknown
	"""
	result = None
	if(menu["buttonList"] != None):
		if(len(menu["buttonList"]) > 0 ):
			for i in menu["buttonList"]:
				if(Button.getState(i) == 1):
					if(Button.getFunc(i) != None):
						result = Button.getFunc(i)()
	return result


def addButton(menu,button,index = None):
	"""
	Add a button to a menu. New button is directly passed in parameters
	@param menu: object of type \"Menu\" on which the button will be added
	@type menu: dict
	@param button: Object of type \"Button\" to add to the menu
	@type button: dict
	@param index: insert button at \"index\" in buttonList
	@type index: int
	@return: -
	@rtype: void
	"""

	assertMenu(menu)
	Button.assertButton(button)
	assert index == None or type (index) is int

	if(index == None):
		menu["buttonList"].append(button)
	else:
		menu["buttonList"].insert(index,button)


	return

def removeButton(menu,button):
	"""
	Remove a button from a menu

	@param menu: object of type \"Menu\" on which the button will be removed
	@type menu: dict
	
	@param button: Button to remove. If type is str, \"button\" correspond to button's text to remove. If it's int, it's corresponding to the index.
	@type button: str or int

	@return: -
	@rtype: void
	"""

	assertMenu(menu)
	assert type(button) is str or int

	if(type(button) is int):
		assert button >= 0 and button < len(menu["buttonList"]),"Index out of range,try is %r and have to be in [0;%r]" % (button,len(menu["buttonList"]))
		menu["buttonList"].pop(button)
		
	elif(type(button) is str):
		for i in menu["buttonList"]:
			if(Button.getText(i) == button):
				menu["buttonList"].remove(i)

	return

def removeAllButtons(menu):
	"""
	Remove all buttons from a menu

	@param menu: object of type \"Menu\" on which all buttons will be removed
	@type menu: dict

	@return: -
	@rtype: void
	"""

	assertMenu(menu)
	for i in range(0,len(menu["buttonList"])):
		menu["buttonList"].pop()

	return

##########################
#
#	Getters
#
##########################

def getSelectedIndex(menu):
	"""
	Get the index of selected button of the menu	
	@param menu: Object of type \"Menu\"
	@type menu: dict

	@return: index of selected button of the menu
	@rtype: int
	"""
	assertMenu(menu)

	return menu["currentIndex"]

def getButtonAt(menu,index):
	"""
	Get contained button at index \"index\" in \"buttonList\" attribute of object \"menu\" of type \"Menu\"	
	@param menu: Object of type \"Menu\"
	@type menu: dict

	@param index: Index of reached button
	@type index: int

	@return: object of type \"Button\" contained at index \"index\" in \"buttonList\" attribute of type \"Menu\"
	@rtype: dict
	"""
	assertMenu(menu)
	assert type(index) is int
	if(len(menu["buttonList"]) != 0):
		assert index >= 0 and index < len(menu["buttonList"]),"Index out of range. Tried is : %r and it have to be in [0,%r]" % (index,len(menu["buttonList"])-1)
	return menu["buttonList"][index]

def getKeyBinder(menu):
	"""
	Return \"keyBinder\" key value of the dict menu (type : \"Menu\")
	@param menu: Dictionnary containing all information about one Menu object
	@type menu: dict

	@return: \"keyBinder\" type object of the level under the form of a dict
	@rtype: dict
	"""
	assertMenu(menu)

	return menu["keyBinder"]



##########################
#
#	Setters
#
##########################

def setSelectedIndex(menu,index):
	"""
	Set current selected index of the menu to \"index\"
	@param menu: Object of type \"Menu\"
	@type menu: dict

	@param index: new selected  button index
	@type index: int

	@return: void
	@rtype: void
	"""
	assertMenu(menu)
	assert type(index) is int
	assert index >= 0 and index < len(menu["buttonList"]),"Index out of range. Tried is : %r and it have to be in [0,%r]" % (index,len(menu["buttonList"])-1)
	menu["currentIndex"] = index
	menu["lastIndex"] = index



##########################
#
#	STATIC Procedures
#
##########################

def printScreen(filePath,vY = None,prePrintOption = ""):
	"""
	STATIC PROCEDURE
	Make a text from file appear on screen. By the top if vY specified.
	@param filePath: Path to file containing informations to print on screen 
	@type filePath: str

	@param vY: Texte descent speed. Use None or 0 to instant appearance
	@type vY: float

	@param prePrintOption: This text will be printed on terminal before the text extract of the file. Use to set proprieties by ANSI code.
	@type prePrintOption: str

	@return: -
	@rtype: void
	"""
	assert vY == None or type(vY) is int or float
	assert type(prePrintOption) is str

	screenObject = Item.Item(Tools.createDatasFromPic(filePath,True))
	dt = Object.dt
	if(prePrintOption != ""):
		sys.stdout.write("\033[1;1H"+prePrintOption)

	if(vY == None or vY == 0):
		Object.show(screenObject)
		print("")
	else:
		assert vY > 0
		Item.setVY(screenObject,float(vY))
		Object.setY(screenObject,-Item.getBaseHeight(screenObject))
		
		while(Object.getY(screenObject) < 0):
			Tools.clearScreen()
			Item.move(screenObject,dt)
			Object.show(screenObject)
			print("")
			time.sleep(dt*2)
		Tools.clearScreen()
		Object.setPosition(screenObject,0,0)
		Object.show(screenObject)
		print("")
	sys.stdout.write("\033[1;1H")

	return

def printText(text):
	"""
	Print text in a frame in the middle of the screen
	@param text: Text to print. Have to be on one line
	@type text: str

	@return: -
	@rtype: void
	"""

	maxLen = 0
	tempList = text.split('\n')
	#calc max text width
	for i in range(0,len(tempList)):
		if(maxLen < len(tempList[i])):
			maxLen = len(tempList[i])

	width = None
	height = None

	dH = 4
	dV = 4

	#calc width and height
	if(width == None):
		width = maxLen+dH
	else :
		width = width
	if(height == None):
		height = len(tempList)+dV
	else :
		height = height

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
	frame = Item.Item(tempList,int(round((Object.SCREEN_WIDTH/2.)-(width/2.))),int(round((Object.SCREEN_HEIGHT/2.)-(height/2.))))
	Object.show(frame)
	
	sys.stdout.write("\033["+str(int(round((Object.SCREEN_HEIGHT/2.)-(height/2.)+(dV/2.)+1)))+";"+str(int(round((Object.SCREEN_WIDTH/2.)-(width/2.)+(dH/2)+1)))+"H"+text)

	print("")

	return

##########################
#
#	internal tests
#
##########################

#if(__name__ == "__main__"):
#	Tools.sysExec("clear")
#	dfltstgs = KeyBinder.initKbStgs()
	#screenObject = Item.Item(Tools.createDatasFromPic("player.pic",True))
#	printText("COUCOU\nComment ça va ?")
#	KeyBinder.waitForKeyPressed()
#	KeyBinder.restoreKbStgs(dfltstgs)