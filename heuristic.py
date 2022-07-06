from PIL import Image, ImageChops
import pygame
import const

class Heuristic:
    def __init__(self, rows, columns, sample_image_path):
        self.rows = rows
        self.columns = columns
        self.sample_image = Image.open(sample_image_path).convert('RGB')
        self.tileset = []

    def unique_tile(self, image):
        if (len(self.tileset) == 0):
            return True
        
        unique = True
        for tile in self.tileset:
            if list(tile.getdata()) == list(image.getdata()):
                unique = False
        
        return unique

    def parse_tileset(self):
        for row in range(self.rows):
            for column in range(self.columns):
                image = self.sample_image.crop((row*const.TILE_SIZE, column*const.TILE_SIZE, (row+1)*const.TILE_SIZE, (column+1)*const.TILE_SIZE))
                if self.unique_tile(image):
                    self.tileset.append(image)