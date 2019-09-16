# -*- coding: utf-8 -*-

########################
#FICHIER DE TEST
# Menu.py
########################

import Object #base type importation
import Tools
import Item
import KeyBinder
import Button
import Menu

import time
import sys
import os

SCREEN_WIDTH = 166
SCREEN_HEIGHT = 48
Tools.resizeTerminal(SCREEN_WIDTH,SCREEN_HEIGHT)



def testF():
	Tools.prDly("SALUT MAGGLE",1)

	return

bouton = Button.Button("Slt",-1,7,testF)
bt2 = Button.Button("TESTV2",-1,11)
bt3 = Button.Button("Never Give Up !",-1,15)
dt = None

kb_global = KeyBinder.KeyBinder("global")

menu0 = Menu.Menu("main")

keyboard_default = None

def quit():
	global kb_global,keyboard_default

	sys.stdout.write('\033[2J')
	sys.stdout.write("\033[38;2;255;255;255m") #text white color restoration
	sys.stdout.write('\033[0m')

	KeyBinder.restoreKbStgs(keyboard_default)

	sys.exit()

	return 0

def init():
	global dt,keyboard_default,kb_global

	#dt = 0.016 #60 fps
	dt = 0.08

	keyboard_default = KeyBinder.initKbStgs()

	KeyBinder.addAction(kb_global,'ESC',quit) #ajout d'une action au KeyBinder

	Menu.addButton(menu0,bouton)
	Menu.addButton(menu0,bt2)
	Menu.addButton(menu0,bt3)

	return 0


def live():
	global ob,dt


	return 0


def show():
	global ob,SCREEN_WIDTH,SCREEN_HEIGHT

	#on clear la console et on réinitialise le curseur
	sys.stdout.write("\033[1;1H")
	sys.stdout.write("\033[2J")

	#affichage des different element
	Menu.show(menu0)

	#deplacement curseur
	sys.stdout.write("\033[0;0H\n")

	return 0


def main():
	global kb_global,keyboard_default

	init()

	i = 0 #variable d'incrémentation de test

	#70
	while(i < 2500):

		live()
		show()
		time.sleep(dt)
		Menu.interact(menu0)
		KeyBinder.interact(kb_global)

		KeyBinder.clearBuffer()

		i+=1

	quit()

	return 0

if(__name__ == "__main__"):
	tmps1 = time.time()
	
	main()

	tmps2=time.time()-tmps1
	print(tmps2)
