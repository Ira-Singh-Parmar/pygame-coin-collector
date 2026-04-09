import pygame

class Coin:
    def __init__(self, tile):
        # Load and scale all 7 coin images
        self.images = [pygame.image.load(f"assets/coin{i}.png").convert_alpha() for i in range(1    , 8)]
        self.images = [pygame.transform.scale(img, (20, 20)) for img in self.images]

        # Initial image
        self.index = 0
        self.image = self.images[self.index]
        self.timer = 0

        # Place coin above the platform
        self.rect = self.image.get_rect(center=(tile.rect.centerx, tile.rect.top - 20))

    def update(self, dt):
        # Animate coin using all 7 frames
        self.timer += dt
        if self.timer > 0.1:  # adjust rotation speed here
            self.index = (self.index + 1) % len(self.images)  # use all frames
            self.image = self.images[self.index]
            self.timer = 0

    def draw(self, screen, camera_offset):
        screen.blit(self.image, (self.rect.x - camera_offset, self.rect.y))