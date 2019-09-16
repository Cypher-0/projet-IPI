# -*- coding: utf-8 -*-

########################
#FICHIER DE TEST
# ProgressBar.py
########################

import Object #base type importation
import Tools
import Item
import KeyBinder
import Button
import Menu
import ProgressBar

import time
import sys
import os

SCREEN_WIDTH = 166
SCREEN_HEIGHT = 48
Tools.resizeTerminal(SCREEN_WIDTH,SCREEN_HEIGHT)

dt = None

kb_global = KeyBinder.KeyBinder("global")

keyboard_default = None

pb0 = ProgressBar.ProgressBar(10,60,3,[0,0,255])

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

	return 0


def live():
	global ob,dt


	return 0


def show():
	global pb0,SCREEN_WIDTH,SCREEN_HEIGHT

	#on clear la console et on réinitialise le curseur
	sys.stdout.write("\033[1;1H")
	sys.stdout.write("\033[2J")

	#affichage des different element
	Object.show(pb0)


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
		KeyBinder.interact(kb_global)

		KeyBinder.clearBuffer()

		i+=1
		time.sleep(dt)

	quit()

	return 0

if(__name__ == "__main__"):
	tmps1 = time.time()
	
	main()

	tmps2=time.time()-tmps1
	print(tmps2)
