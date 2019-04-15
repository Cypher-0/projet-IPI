# -*- coding: utf-8 -*-

from PyTry import *
import time
import sys

dt = 0.16

kb_global = KeyBinder.KeyBinder("global")
obj = Item.Item(Tools.createDatasFromPic("Levels/l0/background.pic"),0,0,[0,255,0],-5)

keyboard_default = None

SCREEN_WIDTH = 166
SCREEN_HEIGHT = 48

def init():
	global dt,keyboard_default,kb_global

	Tools.resizeTerminal(SCREEN_WIDTH,SCREEN_HEIGHT)

	#dt = 0.016
	dt = 0.08

	keyboard_default = KeyBinder.initKbStgs()

	KeyBinder.addAction(kb_global,'ESC',quit) #ajout d'une action au KeyBinder

	return 0

def quit():
	global keyboard_default

	sys.stdout.write('\033[2J')
	sys.stdout.write("\033[38;2;255;255;255m") #text white color restoration
	sys.stdout.write('\033[0m')

	KeyBinder.restoreKbStgs(keyboard_default)

	sys.exit()

	return 

def live():
	global dt
	Item.move(obj,dt)

	return 

def show():
	global obj,SCREEN_WIDTH,SCREEN_HEIGHT

	#on clear la console et on réinitialise le curseur
	sys.stdout.write("\033[1;1H")
	sys.stdout.write("\033[2J")

	#affichage des different element
	Object.show(obj)

	#deplacement curseur
	sys.stdout.write("\033[0;0H\n")

	return 

def main():
	global kb_global,keyboard_default

	init()

	i = 0 #variable d'incrémentation de test

	#70
	while(i < 2500):

		live()
		show()
		time.sleep(dt)
		KeyBinder.interact(kb_global)

		i+=1

	quit()

	return 0

if(__name__ == "__main__"):
	tmps1 = time.time()
	
	main()

	tmps2=time.time()-tmps1
	print(tmps2)