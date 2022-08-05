import pygame
import const
from map import Map

pygame.init()

pygame.display.set_caption("Wave Function Collapse - Terrain Generation")
ROWS, COLUMNS = 20, 15
TILE_SIZE = 32
WIDTH, HEIGHT = ROWS * TILE_SIZE, COLUMNS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

map = Map(50, 50, const.SAMPLE_IMAGE_PATH)
map.parse_tileset()
map.calculate_constraints()


new_map, error_tiles = map.generate_map()
new_map_image = const.surface_to_image(len(new_map) * const.TILE_SIZE, len(new_map[0]) * const.TILE_SIZE, map.map_to_surfaces(new_map))

# while error_tiles == []:
#     new_map, error_tiles = map.generate_map()

draw_map_array = False

def redrawGameWindow():
    screen.fill((255, 255, 255))

    if draw_map_array:
        map.draw_map(screen, new_map, scroll)
    else:
        screen.blit(new_map_image, scroll)
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
            
            if event.key == pygame.K_SPACE:
                draw_map_array = not draw_map_array
            
            if event.key == pygame.K_r:
                new_map = map.generate_map()
                new_map_image = const.surface_to_image(len(new_map) * const.TILE_SIZE, len(new_map[0]) * const.TILE_SIZE, map.map_to_surfaces(new_map))

    keyboard = pygame.key.get_pressed()

    if keyboard[pygame.K_LEFT]:
        scroll[0] += scrol_speed
    
    if keyboard[pygame.K_RIGHT]:
        scroll[0] -= scrol_speed

    if keyboard[pygame.K_UP]:
        scroll[1] += scrol_speed

    if keyboard[pygame.K_DOWN]:
        scroll[1] -= scrol_speed
    
    redrawGameWindow()
pygame.quit()