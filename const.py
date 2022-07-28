import pygame

SAMPLE_IMAGE_PATH = "images/small_sample_image.png"

FPS = 60

TILE_SIZE = 32

def image_to_surface(image):
    # Calculate mode, size and data
    mode = image.mode
    size = image.size
    data = image.tobytes()

    return pygame.image.fromstring(data, size, mode)

def load_image(path):
    image = pygame.image.load(path)

    return pygame.transform.scale(image, (image.get_width(), image.get_height()))