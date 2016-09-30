import pygame
from pygame.locals import *
import sys
import datetime
import os

pygame.init()
FPSCLOCK = pygame.time.Clock()
pygame.mixer.init()
END_MUSIC_EVENT = pygame.USEREVENT + 0
pygame.mixer.music.set_endevent(END_MUSIC_EVENT)
screen = pygame.display.set_mode((480, 320))


def add_tuples(tup1, tup2):
	ls1 = list(tup1)
	ls2 = list(tup2)
	ls = [x + y for x, y in zip(tup1, tup2)]
	tup = tuple(ls)
	return tup

def substract_tuples(tup1, tup2):
	ls1 = list(tup1)
	ls2 = list(tup2)
	ls = [x - y for x, y in zip(tup1, tup2)]
	tup = tuple(ls)
	return tup

def getSongName(song_path):
	pathLs = song_path.split("/")
	fileNameLs = pathLs[-1].split(".")
	songName = fileNameLs[0]
	return songName


class Player:
	current_song_path = ""
	played = False
	paused = True

	@staticmethod
	def play():
		pygame.mixer.music.play()
		Player.played = True
		Player.paused = False

	@staticmethod
	def pause():
		pygame.mixer.music.pause()
		Player.paused = True

	@staticmethod
	def unpause():
		pygame.mixer.music.unpause()
		Player.paused = False


class GenericContainer:
	items = []
	def __init__(self, pos):
		self.content = []
		self.rect = pygame.Rect(pos, (0, 0))

		self.items.append(self)

	def append(self, obj):
		self.content.append(obj)

	def blit(self, screen):
		for obj in self.content:
			obj.blit(screen)

	def clicked(self, pos):
		for obj in self.content:
			if obj.rect.collidepoint(pos):
				obj.clicked(pos)
				break

	def setPos(self, pos):
		relPos = substract_tuples(pos, self.rect.topleft)

		self.rect.topleft = pos
		for obj in self.content:
			obj.setPos(add_tuples(obj.rect.topleft, relPos))


class HContainer(GenericContainer):
	def append(self, obj):
		GenericContainer.append(self, obj)

		obj.setPos(self.rect.topright)
		self.rect.width += obj.rect.width
		if obj.rect.height > self.rect.height:
			self.rect.height = obj.rect.height


class VContainer(GenericContainer):
	def append(self, obj):
		GenericContainer.append(self, obj)

		obj.setPos(self.rect.bottomleft)
		self.rect.height += obj.rect.height
		if obj.rect.width > self.rect.width:
			self.rect.width = obj.rect.width


class Playlist(VContainer):
	def __init__(self, pos=(0, 0)):
		VContainer.__init__(self, pos)

	def append(self, obj):
		VContainer.append(self, obj)

		spaceObj = GenericObject(size=(self.rect.width, 10))
		VContainer.append(self, spaceObj)


class SongItem(HContainer):
	items = []
	def __init__(self, song_path, pos=(0, 0)):
		HContainer.__init__(self, pos)
		print(self.items)
		# self.pos = pos
		self.song_path = song_path
		self.song_name = getSongName(song_path)
		print(self.song_name)

		# self.append(RewindButton)
		playBtn = SongPlayButton(self)
		self.append(playBtn)

		textObj = Label(self.song_name, 18)
		self.append(textObj)
		# self.played = False
		# self.paused = True

	def append(self, obj):
		HContainer.append(self, obj)
		spaceObj = GenericObject(size=(18, self.rect.height))
		HContainer.append(self, spaceObj)

	def play(self):
		pygame.mixer.music.load(self.song_path)
		Player.current_song_path = self.song_path
		Player.play()

	def pause(self):
		Player.pause()

	def unpause(self):
		Player.unpause()


class GenericObject:
	def __init__(self, pos=(0, 0), size=(0, 0)):
		self.rect = pygame.Rect(pos, size)

	def clicked(self, pos):
		pass

	def blit(self, screen):
		pass

	def setPos(self, pos):
		self.rect.topleft = pos


class GenericButton(GenericObject):
	size = (36, 36)
	def __init__(self, pos=(0, 0)):
		print(self)
		print("\n")
		GenericObject.__init__(self, pos, self.size)


