import pygame

pygame.display.set_caption("Wave Function Collapse - Terrain Generation")
ROWS, COLUMNS = 20, 15
TILE_SIZE = 32
WIDTH, HEIGHT = ROWS * TILE_SIZE, COLUMNS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

def redrawGameWindow():
    screen.fill((255, 255, 255))

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