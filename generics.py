import pygame
from utils import *

class GenericContainer:
	items = []
	def __init__(self, pos):
		self.content = []
		self.rect = pygame.Rect(pos, (0, 0))
		self.enabled = True

		self.items.append(self)

	def append(self, obj):
		self.content.append(obj)

	def remove(self, pos):
		del self.content[pos]

	def getRef(self, pos=(0, 0)):
		if self.enabled is True:
			for obj in self.content:
				if obj.rect.collidepoint(pos):
					objRef = obj.getRef(pos)
					return objRef
			return self

	def onMouseDown(self, pos=(0, 0)):
		pass

	def drag(self, pos):
		pass
		# self.setRelPos(pos)

	def onClick(self, pos=(0, 0)):
		pass
		# for obj in self.content:
		# 	if obj.rect.collidepoint(pos):
		# 		obj.onClick(pos)
		# 		break

	def blit(self, screen):
		if self.enabled is True:
			for obj in self.content:
				obj.blit(screen)

	def setAbsPos(self, pos):
		vector = substract_tuples(pos, self.rect.topleft)

		self.rect.topleft = pos
		for obj in self.content:
			obj.setRelPos(vector)

	def setRelPos(self, vector):
		self.rect.topleft = add_tuples(self.rect.topleft, vector)
		for obj in self.content:
			obj.setRelPos(vector)


class HContainer(GenericContainer):
	def append(self, obj):
		GenericContainer.append(self, obj)

		obj.setAbsPos(self.rect.topright)
		self.rect.width += obj.rect.width
		if obj.rect.height > self.rect.height:
			self.rect.height = obj.rect.height

	def remove(self, pos):
		widthToRemove = self.content[pos].rect.width
		GenericContainer.remove(self, pos)
		self.rect.width = self.rect.width - widthToRemove

	def centerContent(self):
		for iterateObj in self.content:
			yVector = self.rect.centery - iterateObj.rect.centery
			iterateObj.setRelPos((0, yVector))


class VContainer(GenericContainer):
	def append(self, obj):
		GenericContainer.append(self, obj)

		obj.setAbsPos(self.rect.bottomleft)
		self.rect.height += obj.rect.height
		if obj.rect.width > self.rect.width:
			self.rect.width = obj.rect.width

	def remove(self, pos):
		heightToRemove = self.content[pos].rect.height
		GenericContainer.remove(self, pos)
		self.rect.height = self.rect.height - heightToRemove

	def centerContent(self):
		for iterateObj in self.content:
			xVector = self.rect.centerx - iterateObj.rect.centerx
			iterateObj.setRelPos((xVector, 0))


class GenericObject:
	def __init__(self, pos=(0, 0), size=(0, 0)):
		self.rect = pygame.Rect(pos, size)
		self.enabled = True

	def getRef(self, pos=(0, 0)):
		if self.enabled is True:
			return self

	def onMouseDown(self, pos=(0, 0)):
		pass

	def drag(self, pos):
		pass
		# self.setRelPos(pos)

	def onClick(self, pos=(0, 0)):
		pass

	def blit(self, screen):
		if self.enabled is True:
			pass

	def setAbsPos(self, pos):
		self.rect.topleft = pos

	def setRelPos(self, vector):
		self.rect.topleft = add_tuples(self.rect.topleft, vector)


class GenericButton(GenericObject):
	size = (36, 36)
	def __init__(self, pos=(0, 0)):
		GenericObject.__init__(self, pos, self.size)
