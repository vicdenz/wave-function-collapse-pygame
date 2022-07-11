from PIL import Image, ImageChops
import pygame
import const
import random
from math import sqrt, ceil

pygame.init()

class Heuristic:
    def __init__(self, rows, columns, sample_image_path):
        self.rows = rows
        self.columns = columns
        self.sample_image = Image.open(sample_image_path).convert('RGB')
        self.tileset = []#Pillow -> Image
        self.tileset_images = []#Pygame -> Surface
        self.sample_map = [[0 for c in range(self.columns)] for r in range(self.rows)]

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
        self.sample_map = [[0 for c in range(image_columns)] for r in range(image_rows)]

        for row in range(image_rows):
            for column in range(image_columns):
                image = self.sample_image.crop((column*const.TILE_SIZE, row*const.TILE_SIZE, (column+1)*const.TILE_SIZE, (row+1)*const.TILE_SIZE))
                if self.unique_tile(image) == -1:
                    self.tileset.append(image)

                    self.tileset_images.append(const.image_to_surface(image))

                self.sample_map[row][column] = self.unique_tile(image)

    def find_neighboring_sides(self, row, column):
        return [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]

    # Calculates the allowed adjacent tiles to each tile type
    def calculate_constraints(self):
        # 0 = top side, 1 = bottom side, 2 = left side, 3 = size side
        self.constraints = {t : [set(range(len(self.tileset))), set(range(len(self.tileset))), set(range(len(self.tileset))), set(range(len(self.tileset)))] for t in range(len(self.tileset))}

        for r, row in enumerate(self.sample_map):
            for c, tile in enumerate(row):

                for i, [n_row, n_column] in enumerate(self.find_neighboring_sides(r, c)):
                    if n_row > -1 and n_column > -1:
                        try:
                            self.constraints[tile][i].remove(self.sample_map[n_row][n_column])
                        except KeyError:
                            pass
                        except IndexError:
                            pass

    def draw_map(self, screen, map, offset=[0, 0]):
        grid_size = ceil(sqrt(len(self.tileset)))
        tile_size = const.TILE_SIZE // grid_size

        for r, row in enumerate(map):
            for c, tile in enumerate(row):
                if type(tile) == list and len(tile) == 1:
                    tile = tile[0]
                if type(tile) == int:
                    surface = self.tileset_images[tile]
                    rect = surface.get_rect(x=c*const.TILE_SIZE+offset[0], y=r*const.TILE_SIZE+offset[1])

                    screen.blit(surface, rect)

                    font = pygame.font.SysFont("Arial", 16)
                    text = font.render(str(tile), True, (255, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
                else:
                    for possibility in tile:
                        surface = pygame.transform.scale(self.tileset_images[possibility], (tile_size, tile_size))
                        rect = surface.get_rect(x=c*const.TILE_SIZE+(possibility%grid_size)*tile_size, y=r*const.TILE_SIZE+(possibility//grid_size)*tile_size)

                        screen.blit(surface, rect)

    # Takes a adjacent list and inverts each side's set
    def invert_adjacent(self, adjacent):
        constraint = []
        for side in adjacent:
            constraint_side = set()
            for i in range(len(self.tileset)):
                if i not in side:
                    constraint_side.add(i)
            constraint.append(constraint_side)
        return constraint

    # Generates a new pseudo-random map to the sample map
    def generate_map(self):
        wave = [[list(range(len(self.tileset))) for column in range(self.columns)] for row in range(self.rows)]

        def propagate(wave, row, column):
            to_change = [(row, column)]

            while len(to_change) != 0:
                for row, column in to_change.copy():
                    constraint = [set(), set(), set(), set()]
                    for p_tile in wave[row][column]:
                        p_constraint = self.constraints[p_tile]
                        for side in range(len(constraint)):
                            constraint[side] = constraint[side].union(p_constraint[side])

                    for i, [n_row, n_column] in enumerate(self.find_neighboring_sides(row, column)):
                        if n_row > -1 and n_column > -1:
                            try:
                                for p_tile in wave[n_row][n_column].copy():
                                    if p_tile in constraint[i]:
                                        wave[n_row][n_column].remove(p_tile)

                                        side_coord = (n_row, n_column)
                                        if side_coord not in to_change:
                                            to_change.append(side_coord)

                            except IndexError:
                                pass

                    to_change.remove((row, column))
        
        def find_next_tile():
            lowest_entropy = len(self.tileset)+1
            lowest_coords = []
            for row in range(len(wave)):
                for column in range(len(wave[row])):
                    tile = wave[row][column]
                    if len(tile) > 1:
                        if len(tile) < lowest_entropy:
                            lowest_entropy = len(tile)
                            lowest_coords = [(row, column)]
                        elif len(tile) == lowest_entropy:
                            lowest_coords.append((row, column))
            if lowest_coords == []:
                return lowest_coords
            else:
                return lowest_coords[random.randint(0, len(lowest_coords)-1)]

        def collapse_tile(row, column):
            wave[row][column] = [wave[row][column][random.randrange(len(wave[row][column]))]]

        while (next_tile := find_next_tile()) != []:
            current_row = next_tile[0]
            current_column = next_tile[1]
            collapse_tile(current_row, current_column)

            propagate(wave, current_row, current_column)

        return wave