import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from settings import *



class Pathfinder:

	def __init__(self, matrix, player):

		self.player = player
		self.display_surface = pygame.display.get_surface()

		self.offset = pygame.math.Vector2()
		self.matrix = matrix


		# setup

		self.grid = Grid(matrix = self.matrix)
		self.select_surf = pygame.image.load('graphics/test/selection.png').convert_alpha()

		# pathfinding
		self.path = []

		self.path_allowed = False

		# x <= 0 can't walk on, x > 0 can wak on
		# boundary = -395

	def draw_active_cell(self):
		self.offset.x = self.player.rect.centerx - WIDTH // 2
		self.offset.y = self.player.rect.centery - HEIGTH // 2

		mouse_pos = pygame.mouse.get_pos()
		row =  int((mouse_pos[1] + self.offset.y) // 64 + 1)
		col =  int((mouse_pos[0] + self.offset.x)// 64 + 1)


		current_cell_value = self.matrix[row][col]

		rect = pygame.Rect((mouse_pos[0] - 16 ,mouse_pos[1] - 16 ),(64,64))
		self.display_surface.blit(self.select_surf,rect)

		if current_cell_value == -395:
			self.path_allowed = False
		else:
			self.path_allowed = True

	def get_coord(self):
		self.offset.x = self.player.rect.centerx - WIDTH // 2
		self.offset.y = self.player.rect.centery - HEIGTH // 2

		mouse_pos = pygame.mouse.get_pos()
		row = int((self.player.hitbox.centery - self.offset.y) // 64 + 1)
		col = int((self.player.hitbox.centerx - self.offset.x) // 64 + 1)
		return (col,  row)

	def create_path(self):
		self.offset.x = self.player.rect.centerx - WIDTH // 2
		self.offset.y = self.player.rect.centery - HEIGTH // 2

		# start
		start_x = int(self.player.rect.centerx // 64 + 1)
		start_y = int(self.player.rect.centery // 64 + 1) # player location
		start = self.grid.node(start_x,start_y)

		# end
		mouse_pos = pygame.mouse.get_pos()
		end_x = int((mouse_pos[0] + self.offset.x) // 64)
		end_y =  int((mouse_pos[1] + self.offset.y) // 64)
		end = self.grid.node(end_x,end_y)

		# path
		finder = AStarFinder()
		self.player.path,self.runs = finder.find_path(start,end,self.grid)
		print (self.player.path, end, start)
		self.grid.cleanup()
		self.player.set_path(self.player.path)




