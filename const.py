import pygame

SAMPLE_IMAGE_PATH = "images/sample_image.png"

TILE_SIZE = 32

def load_image(path):
    image = pygame.image.load(path)

    return pygame.transform.scale(image, (image.get_width(), image.get_height()))