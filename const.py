import pygame

SAMPLE_IMAGE_PATH = "images/sample_image.png"

FPS = 60

TILE_SIZE = 32

def image_to_surface(image):
    # Calculate mode, size and data
    mode = image.mode
    size = image.size
    data = image.tobytes()

    return pygame.image.fromstring(data, size, mode)

def surface_to_image(width, height, surfaces):
    surface = pygame.Surface((width, height))
    surface.fill((255, 255, 255))

    row_size = height/len(surfaces)
    column_size = width/len(surfaces[0])
    for row in range(len(surfaces)):
        for column in range(len(surfaces[row])):
            if surfaces[row][column] != None:
                surface.blit(surfaces[row][column], (column_size*column, row_size*row))
    
    return surface

def load_image(path):
    image = pygame.image.load(path)

    return pygame.transform.scale(image, (image.get_width(), image.get_height()))