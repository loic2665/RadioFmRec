import pygame
from pygame.locals import *
import sys
import datetime
import os

from objects import *

pygame.init()
FPSCLOCK = pygame.time.Clock()
pygame.mixer.init()

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((480, 320))

# Chargement et collage du fond
fond = pygame.image.load("./data/img/background.png").convert()
close = pygame.image.load("./data/img/close.png").convert_alpha()
close = pygame.transform.scale(close, (36, 36))
play = pygame.image.load("./data/img/play.png").convert_alpha()
play = pygame.transform.scale(play, (36, 36))
restart = pygame.image.load("./data/img/restart.png").convert_alpha()
restart = pygame.transform.scale(restart, (32, 32))

# Chargement et collage du personnage
cursor = pygame.image.load("./data/img/mouse.gif").convert_alpha()
cursor_x = 0
cursor_y = 0

#liste de musiques
music_names = os.listdir('./data/rec')
print(music_names)

#fichier musique
liste_sons = []
for name in music_names:
	son = pygame.mixer.Sound("{}{}".format("./data/rec/", name))
	liste_sons.append(son)

playStatus = False


def message(msg, dim, pos, color): #merci a alex pour l'affichage du texte :)
	fontObj = pygame.font.Font('freesansbold.ttf', int(dim))
	textSurfaceObj = fontObj.render(msg, True, color)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.topleft = pos
	fenetre.blit(textSurfaceObj, textRectObj)
	pygame.display.update(textRectObj)


while True:

	fenetre.blit(fond, (0, 0)) # fenetre correspondant à la ou on veut l'afficher !! [image, x;y]

	closeRect = fenetre.blit(close, (435, 6))
	restartRect = fenetre.blit(restart, (390, 8))

	now = datetime.datetime.now()
	message(now.strftime("On est le %d/%m/%Y, il est %H:%M:%S"), 17, (15, 15), (255, 255, 255))



	texte_y = 70 #pixel du debut de la ligne
	texte_x = 15

	page = 1

	playButtons = []
	son_nbr = page*4
	for i in range(0+(page*4), 4+(page*4)):
		if i >= len(music_names):
			pass
		else:
			message(music_names[i][0:len(music_names[i])-4], 17, (texte_x, texte_y), (255, 255, 255))
			# playButtons.append(fenetre.blit(play, (380, texte_y-5)))
			playButton = PlayButton(liste_sons[son_nbr])
			playButton.rect = fenetre.blit(play, (380, texte_y-5))
			playButtons.append(playButton)
			# play(i)
			texte_y += 45 # ajoute x pixel d'espace
			son_nbr += 1


	# Re-collage
	# fenetre.blit(fond, (0, 0))

	# Rafraichissement
	# Tjrs dernier
	fenetre.blit(cursor, (cursor_x, cursor_y))


	#gestion des evenements toujours à la fin!

	for event in pygame.event.get():  # Attente des événements

		if event.type == QUIT:
			continuer = 0
			pygame.quit()
			exit()
		if event.type == MOUSEMOTION:
			#if event.button == 1:  # Si clic gauche
				# On change les coordonnées du perso
			cursor_x = event.pos[0]
			cursor_y = event.pos[1]
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Set the x, y postions of the mouse click
			x = event.pos[0]
			y = event.pos[1]
			if closeRect.collidepoint(x, y):
				continuer = 0
				print("EXIT")
				pygame.quit()
				exit()
			for playButton in playButtons:
				if playButton.rect.collidepoint(x, y):
					playButton.play()
					#~ if playStatus == False:
						#~ son.play()
						#~ print("PLAY MUSIC")
						#~ playStatus = True
					#~ else:
						#~ pygame.mixer.pause()
						#~ print("STOP MUSIC")
						#~ playStatus = False
			if restartRect.collidepoint(x, y):
				pygame.mixer.stop()

				print("RESTART MIXER PYGAME")
				playStatus = False

	pygame.display.update()
	FPSCLOCK.tick(60)
