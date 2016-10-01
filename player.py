import pygame
from pygame.locals import *
import sys
import datetime
import os

pygame.init()
screen = pygame.display.set_mode((480, 320))
FPSCLOCK = pygame.time.Clock()
pygame.mixer.init()
END_MUSIC_EVENT = pygame.USEREVENT + 0
pygame.mixer.music.set_endevent(END_MUSIC_EVENT)


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

from utils import *
from generics import *


class Playlist(HContainer):
	def __init__(self, pos=(0, 0)):
		HContainer.__init__(self, pos)
		self.pages = []
		self.backBtn = BackButton(self)
		HContainer.append(self, self.backBtn)
		self.mainPage = GenericObject(size=(384, 174))
		self.mainPage.enabled = False
		HContainer.append(self, self.mainPage)
		self.forwardBtn = ForwardButton(self)
		HContainer.append(self, self.forwardBtn)

		HContainer.centerContent(self)
		# self.content.append(self.pages)
		self.pageNumber = 0

	def appendPage(self, page):
		page.setAbsPos(self.mainPage.rect.topleft)
		self.pages.append(page)

	def getRef(self, pos=(0, 0)):
		for obj in self.content:
			if obj.enabled == True:
				if obj.rect.collidepoint(pos):
					objRef = obj.getRef(pos)
					return objRef

		for obj in self.pages:
			if obj.enabled == True:
				if obj.rect.collidepoint(pos):
					objRef = obj.getRef(pos)
					return objRef
		return self

	def blit(self, screen):
		self.backBtn.blit(screen)

		self.pages[self.pageNumber].blit(screen)
		self.forwardBtn.blit(screen)

class BackButton(GenericButton):
	size = GenericButton.size
	image = pygame.image.load("./data/img/backBtn.png").convert_alpha()
	image = pygame.transform.scale(image, size)

	def __init__(self, playlistObj, pos=(0, 0)):
		GenericButton.__init__(self, pos)
		self.playlistObj = playlistObj
		self.enabled = False
		# self.image = self.playImage

	def onClick(self, pos=(0, 0)):
		if self.enabled is True:
			self.playlistObj.pages[self.playlistObj.pageNumber].enabled = False
			self.playlistObj.pageNumber -= 1
			self.playlistObj.pages[self.playlistObj.pageNumber].enabled = True

			# tempPos = self.playlistObj.pages[self.playlistObj.pageNumber].rect.topleft
			self.playlistObj.pages[self.playlistObj.pageNumber].setAbsPos(self.playlistObj.mainPage.rect.topleft)
			# self.playlistObj.pages[0].rect.topleft = tempPos

			self.playlistObj.forwardBtn.enabled = True
			if self.playlistObj.pageNumber == 0:
				self.enabled = False

	def blit(self, screen):
		if self.enabled is True:
			screen.blit(self.image, self.rect.topleft)


class ForwardButton(GenericButton):
	size = GenericButton.size
	image = pygame.image.load("./data/img/forwardBtn.png").convert_alpha()
	image = pygame.transform.scale(image, size)

	def __init__(self, playlistObj, pos=(0, 0)):
		GenericButton.__init__(self, pos)
		self.playlistObj = playlistObj
		# self.image = self.playImage

	def onClick(self, pos=(0, 0)):
		print("CLICKED")
		if self.enabled is True:
			self.playlistObj.pages[self.playlistObj.pageNumber].enabled = False
			self.playlistObj.pageNumber += 1
			self.playlistObj.pages[self.playlistObj.pageNumber].enabled = True

			# tempPos = self.playlistObj.pages[self.playlistObj.pageNumber].rect.topleft
			self.playlistObj.pages[self.playlistObj.pageNumber].setAbsPos(self.playlistObj.mainPage.rect.topleft)
			# self.playlistObj.pages[0].rect.topleft = tempPos

			self.playlistObj.backBtn.enabled = True
			if self.playlistObj.pageNumber == len(self.playlistObj.pages) - 1:
				self.enabled = False

	def blit(self, screen):
		if self.enabled is True:
			screen.blit(self.image, self.rect.topleft)


class Page(VContainer):
	def __init__(self, pos=(0, 0)):
		VContainer.__init__(self, pos)

	def append(self, obj):
		VContainer.append(self, obj)

		spaceObj = GenericObject(size=(0, 10))
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
		spaceObj = GenericObject(size=(18, 0))
		HContainer.append(self, spaceObj)

		for iterateObj in self.content:
			yVector = self.rect.centery - iterateObj.rect.centery
			iterateObj.setRelPos((0, yVector))

	def play(self):
		pygame.mixer.music.load(self.song_path)
		Player.current_song_path = self.song_path
		Player.play()

	def pause(self):
		Player.pause()

	def unpause(self):
		Player.unpause()


