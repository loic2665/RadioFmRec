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

def getSongName(song_path):
	ls = song_path.split("/")
	return ls[-1]


class Status:
	current_song_path = ""
	played = False
	paused = True


class EmptyHContainer:
	items = []

	def __init__(self, pos=(0, 0)):
		self.content = []

		self.rect = pygame.Rect(pos, (0, 0))

		self.items.append(self)

	def append(self, obj):
		self.content.append(obj)
		obj.setPos(self.rect.topright)

		self.rect.width += obj.rect.width
		if obj.rect.height > self.rect.height:
			self.rect.height = obj.rect.height
		# self.rect.size = add_tuples(self.rect.size, obj.rect.size)
		# EmptyHContainer.numbercontent += 1
		# print(EmptyHContainer.numbercontent) ## DEBUGGING
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
			if obj.rect.collidepoint(pos):
				obj.clicked(pos)
				break


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
		playBtn = PlayButton(self)
		self.append(playBtn)
		emptyObj = EmptyObject(size=(18, 36))
		self.append(emptyObj)
		textObj = Label(self.song_name, 18)
		self.append(textObj)
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

	def clicked(self, pos):
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

	def __init__(self, parent, pos=(0, 0)):
		EmptyObject.__init__(self, pos, self.size)
		self.parent = parent
		self.image = self.playImage

		# self.pos = pos
		# self.rect = pygame.Rect(self.pos, self.size)

	def blit(self, screen):
		screen.blit(self.image, self.rect.topleft)

	def clicked(self, pos):
		print("CLICKED ON PLAY {}".format(self.rect)) ## DEBUGGING
		if Status.played == False or self.parent.song_path != Status.current_song_path:
			self.parent.play()
			self.image = self.pauseImage
		else:
			if Status.paused == False:
				self.parent.pause()
				self.image = self.playImage
			else:
				self.parent.unpause()
				self.image = self.pauseImage

	def reset(self):
		self.image = self.playImage


class RewindButton(EmptyObject):
	size = (36, 36)
	image = pygame.image.load("./data/img/rewindBtn.png").convert_alpha()
	image = pygame.transform.scale(image, size)

	def __init__(self, pos=(0, 0)):
		EmptyObject.__init__(self, pos, self.size)

	def blit(self, screen):
		screen.blit(self.image, self.rect.topleft)

	def clicked(self, pos):
		pygame.mixer.music.rewind()


class Label(EmptyObject):
	def __init__(self, msg, size, pos=(0, 0), color=(224, 224, 224)):
		EmptyObject.__init__(self, pos)
		fontObj = pygame.font.Font('freesansbold.ttf', int(size))
		self.textObj = fontObj.render(msg, True, color)
		self.rect = self.textObj.get_rect()
		self.rect.topleft = pos
		# screen.blit(textSurfaceObj, textRectObj)

	def blit(self, screen):
		screen.blit(self.textObj, self.rect)

	def clicked(self, pos):
		pass
			# pygame.mixer.music.rewind()


# def text(screen, msg, pos, size, color=(224, 224, 224)): # merci a alex pour l'affichage du texte :)
# 	fontObj = pygame.font.Font('freesansbold.ttf', int(size))
# 	textSurfaceObj = fontObj.render(msg, True, color)
# 	textRectObj = textSurfaceObj.get_rect()
# 	textRectObj.topleft = pos
# 	screen.blit(textSurfaceObj, textRectObj)
	# pygame.display.update(textRectObj)





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

song1 = SongItem((30, 60), musicList[0])
song2 = SongItem((30, 100), musicList[1])
song3 = SongItem((30, 140), musicList[2])
song4 = SongItem((30, 180), musicList[3])
rewBtn = RewindButton(pos=(10, 270))
# text = Label("Test", 15)

content.append(song1)
content.append(song2)
content.append(song3)
content.append(song4)
content.append(rewBtn)

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
	song1.blit(screen)
	song2.blit(screen)
	song3.blit(screen)
	song4.blit(screen)
	rewBtn.blit(screen)
	# text.blit(screen)
	pygame.display.update()
	FPSCLOCK.tick(60)
