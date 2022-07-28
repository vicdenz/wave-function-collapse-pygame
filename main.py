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
running = True

map = Map(20, 20, const.SAMPLE_IMAGE_PATH)
map.parse_tileset()
map.calculate_constraints()

new_map = map.generate_map()

def redrawGameWindow():
    screen.fill((255, 255, 255))

    map.draw_map(screen, new_map, scroll)
    # map.draw_map(screen, map.sample_map, [20*const.TILE_SIZE+scroll[0], scroll[1]])

    pygame.display.update()

scroll = [0, 0]
scrol_speed = 5
while running:
    clock.tick(const.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                running = False

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