class SongPlayButton(GenericButton):
	size = GenericButton.size
	playImage = pygame.image.load("./data/img/playBtn.png").convert_alpha()
	playImage = pygame.transform.scale(playImage, size)
	pauseImage = pygame.image.load("./data/img/pauseBtn.png").convert_alpha()
	pauseImage = pygame.transform.scale(pauseImage, size)

	def __init__(self, songItemObj, pos=(0, 0)):
		GenericButton.__init__(self, pos)
		self.songItemObj = songItemObj
		# self.image = self.playImage

	def onClick(self, pos=(0, 0)):
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


class GlobalPlayButton(GenericButton):
	size = GenericButton.size
	playImage = pygame.image.load("./data/img/playBtn.png").convert_alpha()
	playImage = pygame.transform.scale(playImage, size)
	pauseImage = pygame.image.load("./data/img/pauseBtn.png").convert_alpha()
	pauseImage = pygame.transform.scale(pauseImage, size)

	def __init__(self, pos=(0, 0)):
		GenericButton.__init__(self, pos)

	def onClick(self, pos=(0, 0)):
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

	def onClick(self, pos=(0, 0)):
		pygame.mixer.music.rewind()

	def blit(self, screen):
		screen.blit(self.image, self.rect.topleft)


class Label(GenericObject):
	def __init__(self, msg, fontSize, pos=(0, 0), color=(224, 224, 224)):
		GenericObject.__init__(self, pos)
		self.fontSize = fontSize
		self.message = msg[:27]
		if self.message != msg:
			self.message += "..."

		self.fontColor = color

		fontObj = pygame.font.Font('freesansbold.ttf', int(self.fontSize))
		self.textObj = fontObj.render(self.message, True, self.fontColor)
		self.rect = self.textObj.get_rect()
		self.rect.topleft = pos

	def blit(self, screen):
		screen.blit(self.textObj, self.rect)

	def changeText(self, msg):
		self.textObj = fontObj.render(msg, True, self.color)
		pos = self.rect.topleft
		self.rect = self.textObj.get_rect()
		self.rect.topleft = pos


class CloseButton(GenericButton):
	size = GenericButton.size
	image = pygame.image.load("./data/img/closeBtn.png").convert_alpha()
	image = pygame.transform.scale(image, size)

	def __init__(self, pos=(0, 0)):
		GenericButton.__init__(self, pos)
		# self.enabled = True

	def onClick(self, pos=(0, 0)):
		pygame.quit()
		exit()

	def blit(self, screen):
		screen.blit(self.image, self.rect.topleft)


fond = pygame.image.load("./data/img/background.png").convert()
background = pygame.Surface(screen.get_size())
background.blit(fond, (0, 0))

# close = pygame.image.load("./data/img/close.png").convert_alpha()
# close = pygame.transform.scale(close, (36, 36))
# restart = pygame.image.load("./data/img/restart.png").convert_alpha()
# restart = pygame.transform.scale(restart, (32, 32))

music_dir = "./data/rec/"
music_names = os.listdir("./data/rec/")
musicList = []
for music_name in music_names:
	musicList.append("{}{}".format(music_dir, music_name))

playlist = Playlist(pos=(10, 60))
for i in range(0, len(musicList), 4):
	page = Page()
	for songIndex in range(i, i+4):
		try:
			song = SongItem(musicList[songIndex])
			page.append(song)
		except:
			break
	page.remove(-1)
	page.enabled = False
	playlist.appendPage(page)
playlist.pages[0].enabled = True

rewBtn = RewindButton()
spaceObj = GenericObject(size=(10, 0))
globalPlayBtn = GlobalPlayButton()
globalCtrls = HContainer(pos=(10, 270))
globalCtrls.append(rewBtn)
globalCtrls.append(spaceObj)
globalCtrls.append(globalPlayBtn)
# globalPlayBtn.setAbsPos((0, 0))
closeBtn = CloseButton(pos=(430, 8))

content = []
content.append(playlist)
content.append(globalCtrls)
content.append(closeBtn)

print(HContainer.items)

drag = False
mouseDown = False
collideObj = None

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True
			cursorPos = event.pos
			cursorVector = pygame.mouse.get_rel()

			for obj in content:
				if obj.rect.collidepoint(cursorPos):
					collideObj = obj.getRef(cursorPos)
					print("ONE TIME")
					print(collideObj)
					break

		if event.type == pygame.MOUSEMOTION:
			cursorPos = event.pos
			cursorRelPos = pygame.mouse.get_rel()
			if mouseDown is True and collideObj is not None:
				drag = True
				collideObj.drag(cursorRelPos)
				print(collideObj)

		if event.type == pygame.MOUSEBUTTONUP:
			cursorPos = event.pos

			if drag is False and collideObj is not None:
				collideObj.onClick(cursorPos)

			mouseDown = False
			drag = False
			collideObj = None

		if event.type == END_MUSIC_EVENT and event.code == 0:
			Player.played = False
			Player.paused = True
			print("END")
			print(Player.current_song_path)

	screen.blit(background, (0, 0))
	playlist.blit(screen)
	globalCtrls.blit(screen)
	closeBtn.blit(screen)

	pygame.display.update()
	FPSCLOCK.tick(60)
