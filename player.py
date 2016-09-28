import pygame
from pygame.locals import *
import sys
import datetime
import os

pygame.init()
FPSCLOCK = pygame.time.Clock()
pygame.mixer.init()
screen = pygame.display.set_mode((480, 320))

def add_tuples(tup1, tup2):
	ls1 = list(tup1)
	ls2 = list(tup2)
	ls = [x + y for x, y in zip(tup1, tup2)]
	tup = tuple(ls)
	return tup


class Status:
	current_song_path = ""
	played = False
	paused = True
	# To change "controls" to Status

class EmptyHContainer:
	items = []

	def __init__(self, pos=(0, 0)):
		self.content = []

		self.rect = pygame.Rect(pos, (0, 0))

		self.items.append(self)

	def append(self, obj):
		self.content.append(obj)
		obj.setPos(add_tuples(self.rect.topleft, (self.rect.width, 0)))

		self.rect.width += obj.rect.width
		if obj.rect.height > self.rect.height:
			self.rect.height = obj.rect.height
		# self.rect.size = add_tuples(self.rect.size, obj.rect.size)
		# EmptyHContainer.numbercontent += 1
		# print(EmptyHContainer.numbercontent) ## DEBUGGING


		self.rect.width += obj.rect.width
		if obj.rect.height > self.rect.height:
			self.rect.height = obj.rect.height
		# self.rect = pygame.Rect(self.pos, self.size)

	def setPos(self, pos):
		self.rect.topleft = pos

	def setsize(self, size):
		self.rect.size = size

	def blit(self, screen):
		for obj in self.content:
			obj.blit(screen)

		# self.rect = pygame.Rect(self.pos, self.size)

	def clicked(self, pos):
		for obj in self.content:
			obj.clicked(self, pos)


class SongItem(EmptyHContainer):
	# items = []

	def __init__(self, pos, song_path):
		EmptyHContainer.__init__(self, pos)
		print(self.items)
		# self.pos = pos
		self.song_path = song_path
		self.song_name = getSongName(song_path)
		print(self.song_name)

		# self.append(RewindButton)
		playBtn = PlayButton()
		self.append(playBtn)
		emptyObj = EmptyObject(size=(18, 36))
		self.append(emptyObj)
		# self.played = False
		# self.paused = True

	def play(self):
		for song_item in SongItem.items:
			song_item.reset()
			for obj in song_item.content:
				obj.reset()

		pygame.mixer.music.load(self.song_path)
		Status.current_song_path = self.song_path
		pygame.mixer.music.play()
		# self.played = True
		Status.played = True
		Status.paused = False

	def pause(self):
		pygame.mixer.music.pause()
		Status.paused = True

	def unpause(self):
		pygame.mixer.music.unpause()
		Status.paused = False

	def reset(self):
		Status.played = False
		Status.paused = True


class EmptyObject:
	def __init__(self, pos=(0, 0), size=(0, 0)):
		self.rect = pygame.Rect(pos, size)

	def clicked(self, controls, pos):
		pass

	def setPos(self, pos):
		self.rect.topleft = pos

	def setsize(self, size):
		self.rect.size = size

	def blit(self, screen):
		pass

	def reset(self):
		pass


class PlayButton(EmptyObject):
	size = (36, 36)
	playImage = pygame.image.load("./data/img/play.png").convert_alpha()
	playImage = pygame.transform.scale(playImage, size)
	pauseImage = pygame.image.load("./data/img/pauseBtn.png").convert_alpha()
	pauseImage = pygame.transform.scale(pauseImage, size)

	def __init__(self, pos=(0, 0)):
		EmptyObject.__init__(self, pos, self.size)
		self.image = self.playImage
		# self.pos = pos
		# self.rect = pygame.Rect(self.pos, self.size)

	def blit(self, screen):
		# if controls.paused == True:
		# 	self.image = self.playImage
		# else:
		# 	self.image = self.pauseImage
		screen.blit(self.image, self.rect.topleft)

	def clicked(self, controls, pos):
		if self.rect.collidepoint(pos):
			print("CLICKED ON PLAY {}".format(self.rect)) ## DEBUGGING
			if Status.played == False or controls.song_path != Status.current_song_path:
				controls.play()
				self.image = self.pauseImage
			else:
				if Status.paused == False:
					controls.pause()
					self.image = self.playImage
				else:
					controls.unpause()
					self.image = self.pauseImage

	def reset(self):
		self.image = self.playImage


class RewindButton(EmptyObject):
	size = (36, 36)
	image = pygame.image.load("./data/img/rewindBtn.png").convert_alpha()
	image = pygame.transform.scale(image, size)

	def __init__(self, pos=(0, 0)):
		EmptyObject.__init__(self, pos)

	def blit(self, screen):
		screen.blit(self.image, self.rect.topleft)

	def clicked(self, controls, pos):
		if self.rect.collidepoint(pos):
			pygame.mixer.music.rewind()



def text(screen, msg, pos, size, color=(224, 224, 224)): # merci a alex pour l'affichage du texte :) | de rien comme d'hab ;)
	fontObj = pygame.font.Font('freesansbold.ttf', int(size))
	textSurfaceObj = fontObj.render(msg, True, color)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.topleft = pos
	screen.blit(textSurfaceObj, textRectObj)
	# pygame.display.update(textRectObj)

def getSongName(song_path):
	ls = song_path.split("/")
	return ls[-1]



fond = pygame.image.load("./data/img/background.png").convert()
background = pygame.Surface(screen.get_size())
background.blit(fond, (0, 0))

close = pygame.image.load("./data/img/close.png").convert_alpha()
close = pygame.transform.scale(close, (36, 36))
restart = pygame.image.load("./data/img/restart.png").convert_alpha()
restart = pygame.transform.scale(restart, (32, 32))

music_dir = "./data/rec/"
music_names = os.listdir("./data/rec/")
musicList = []
for music_name in music_names:
	musicList.append("{}{}".format(music_dir, music_name))

content = []
# playBtn = PlayButton()
# playBtn2 = PlayButton()
song = SongItem((200, 200), musicList[0])

# song.append(RewindButton)
# song.append(EmptyObject, sizeObj=(18, 36))
# song.append(PlayButton)
# ctrls.append(PlayButton)

song2 = SongItem((150, 150), musicList[1])
# song2.append(PlayButton)

content.append(song)
content.append(song2)

print(EmptyHContainer.items)
# for item in SongItem.items:
# 	for obj in item.content:
# 		print(obj)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()

		if event.type == MOUSEMOTION:
			cursor = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			cursorPos = event.pos
			for obj in content:
				if obj.rect.collidepoint(cursorPos):
					obj.clicked(cursorPos)
					break

	screen.blit(background, (0, 0))
	song.blit(screen)
	song2.blit(screen)
	pygame.display.update()
	FPSCLOCK.tick(60)
