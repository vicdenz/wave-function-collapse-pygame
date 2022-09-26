import random
from tile import Tile
from map import Map

class Generator:
    @staticmethod
    def propagate(map, function, error_tiles, row, column):
        to_change = [(row, column)]

        while len(to_change) != 0:
            for row, column in to_change.copy():
                p_tile = function[row][column]

                if p_tile.get_entropy() > 0:
                    #get contraints from collapsed tile
                    p_constraint = [set(), set(), set(), set()]
                    if p_tile.collapsed:
                        p_constraint = map.constraints[p_tile.tile]
                    else:
                        for possibility in p_tile.wave:
                            for i, side in enumerate(map.constraints[possibility]):
                                p_constraint[i] = p_constraint[i].union(side)
                    #We need to remove the possibilites THAT AREN'T in p_contraint, so we invert it to check
                    p_constraint = Generator.invert_adjacent(p_constraint, len(map.tileset))

                    p_neighbors = map.find_neighboring_sides(row, column)
                    side_coords = p_tile.update_neighbors(function, p_neighbors, p_constraint)
                    for side_coord in side_coords:
                        if side_coord not in to_change:
                            to_change.append(side_coord)
                        
                        if function[side_coord[0]][side_coord[1]].get_entropy() == 0:
                            error_tiles.append(side_coord)

                p_tile.counter += 1
                to_change.remove((row, column))
        
        return function, error_tiles

    @staticmethod
    def find_next_tile(function, tileset):
        lowest_entropy = len(tileset)+1
        lowest_coords = []

        for row in range(len(function)):
            for column in range(len(function[row])):
                tile = function[row][column]
                if not tile.collapsed:
                    tile_entropy = tile.get_entropy()
                    if 0 < tile_entropy < lowest_entropy:
                        lowest_entropy = tile_entropy
                        lowest_coords = [(row, column)]
                    elif tile_entropy == lowest_entropy:
                        lowest_coords.append((row, column))
        if len(lowest_coords) != 0:
            return lowest_coords[random.randint(0, len(lowest_coords)-1)]

    @staticmethod
    def collapse_tile(function, row, column):
        function[row][column].tile = function[row][column].wave[random.randrange(len(function[row][column].wave))]

        function[row][column].collapsed = True

    # Takes a contraints list and inverts each side's set
    @staticmethod
    def invert_adjacent(adjacent, num_of_tiles):
        constraint = []
        for side in adjacent:
            constraint_side = set()
            for i in range(num_of_tiles):
                if i not in side:
                    constraint_side.add(i)
            constraint.append(constraint_side)
        return constraint

    @staticmethod
    def generate(map):
        generated_map = [[Tile(row, column, map.tileset) for column in range(map.columns)] for row in range(map.rows)]

        error_tiles = []

        while (next_tile := Generator.find_next_tile(generated_map, map.tileset)) != None:
            current_row = next_tile[0]
            current_column = next_tile[1]
            Generator.collapse_tile(generated_map, current_row, current_column)

            generated_map, error_tiles = Generator.propagate(map, generated_map, error_tiles, current_row, current_column)

        return generated_map, error_tiles