class GenericPlayButton(GenericButton):
	size = GenericButton.size
	playImage = pygame.image.load("./data/img/playBtn.png").convert_alpha()
	playImage = pygame.transform.scale(playImage, size)
	pauseImage = pygame.image.load("./data/img/pauseBtn.png").convert_alpha()
	pauseImage = pygame.transform.scale(pauseImage, size)
	def __init__(self, pos=(0, 0)):
		GenericButton.__init__(self, pos)


class SongPlayButton(GenericPlayButton):
	def __init__(self, songItemObj, pos=(0, 0)):
		GenericPlayButton.__init__(self, pos)
		self.songItemObj = songItemObj
		# self.image = self.playImage

	def clicked(self, pos):
		print("CLICKED ON PLAY {}".format(self.rect)) ## DEBUGGING
		if Player.played == False or self.songItemObj.song_path != Player.current_song_path:
			self.songItemObj.play()
			# self.image = self.pauseImage
		else:
			if Player.paused == False:
				self.songItemObj.pause()
				# self.image = self.playImage
			else:
				self.songItemObj.unpause()
				# self.image = self.pauseImage

	def blit(self, screen):
		if Player.current_song_path == self.songItemObj.song_path \
		and Player.played == True and Player.paused == False:
			screen.blit(self.pauseImage, self.rect.topleft)
		else:
			screen.blit(self.playImage, self.rect.topleft)


class GlobalPlayButton(GenericPlayButton):
	def __init__(self, pos=(0, 0)):
		GenericPlayButton.__init__(self, pos)

	def clicked(self, pos):
		print("CLICKED ON PLAY {}".format(self.rect)) ## DEBUGGING
		if Player.played == False:
			pygame.mixer.music.play()
			Player.played = True
			Player.paused = False
		else:
			if Player.paused == False:
				pygame.mixer.music.pause()
				Player.paused = True
				# self.image = self.playImage
			else:
				pygame.mixer.music.unpause()
				Player.paused = False
				# self.image = self.pauseImage

	def blit(self, screen):
		if Player.played == True and Player.paused == False:
			screen.blit(self.pauseImage, self.rect.topleft)
		else:
			screen.blit(self.playImage, self.rect.topleft)


class RewindButton(GenericButton):
	size = GenericButton.size
	image = pygame.image.load("./data/img/rewindBtn.png").convert_alpha()
	image = pygame.transform.scale(image, size)

	def __init__(self, pos=(0, 0)):
		GenericButton.__init__(self, pos)

	def clicked(self, pos):
		pygame.mixer.music.rewind()

	def blit(self, screen):
		screen.blit(self.image, self.rect.topleft)


class Label(GenericObject):
	def __init__(self, msg, fontSize, pos=(0, 0), color=(224, 224, 224)):
		GenericObject.__init__(self, pos)
		fontObj = pygame.font.Font('freesansbold.ttf', int(fontSize))
		self.textObj = fontObj.render(msg, True, color)
		self.rect = self.textObj.get_rect()
		self.rect.topleft = pos

	def clicked(self, pos):
		pass

	def blit(self, screen):
		screen.blit(self.textObj, self.rect)


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

song1 = SongItem(musicList[0])
song2 = SongItem(musicList[1])
song3 = SongItem(musicList[2])
song4 = SongItem(musicList[3])
playlist = Playlist(pos=(30, 60))
playlist.append(song1)
playlist.append(song2)
playlist.append(song3)
playlist.append(song4)

rewBtn = RewindButton()
spaceObj = GenericObject(size=(10, 0))
globalPlayBtn = GlobalPlayButton()
globalCtrls = HContainer(pos=(10, 270))
globalCtrls.append(rewBtn)
globalCtrls.append(spaceObj)
globalCtrls.append(globalPlayBtn)

content.append(playlist)
content.append(globalCtrls)

print(HContainer.items)

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

		if event.type == END_MUSIC_EVENT and event.code == 0:
			Player.played = False
			Player.paused = True
			print("END")
			print(Player.current_song_path)

	screen.blit(background, (0, 0))
	playlist.blit(screen)
	globalCtrls.blit(screen)

	pygame.display.update()
	FPSCLOCK.tick(60)
