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
        self.tile = tile

    def get_entropy(self):
        return len(self.wave)
    
    def update_wave(self, map, neighbors, contraint):
        side_coords = []

        for i, [n_row, n_column] in enumerate(neighbors):
            if n_row > -1 and n_column > -1:
                try:
                    n_tile = map[n_row][n_column]
                    #Loop through wave possibilities and remove not allowed tiles
                    for possibility in n_tile.wave.copy():
                        if possibility in contraint[i]:
                            n_tile.wave.remove(possibility)

                            side_coords.append((n_row, n_column))
                    if n_tile.get_entropy() == 1:
                        n_tile.collapsed = True

                except IndexError:
                    pass
        
        return side_coords

    def draw(self, offset, screen):
        grid_size = ceil(sqrt(len(self.tileset)))
        tile_size = const.TILE_SIZE // grid_size

        if self.collapsed and self.get_entropy() > 0:
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