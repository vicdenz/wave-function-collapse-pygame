import pygame
import const
from math import sqrt, ceil

class Tile:
    def __init__(self, row, column, tileset, collapsed=False, tile=0):
        self.row = row
        self.column = column
        self.tileset = tileset#Pygame -> Surface
        self.wave = [tile] if collapsed else list(range(len(self.tileset)))
        self.collapsed = collapsed
        self.entropy = self.update_entropy()

    def update_entropy(self):
        self.entropy = len(self.wave)
        return self.entropy
    
    def draw(self, offset, screen):
        grid_size = ceil(sqrt(len(self.tileset)))
        tile_size = const.TILE_SIZE // grid_size

        if self.collapsed:
            surface = self.tileset[self.wave[0]]
            rect = surface.get_rect(x=self.column*const.TILE_SIZE+offset[0], y=self.row*const.TILE_SIZE+offset[1])

            screen.blit(surface, rect)

            font = pygame.font.SysFont("Arial", 16)
            text = font.render(str(self.wave), True, (255, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else:
            for possibility in self.wave:
                surface = pygame.transform.scale(self.tileset[possibility], (tile_size, tile_size))
                rect = surface.get_rect(x=self.column*const.TILE_SIZE+(possibility%grid_size)*tile_size+offset[0], y=self.row*const.TILE_SIZE+(possibility//grid_size)*tile_size+offset[1])

                screen.blit(surface, rect)