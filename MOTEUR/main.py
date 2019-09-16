# -*- coding: utf-8 -*-

import Object #base type importation
import Tools
import Item
import KeyBinder
import Button

import time
import sys
import os

#max visible : 125,31
#datas = [[0,0,0,0,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]]
#ob = Item.Item(datas,135,40,[255,0,0],-26,-30,0,9.81)
datas = Tools.createDatasFromPic("pictures/image")
ob = Item.Item(datas,5,21,[255,0,0]) #center : x=78, y=21

bg1 = Object.Object(Tools.createDatasFromPic("pictures/bg0"),0,0,[128,128,128])
fg1 = Object.Object(Tools.createDatasFromPic("pictures/fg0"),0,0,[70,220,70])
enemy0 = Object.Object(Tools.createDatasFromPic("pictures/enemy0"),130,10,[242,173,12])
#hud0 = Object.Object(Tools.createDatasFromPic("pictures/hud0"),0,0,[50,112,255])


bouton = Button.Button("Slt",50,20,15,5)
dt = None

kb_global = KeyBinder.KeyBinder("global")

SCREEN_WIDTH = 166
SCREEN_HEIGHT = 48

keyboard_default = None

def DEBUG():
	global ob
	#bt = Button.Button("salut",0,0)
	Tools.prDly("HI",3)
	#Object.show(bt)
	time.sleep(3)
	return 0


def quit():
	global kb_global,keyboard_default

	sys.stdout.write('\033[2J')
	sys.stdout.write("\033[38;2;255;255;255m") #text white color restoration
	sys.stdout.write('\033[0m')

	KeyBinder.restoreKbStgs(keyboard_default)

	sys.exit()

	return 0

def init():
	global ob,dt,keyboard_default,kb_global

	Tools.resizeTerminal(SCREEN_WIDTH,SCREEN_HEIGHT)

	#dt = 0.016
	dt = 0.08

	keyboard_default = KeyBinder.initKbStgs()

	KeyBinder.addAction(kb_global,'ESC',quit) #ajout d'une action au KeyBinder
	#KeyBinder.addAction(kb_global,'d',DEBUG)
	#KeyBinder.addAction(kb_global,'g',Tools.prDly,"TEXT INCONNU",1.5)
	#KeyBinder.addAction(kb_global,'r',Tools.prDly,"TEXTE VVVVVV33333333",1)

	Tools.debug("",True)

	return 0


def live():
	global ob,dt
	Item.move(ob,dt)

	return 0


def show():
	global ob,SCREEN_WIDTH,SCREEN_HEIGHT

	#on clear la console et on réinitialise le curseur
	sys.stdout.write("\033[1;1H")
	sys.stdout.write("\033[2J")

	#affichage des different element
	Object.show(bg1)
	Object.show(fg1)
	Object.show(enemy0)
	#Object.show(hud0)
	Object.show(ob)

	#Button.show(bouton)

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
		KeyBinder.interact(kb_global)

		i+=1

	quit()

	return 0

if(__name__ == "__main__"):
	tmps1 = time.time()
	
	main()

	tmps2=time.time()-tmps1
	print(tmps2)