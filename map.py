from PIL import Image
import pygame
import const
from tile import Tile

pygame.init()

class Map:
    def __init__(self, rows, columns, sample_image_path):
        self.rows = rows
        self.columns = columns
        self.sample_image = Image.open(sample_image_path).convert('RGBA')
        self.tileset = []#Pygame -> Surface
        self.tileset_images = []#Pillow -> Image

        self.sample_map = []
        self.constraints = []

        self.parse_tileset()
        self.calculate_constraints()

    def unique_tile(self, image):
        if (len(self.tileset_images) == 0):
            return -1
        
        for index, tile in enumerate(self.tileset_images):
            if list(tile.getdata()) == list(image.getdata()):
                return index
        
        return -1

    # read through the sample image and creates the tileset
    def parse_tileset(self):
        image_rows = self.sample_image.height//const.TILE_SIZE
        image_columns = self.sample_image.width//const.TILE_SIZE

        image_map = []

        for row in range(image_rows):
            image_row = []
            for column in range(image_columns):
                image = self.sample_image.crop((column*const.TILE_SIZE, row*const.TILE_SIZE, (column+1)*const.TILE_SIZE, (row+1)*const.TILE_SIZE))
                image_row.append(image)
                if image.getextrema()[3][0] != 0:
                    if self.unique_tile(image) == -1:
                        self.tileset_images.append(image)

                        self.tileset.append(const.image_to_surface(image))
            image_map.append(image_row)

        self.sample_map = [[Tile(r, c, self.tileset, True, 0) for c in range(image_columns)] for r in range(image_rows)]
        for row, image_row in enumerate(image_map):
            for column, image in enumerate(image_row):
                self.sample_map[row][column].tile = self.unique_tile(image)

    #Return the indexes of top, bottom, left and right neighbors of a given index
    def find_neighboring_sides(self, row, column):
        # 0 = top side, 1 = bottom side, 2 = left side, 3 = right side
        neighboring_sides = [(row-1, column) if row > 0 else None, (row+1, column) if row < self.rows-1 else None, (row, column-1) if column > 0 else None, (row, column+1)  if column < self.columns-1 else None]
        return filter(lambda val: val !=  None, neighboring_sides)

    # Calculates the allowed adjacent tiles to each tile type
    def calculate_constraints(self):
        # 0 = top side, 1 = bottom side, 2 = left side, 3 = right side
        self.constraints = {t : [set(), set(), set(), set()] for t in range(len(self.tileset))}

        for r, row in enumerate(self.sample_map):
            for c, tile in enumerate(row):
                p_tile = tile.tile

                for i, [n_row, n_column] in enumerate(self.find_neighboring_sides(r, c)):
                    if -1 < n_row and -1 < n_column:
                        try:
                            self.constraints[p_tile][i].add(self.sample_map[n_row][n_column].tile)
                        except IndexError:
                            pass
                        except KeyError:
                            pass

    def draw_map(self, screen, map, offset=[0, 0]):
        for r, row in enumerate(map):
            for c, tile in enumerate(row):
                tile.draw(offset, screen)

    # Takes a 2d array of Tiles and returns an 2d array of surfaces using the tileset
    @staticmethod
    def map_to_surfaces(map, tileset):
        new_map = []

        for row in map:
            new_row = []
            for tile in row:
                if tile.get_entropy() == 1:
                    new_row.append(tileset[tile.tile])
                else:
                    new_row.append(None)
            new_map.append(new_row)
        
        return new_map