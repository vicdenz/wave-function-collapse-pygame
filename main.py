import pygame
import const
from heuristic import Heuristic

pygame.init()

pygame.display.set_caption("Wave Function Collapse - Terrain Generation")
ROWS, COLUMNS = 20, 15
TILE_SIZE = 32
WIDTH, HEIGHT = ROWS * TILE_SIZE, COLUMNS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

heuristic = Heuristic(10, 10, const.SAMPLE_IMAGE_PATH)
heuristic.parse_tileset()
heuristic.calculate_adjacent()

new_map = heuristic.generate_map()

to_change = [(2, 2)]
def redrawGameWindow():
    screen.fill((255, 255, 255))

    heuristic.draw_map(screen, new_map)
    heuristic.draw_map(screen, heuristic.sample_map, [10*const.TILE_SIZE, 0])

    pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                running = False
            
            if event.key == pygame.K_SPACE:
                # if len(to_change) != 0:
                #     for row, column in to_change.copy():
                #         constraint = [set(), set(), set(), set()]
                #         for p_tile in new_map[row][column]:
                #             inverted_adjacent = heuristic.invert_adjacent(heuristic.allowed_adjacents[p_tile])
                #             for side in range(len(constraint)):
                #                 constraint[side] = constraint[side].union(inverted_adjacent[side])

                #         neighboring_sides = [(row, column-1), (row, column+1), (row-1, column), (row+1, column)]
                #         for i, n_side in enumerate(neighboring_sides):
                #             n_row = n_side[0]
                #             n_column = n_side[1]

                #             if n_row > -1 and n_column > -1:
                #                 try:
                #                     for p_tile in new_map[n_row][n_column].copy():
                #                         if p_tile in constraint[i]:
                #                             new_map[n_row][n_column].remove(p_tile)

                #                             side_coord = neighboring_sides[i]
                #                             if side_coord not in to_change:
                #                                 to_change.append(side_coord)

                #                 except IndexError:
                #                     pass

                #         to_change.remove((row, column))
                for row in new_map:
                    new_row = []
                    for tile in row:
                        if len(tile) == 1:
                            new_row.append(tile[0])
                        else:
                            new_row.append([])
                    print(new_row)
    
    redrawGameWindow()
pygame.quit()