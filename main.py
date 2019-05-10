# -*- coding: utf-8 -*-

from PyTry import *
import Level

import time
import sys
import subprocess

dt = None

saveName = "1"

kb_global = KeyBinder.KeyBinder("global")
obj = Item.Item(Tools.createDatasFromPic("Levels/l0/background.pic"),0,0,[0,255,0],-5)
prov = Level.Level("Levels/l0",saveName)

keyboard_default = None

SCREEN_WIDTH = 166
SCREEN_HEIGHT = 48

def init():
	global dt,keyboard_default,kb_global

	#Tools.resizeTerminal(SCREEN_WIDTH,SCREEN_HEIGHT)
	Tools.sysExec("python2.7 initTerm.py")

	dt = 0.06
	#dt = 0.09

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
	Level.interact(prov)
	KeyBinder.interact(kb_global)

	return 

def show():
	global SCREEN_WIDTH,SCREEN_HEIGHT

	#on clear la console et on réinitialise le curseur
	sys.stdout.write("\033[1;1H")
	sys.stdout.write("\033[2J")

	#affichage des different element
	#Object.show(obj)
	Level.show(prov)

	#deplacement curseur
	sys.stdout.write("\033[0;0H\n")

	return 

def main():
	global kb_global,keyboard_default

	init()

	i = 0 #variable d'incrémentation de test

	lastTime = 0

	#70
	while(i < 25000):

		live()
		if(time.time()-lastTime > dt):
			show()
			lastTime = time.time()
			#Tools.prDly("SALUT")
		KeyBinder.clearBuffer()
		time.sleep(Level.dt)
		

		i+=1

	quit()

	return 0

if(__name__ == "__main__"):
	tmps1 = time.time()
	
	main()

	tmps2=time.time()-tmps1
	print(tmps2)