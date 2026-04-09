import pygame
from settings import *

class Player:
    def __init__(self):
        # Load only the idle image
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60)) # -- Smaller player
        self.rect = self.image.get_rect(topleft=(100, 100))
        
        # Movement
        self.vel_y = 0
        self.speed = 250
        self.dx = 0
        self.on_ground = False

        #Falling sound
        self.fall_sound = pygame.mixer.Sound("assets/fall.wav")
        self.fall_sound.set_volume(0.6)
        self.falling = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.dx = 0

        # Move left
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx = -self.speed

        # Move right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx = self.speed

        # Jump only if on ground -------------
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -12
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY 
        self.rect.y += self.vel_y


    def update(self, dt):
        self.input()
        self.rect.x += self.dx * dt
        self.apply_gravity()
        
        # Track falling
        if not self.on_ground:
            self.falling = True

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))