from PIL import Image, ImageChops
import pygame
import const

class Heuristic:
    def __init__(self, rows, columns, sample_image_path):
        self.rows = rows
        self.columns = columns
        self.sample_image = Image.open(sample_image_path).convert('RGB')
        self.tileset = []
        self.sample_map = [[0 for c in range(self.columns)] for r in range(self.rows)]

    def unique_tile(self, image):
        if (len(self.tileset) == 0):
            return -1
        
        for index, tile in enumerate(self.tileset):
            if list(tile.getdata()) == list(image.getdata()):
                return index
        
        return -1

    # read through the sample image and creates the tileset
    def parse_tileset(self):
        for row in range(self.rows):
            for column in range(self.columns):
                image = self.sample_image.crop((row*const.TILE_SIZE, column*const.TILE_SIZE, (row+1)*const.TILE_SIZE, (column+1)*const.TILE_SIZE))
                if self.unique_tile(image) == -1:
                    self.tileset.append(image)
    
    # read through the sample image and maps each tile to the index of the tileset
    def create_map(self):
        for row in range(self.rows):
            for column in range(self.columns):
                image = self.sample_image.crop((row*const.TILE_SIZE, column*const.TILE_SIZE, (row+1)*const.TILE_SIZE, (column+1)*const.TILE_SIZE))

                self.sample_map[row][column] = self.unique_tile(image)
    
    def draw_map(self, screen):
        for r, row in enumerate(self.sample_map):
            for c, tile in enumerate(row):
                image = self.tileset[tile]

                # Calculate mode, size and data
                mode = image.mode
                size = image.size
                data = image.tobytes()

                surface = pygame.image.fromstring(data, size, mode)

                screen.blit(surface, (r*const.TILE_SIZE, c*const.TILE_SIZE))