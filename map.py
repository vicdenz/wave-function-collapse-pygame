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
        self.sample_image = Image.open(sample_image_path).convert('RGBA')
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

        image_map = []

        for row in range(image_rows):
            image_row = []
            for column in range(image_columns):
                image = self.sample_image.crop((column*const.TILE_SIZE, row*const.TILE_SIZE, (column+1)*const.TILE_SIZE, (row+1)*const.TILE_SIZE))
                image_row.append(image)
                if image.getextrema()[3][0] != 0:
                    if self.unique_tile(image) == -1:
                        self.tileset.append(image)

                        self.tileset_images.append(const.image_to_surface(image))
            image_map.append(image_row)

        self.sample_map = [[Tile(r, c, self.tileset_images, True, 0) for c in range(image_columns)] for r in range(image_rows)]
        for row, image_row in enumerate(image_map):
            for column, image in enumerate(image_row):
                self.sample_map[row][column].tile = self.unique_tile(image)

    def find_neighboring_sides(self, row, column):
        # 0 = top side, 1 = bottom side, 2 = left side, 3 = right side
        return [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]

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
                    new_row.append(self.tileset_images[tile.tile])
                else:
                    new_row.append(None)
            new_map.append(new_row)
        
        return new_map

    # Generates a new pseudo-random map to the sample map
    def generate_map(self):
        generated_map = [[Tile(row, column, self.tileset_images) for column in range(self.columns)] for row in range(self.rows)]

        error_tiles = []

        def propagate(map, row, column):
            to_change = [(row, column)]

            while len(to_change) != 0:
                for row, column in to_change.copy():
                    p_tile = map[row][column]

                    if p_tile.get_entropy() > 0:
                        #get contraints from collapsed tile
                        p_constraint = [set(), set(), set(), set()]
                        if p_tile.collapsed:
                            p_constraint = self.constraints[p_tile.tile]
                        else:
                            for possibility in p_tile.wave:
                                for i, side in enumerate(self.constraints[possibility]):
                                    p_constraint[i] = p_constraint[i].union(side)
                        #We need to remove the possibilites THAT AREN'T in p_contraint, so we invert it to check
                        p_constraint = self.invert_adjacent(p_constraint)

                        p_neighbors = self.find_neighboring_sides(row, column)
                        side_coords = p_tile.update_neighbors(map, p_neighbors, p_constraint)
                        for side_coord in side_coords:
                            if side_coord not in to_change:
                                to_change.append(side_coord)
                            
                            if map[side_coord[0]][side_coord[1]].get_entropy() == 0:
                                error_tiles.append(side_coord)

                    p_tile.counter += 1
                    to_change.remove((row, column))

        def find_next_tile(map):
            lowest_entropy = len(self.tileset)+1
            lowest_coords = []

            for row in range(len(map)):
                for column in range(len(map[row])):
                    tile = map[row][column]
                    if not tile.collapsed:
                        tile_entropy = tile.get_entropy()
                        if 0 < tile_entropy < lowest_entropy:
                            lowest_entropy = tile_entropy
                            lowest_coords = [(row, column)]
                        elif tile_entropy == lowest_entropy:
                            lowest_coords.append((row, column))
            if len(lowest_coords) != 0:
                return lowest_coords[random.randint(0, len(lowest_coords)-1)]

        def collapse_tile(map, row, column):
            map[row][column].tile = map[row][column].wave[random.randrange(len(map[row][column].wave))]

            map[row][column].collapsed = True

        while (next_tile := find_next_tile(generated_map)) != None:
            current_row = next_tile[0]
            current_column = next_tile[1]
            collapse_tile(generated_map, current_row, current_column)

            propagate(generated_map, current_row, current_column)

        for row in generated_map:
            print([tile.counter for tile in row])

        return generated_map, error_tiles