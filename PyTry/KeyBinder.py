

"""
File containing definition of type "KeyBinder" used to manage interactions between keyboard and program
"""
#used to link keyboard event and functions

import termios
import select
import tty
import sys
#import time
import copy

import Tools

attributesList = ["name","actionList"]
#name : str : name of keybinder
#actionList : list : list of actions existing in the keyBinder. This "type" is defined later in the file
"""
\"KeyBinder\" type attributes list
@type: list
"""

##########################
#
#	Constructor
#
##########################

#----- KeyBinder

def KeyBinder(name):
	"""
	\"KeyBinder\" type constructor
	@param name: Name of the KeyBinder
	@type name: str
	@return: dictionnary containing all informations of created object
	@rtype: dict
	"""
	assert type(name) is str
	return {"name":name,"actionList":[]}

#----- Action

def Action(key,function,param1 = None,param2 = None):
	"""
	\"Action\" subtype constructor
	@param key: keyboard key to link
	@type key: str
	@param function: Function to link to the key
	@type function: function
	@param param1: First parameter to pass to linked function
	@type param1: Undefined
	@param param2: Second parameter to pass to linked function
	@type param2: Undefined
	@return: dictionnary containing all informations of created subobject
	@rtype: dict
	"""
	assert type(key) is str
	esc = '\x1b' #keyCode for all keys like UP,DOWN,LEFT,RIGHT,ESC

	if(key == "ESC"):
		key = esc

	return {"key":key,"function":function,"param1":param1,"param2":param2}

##########################
#
#	Procedures
#
##########################

#----- KeyBinder

def assertKeyBinder(kb):
	"""
	Assert kb is at least corresponding to \"KeyBinder\" type criterias
	@param kb: object to test
	@type kb: dict
	@return: True if correct \"KeyBinder\" type. The procedure stop if it's not
	@rtype: bool
	"""
	assert type(kb) is dict
	for i in range(0,len(attributesList)):
		assert attributesList[i] in kb.keys(),"\"KeyBinder\" type expect %r key."%attributesList[i]

	return True #return true if "kb" is a correct "KeyBinder" object

def isData():#is keyboard data availables
	"""
	Test if keyboard data is available
	@return: True if datas availables
	@rtype: bool
	"""
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def interact(kb,clearBuffer = False): #<<main>> function to call every loop for every KeyBinder object. Keys test are in it
	"""
	MAIN function to call every loop for every KeyBinder object. It call every functions connected to every keys pressed
	@param kb: \"KeyBinder\" object
	@type kb: dict

	@param clearBuffer: Have the buffer to be cleared at the end of the function
	@type clearBuffer: bool

	@return: - 
	@rtype: void
	"""
	assertKeyBinder(kb) #PERFORMANCE  --> comment this line to increase performances (use carefully)

	if((isData() == True)):
		if(len(kb["actionList"])>0):
			c = sys.stdin.read(1)#type(c) is str
			for i in range(0,len(kb["actionList"])):
				if(c == kb["actionList"][i]["key"]):
					if(not(kb["actionList"][i]["param1"] == None)):
						if(not(kb["actionList"][i]["param2"] == None)):
							kb["actionList"][i]["function"](kb["actionList"][i]["param1"],kb["actionList"][i]["param2"])
						else:
							kb["actionList"][i]["function"](kb["actionList"][i]["param1"])
					else:
						kb["actionList"][i]["function"]()

	if(clearBuffer):
		termios.tcflush(sys.stdin.fileno(),termios.TCIFLUSH)
	
	return


def clearBuffer():
	""" 
	Clear input buffer
	@return: -
	@rtype: void
	"""

	termios.tcflush(sys.stdin.fileno(),termios.TCIFLUSH)

	return

def addAction(kb,key,function,param1 = None,param2 = None): #add an action to the actionList
	"""
	Create a new connection between a function and a key
	@param key: keyboard key to link
	@type key: str
	@param function: Function to link to the key
	@type function: function
	@param param1: First parameter to pass to linked function
	@type param1: Undefined
	@param param2: Second parameter to pass to linked function
	@type param2: Undefined
	@return: -
	@rtype: void
	"""
	assertKeyBinder(kb) #PERFORMANCE  --> comment this line to increase performances (use carefully)

	kb["actionList"].append(Action(key,function,param1,param2))

	return

##########################
#
#	Getters
#
##########################

#----- KeyBinder

def getName(kb):
	"""
	Get \"name\" attribute value of KeyBinder object \"kb\"
	@param kb: object of type \"KeyBinder\"
	@type kb: dict
	@return: keyBinder name
	@rtype: str
	"""
	assertKeyBinder(kb) #PERFORMANCE  --> comment this line to increase performances (use carefully)
	return kb["name"]

##########################
#
#	Setters
#
##########################

#----- KeyBinder

def setName(kb,name):
	"""
	Set \"name\" attribute value of KeyBinder object \"kb\"
	@param kb: object of type \"KeyBinder\"
	@type kb: dict
	@param name: New value for \"name\" attribute of \"kb\"
	@type name: str
	@return: keyBinder name
	@rtype: str
	"""
	assert type(name) is str
	assertKeyBinder(kb)
	kb["name"] = name
	return 0

#################################################################
#
#	STATIC procedures
#
#################################################################

#this function have to be called at the beginning of the program
def initKbStgs(): #return KeyBoard base Settings, to use in procedure restoreKbStgs at the end of the program
	"""
	STATIC PROCEDURE
	Initialize keyboard settings to be able to interact with user
	@return: tty default settings (used to be restored at the end of the program)
	@rtype: list
	"""
	old_settings = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin.fileno())#initiate keyboard
	return copy.deepcopy(old_settings)

#this function have to be called at the end of the program
def restoreKbStgs(old_settings): #restore KeyBoard Settings
	"""
	STATIC PROCEDURE
	Restore default keyboard settings using the result of \"initKbStgs()\"
	@param old_settings: result of \"initKbStgs()\" used at the beginning of the program. Parameters to restore.
	@type old_settings: list
	@return: -
	@rtype: void
	"""
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def waitForKeyPressed(key = None):
	"""
	STATIC PROCEDURE
	Don't do anything while a key corresponding to \"key\" is not pressed
	@param key: Is the key pressed \"key\". None <=> any key will work
	@type key: str

	@return: -
	@rtype: void
	"""
	while True:
		if(isData()):
			if(key != None):
				if(sys.stdin.read(1) == key):
					clearBuffer()
					return
			else:
				clearBuffer()
				return

	return