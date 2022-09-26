import pygame
import const
from generator import Generator
from map import Map
from tile import Tile

pygame.init()

pygame.display.set_caption("Wave Function Collapse - Terrain Generation")
ROWS, COLUMNS = 20, 15
TILE_SIZE = 32
WIDTH, HEIGHT = ROWS * TILE_SIZE, COLUMNS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

map = Map(30, 30, const.SAMPLE_IMAGE_PATH)

# new_map, error_tiles = Generator.generate(map)
# new_map_image = const.surfaces_to_image(len(new_map) * const.TILE_SIZE, len(new_map[0]) * const.TILE_SIZE, Map.map_to_surfaces(new_map, map.tileset))

new_map = [[Tile(row, column, map.tileset) for column in range(map.columns)] for row in range(map.rows)]
new_map_image = pygame.Surface((0, 0))
error_tiles = []

generate_map = True

draw_map_array = True
draw_error_tiles = False

def redrawGameWindow():
    screen.fill((255, 255, 255))

    if draw_map_array:
        map.draw_map(screen, new_map, scroll)
    else:
        screen.blit(new_map_image, scroll)

    if draw_error_tiles:
        for tile in error_tiles:
            pygame.draw.rect(screen, (255, 0, 0), [tile[1]*TILE_SIZE+scroll[0], tile[0]*TILE_SIZE+scroll[1], TILE_SIZE, TILE_SIZE])
    # map.draw_map(screen, map.sample_map, [map.columns*const.TILE_SIZE+scroll[0], scroll[1]])

    pygame.display.update()

scroll = [0, 0]
scrol_speed = 5
running = True
while running:
    clock.tick(const.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                running = False

            if event.key == pygame.K_e:
                draw_error_tiles = not draw_error_tiles

            if event.key == pygame.K_SPACE:
                draw_map_array = not draw_map_array
            
            if event.key == pygame.K_r:
                new_map = [[Tile(row, column, map.tileset) for column in range(map.columns)] for row in range(map.rows)]
                new_map_image = pygame.Surface((0, 0))
                error_tiles = []

                generate_map = True

    keyboard = pygame.key.get_pressed()

    if keyboard[pygame.K_LEFT]:
        scroll[0] += scrol_speed
    
    if keyboard[pygame.K_RIGHT]:
        scroll[0] -= scrol_speed

    if keyboard[pygame.K_UP]:
        scroll[1] += scrol_speed

    if keyboard[pygame.K_DOWN]:
        scroll[1] -= scrol_speed
    
    if generate_map and (next_tile := Generator.find_next_tile(new_map, map.tileset)) != None:
        current_row = next_tile[0]
        current_column = next_tile[1]
        Generator.collapse_tile(new_map, current_row, current_column)

        new_map, error_tiles = Generator.propagate(map, new_map, error_tiles, current_row, current_column)
    elif generate_map:
        generate_map = False
        new_map_image = const.surfaces_to_image(len(new_map) * const.TILE_SIZE, len(new_map[0]) * const.TILE_SIZE, Map.map_to_surfaces(new_map, map.tileset))
        print("New Map Generated.")

    redrawGameWindow()
pygame.quit()