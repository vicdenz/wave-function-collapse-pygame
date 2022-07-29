from PIL import Image, ImageChops
import pygame
import const
import random
from math import sqrt, ceil
from tile import Tile

pygame.init()

class Map:
    def __init__(self, rows, columns, sample_image_path):
        self.rows = rows
        self.columns = columns
        self.sample_image = Image.open(sample_image_path).convert('RGB')
        self.tileset = []#Pillow -> Image
        self.tileset_images = []#Pygame -> Surface
        self.sample_map = []

        self.constraints = []

    def unique_tile(self, image):
        if (len(self.tileset) == 0):
            return -1
        
        for index, tile in enumerate(self.tileset):
            if list(tile.getdata()) == list(image.getdata()):
                return index
        
        return -1

    # read through the sample image and creates the tileset
    def parse_tileset(self):
        image_rows = self.sample_image.height//const.TILE_SIZE
        image_columns = self.sample_image.width//const.TILE_SIZE

        for row in range(image_rows):
            for column in range(image_columns):
                image = self.sample_image.crop((column*const.TILE_SIZE, row*const.TILE_SIZE, (column+1)*const.TILE_SIZE, (row+1)*const.TILE_SIZE))
                if self.unique_tile(image) == -1:
                    self.tileset.append(image)

                    self.tileset_images.append(const.image_to_surface(image))

        self.sample_map = [[Tile(r, c, self.tileset_images, True, 0) for c in range(image_columns)] for r in range(image_rows)]
        for row in range(image_rows):
            for column in range(image_columns):
                image = self.sample_image.crop((column*const.TILE_SIZE, row*const.TILE_SIZE, (column+1)*const.TILE_SIZE, (row+1)*const.TILE_SIZE))

                self.sample_map[row][column].wave = [self.unique_tile(image)]

    def find_neighboring_sides(self, row, column):
        return [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]

    # Calculates the allowed adjacent tiles to each tile type
    def calculate_constraints(self):
        # 0 = top side, 1 = bottom side, 2 = left side, 3 = right side
        self.constraints = {t : [set(), set(), set(), set()] for t in range(len(self.tileset))}

        for r, row in enumerate(self.sample_map):
            for c, tile in enumerate(row):
                p_tile = tile.wave[0]

                for i, [n_row, n_column] in enumerate(self.find_neighboring_sides(r, c)):
                    if -1 < n_row and -1 < n_column:
                        try:
                            self.constraints[p_tile][i].add(self.sample_map[n_row][n_column].wave[0])
                        except IndexError:
                            pass
                        except KeyError:
                            pass

    def draw_map(self, screen, map, offset=[0, 0]):
        for r, row in enumerate(map):
            for c, tile in enumerate(row):
                tile.draw(offset, screen)

    # Takes a contraints list and inverts each side's set
    def invert_adjacent(self, adjacent):
        constraint = []
        for side in adjacent:
            constraint_side = set()
            for i in range(len(self.tileset)):
                if i not in side:
                    constraint_side.add(i)
            constraint.append(constraint_side)
        return constraint

    # Takes a 2d array of Tiles and returns an 2d array of surfaces using the tileset
    def map_to_surfaces(self, map):
        new_map = []

        for row in map:
            new_row = []
            for tile in row:
                if tile.get_entropy() == 1:
                    new_row.append(self.tileset_images[tile.wave[0]])
                else:
                    new_row.append(None)
            new_map.append(new_row)
        
        return new_map

    # Generates a new pseudo-random map to the sample map
    def generate_map(self):
        map = [[Tile(row, column, self.tileset_images) for column in range(self.columns)] for row in range(self.rows)]

        def propagate(map, row, column):
            to_change = [(row, column)]

            while len(to_change) != 0:
                for row, column in to_change.copy():
                    if map[row][column].get_entropy() > 0:
                        #get contraints from collapsed tile
                        p_constraint = [set(), set(), set(), set()]
                        for possibility in map[row][column].wave:
                            for i, side in enumerate(self.constraints[possibility]):
                                p_constraint[i] = p_constraint[i].union(side)
                        #We need to remove the possibilites THAT AREN'T in p_contraint, so we invert it to check
                        p_constraint = self.invert_adjacent(p_constraint)

                        p_neighbors = self.find_neighboring_sides(row, column)
                        for side_coord in map[row][column].update_wave(map, p_neighbors, p_constraint):
                            if side_coord not in to_change:
                                to_change.append(side_coord)

                    to_change.remove((row, column))

        def find_next_tile():
            lowest_entropy = len(self.tileset)+1
            lowest_coords = []
            for row in range(len(map)):
                for column in range(len(map[row])):
                    tile = map[row][column]
                    tile.get_entropy()
                    if tile.get_entropy() > 1:
                        if tile.get_entropy() < lowest_entropy:
                            lowest_entropy = tile.get_entropy()
                            lowest_coords = [(row, column)]
                        elif tile.get_entropy() == lowest_entropy:
                            lowest_coords.append((row, column))
            if lowest_coords == []:
                return lowest_coords
            else:
                return lowest_coords[random.randint(0, len(lowest_coords)-1)]

        def collapse_tile(row, column):
            map[row][column].wave = [map[row][column].wave[random.randrange(len(map[row][column].wave))]]

            map[row][column].collapsed = True
            map[row][column].get_entropy()

        while (next_tile := find_next_tile()) != []:
            current_row = next_tile[0]
            current_column = next_tile[1]
            collapse_tile(current_row, current_column)

            propagate(map, current_row, current_column)

        return map