import pygame
import const
from heuristic import Heuristic

pygame.display.set_caption("Wave Function Collapse - Terrain Generation")
ROWS, COLUMNS = 20, 15
TILE_SIZE = 32
WIDTH, HEIGHT = ROWS * TILE_SIZE, COLUMNS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

heuristic = Heuristic(20, 15, const.SAMPLE_IMAGE_PATH)
heuristic.parse_tileset()
heuristic.create_map()

def redrawGameWindow():
    screen.fill((255, 255, 255))

    heuristic.draw_map(screen)

    pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_QUIT:
                running = False
    
    redrawGameWindow()
pygame.quit()