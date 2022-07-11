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

heuristic = Heuristic(20, 20, const.SAMPLE_IMAGE_PATH)
heuristic.parse_tileset()
heuristic.calculate_constraints()

new_map = heuristic.generate_map()

def redrawGameWindow():
    screen.fill((255, 255, 255))

    heuristic.draw_map(screen, new_map, scroll)
    # heuristic.draw_map(screen, heuristic.sample_map, [10*const.TILE_SIZE, 0])

    pygame.display.update()

scroll = [0, 0]
scrol_speed = 5
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                running = False

    keyboard = pygame.key.get_pressed()

    if keyboard[pygame.K_LEFT]:
        scroll[0] -= scrol_speed
    
    if keyboard[pygame.K_RIGHT]:
        scroll[0] += scrol_speed

    if keyboard[pygame.K_UP]:
        scroll[1] -= scrol_speed

    if keyboard[pygame.K_DOWN]:
        scroll[1] += scrol_speed
    
    redrawGameWindow()
pygame.quit()