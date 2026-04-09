import pygame
import random

class Tile:
    def __init__(self, x, y, image_file):
        # Load and scale the chosen tile variant
        self.image = pygame.image.load(f"assets/{image_file}").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 30))  # smaller tile
        self.rect = self.image.get_rect(topleft=(x, y))

def generate_tiles(num_tiles=12):
    tiles = []
    x = 200  # starting x position

    for i in range(num_tiles):
        x += random.randint(120, 250)  # horizontal gap
        y = random.randint(250, 450)   # random height

        # Randomly choose a tile variant
        variant = random.choice(["platform1.png", "platform2.png", "platform3.png"])
        tiles.append(Tile(x, y, variant))

    return tiles