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
	Button.setState(menu["buttonList"][menu["lastIndex"]],0)
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

	SCREEN_WIDTH,SCREEN_HEIGHT = Tools.getTerminalSize()
	x = int((SCREEN_WIDTH/2.)-(len(menu["title"])/2.))
	Tools.goAt(x,0)
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
		for i in range(0,len(menu["buttonList"])):
			if(Button.getState(menu["buttonList"][i]) == 1):
				if(Button.getFunc(menu["buttonList"][i]) != None):
					result = Button.getFunc(menu["buttonList"][i])()
	return result


def addButton(menu,button):
	"""
	Add a button to a menu. New button is directly passed in parameters
	@param menu: object of type \"Menu\" on which the button will be added
	@type menu: dict
	@param button: Object of type \"Button\" to add to the menu
	@type button: dict
	@return: -
	@rtype: void
	"""

	assertMenu(menu)
	Button.assertButton(button)
	menu["buttonList"].append(button)

	return


##########################
#
#	STATIC Procedures
#
##########################

def printScreen(filePath,vY = None):
	"""
	STATIC PROCEDURE
	Make a text from file appear on screen. By the top if vY specified.
	@param filePath: Path to file containing informations to print on screen 
	@type filePath: str

	@return: -
	@rtype: void
	"""
	assert vY == None or type(vY) is int or float

	screenObject = Item.Item(Tools.createDatasFromPic(filePath))
	dt = Object.dt

	if(vY == None):
		Object.show(screenObject)
	else:
		assert vY > 0
		Item.setVY(screenObject,float(vY))
		Object.setY(screenObject,-Item.getBaseHeight(screenObject))
		
		while(Object.getY(screenObject) < 0):
			Tools.clearScreen()
			Item.move(screenObject,dt)
			Object.show(screenObject)
			time.sleep(dt*2)
	sys.stdout.write("\033[1;1H")

	return

##########################
#
#	Getters
#
##########################

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
	assert index >= 0 and index < len(menu["buttonList"]),"Index out of range. Tried is : %r and it have to be in [0,%r]" % (index,len(menu["buttonList"])-1)
	return menu["buttonList"][i]


##########################
#
#	internal tests
#
##########################

#if(__name__ == "__main__"):
#	Tools.sysExec("clear")
#	dfltstgs = KeyBinder.initKbStgs()
#	printScreen("screenTextTest",20)
#	KeyBinder.waitForKeyPressed()
#	KeyBinder.restoreKbStgs(dfltstgs)