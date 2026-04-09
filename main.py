import pygame
import sys
import random
import math
from settings import *
from player import Player
from coin import Coin
from tile import Tile, generate_tiles
from camera import Camera


#Initialize pygame
pygame.init()

#Background music -------
pygame.mixer.init()

#Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")
clock = pygame.time.Clock()

# Load assets
bg = pygame.image.load("assets/sky.png").convert()
ground_img = pygame.image.load("assets/ground.png").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (WIDTH, 40))
ground_rect = ground_img.get_rect(topleft=(0, HEIGHT - 40))

# Music ---------
pygame.mixer.music.load("assets/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)

#Coin sound -------------
coin_sound = pygame.mixer.Sound("assets/coin.wav")
coin_sound.set_volume(0.6)

#Game states ----------
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Fonts
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 72)

#Start button ---------
start_button = pygame.Rect(0, 0, 200, 60)
restart_button = pygame.Rect(0, 0, 200, 60)
start_button.center = (WIDTH // 2, HEIGHT // 2)
restart_button.center = (WIDTH // 2, HEIGHT // 2 + 50)

def reset_game():
    global tiles, coins, player, camera, score
    
    tiles = generate_tiles()
    start_tile = Tile(100, 400, "platform1.png")
    tiles.insert(0, start_tile)

    coins = [Coin(tile) for tile in tiles]

    player.rect.midbottom = start_tile.rect.midtop
    player.vel_y = 0

    camera.offset_x = 0
    score = 0

#Creating world ------------
tiles = generate_tiles()

#Start platform -----------
start_tile = Tile(100, 400, "platform1.png")  # starting platform
tiles.insert(0, start_tile)  # add it at beginning

coins = [Coin(tile) for tile in tiles]

player = Player()
player.rect.midbottom = start_tile.rect.midtop

camera = Camera(WIDTH, HEIGHT)

score = 0

#Game Loop --------------
running = True
while running:
    dt = clock.tick(FPS) / 1000
    mouse_pos = pygame.mouse.get_pos(   )

    #Events -----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_state = PLAYING
                    pygame.mixer.music.play(-1, fade_ms = 1000) #-- music starts
        
        elif game_state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    game_state = PLAYING
                    reset_game()
                    pygame.mixer.music.play(-1, fade_ms=500)
                    pygame.event.clear()


    #Update Player ----------
    if game_state == PLAYING:
        player.update(dt)
        player.on_ground = False

        for tile in tiles:
            if player.rect.colliderect(tile.rect):
                if player.vel_y > 0:
                    player.rect.bottom = tile.rect.top
                    player.vel_y = 0      
                    player.on_ground = True
                    
    #Ground collision
    player_screen_rect = player.rect.copy()
    player_screen_rect.x -= camera.offset_x


    # Ground collision -> Game over
    if player_screen_rect.bottom >= ground_rect.top:
        if player.falling:
            player.fall_sound.play()
            player.falling = False
        game_state = GAME_OVER
        pygame.mixer.music.fadeout(1000)

    #Coin Update --------------
    for coin in coins[:]:
        coin.update(dt)
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)
            score += 1
            coin_sound.play()

    # Camera update
        camera.update(player.rect)

    # Generate new tiles
        farthest_x = max([tile.rect.x for tile in tiles])
        if farthest_x - player.rect.x < WIDTH:
            x = farthest_x + random.randint(120, 250)
            y = random.randint(250, 450)
            variant = random.choice(["platform1.png", "platform2.png", "platform3.png"])
            new_tile = Tile(x, y, variant)
            tiles.append(new_tile)
            coins.append(Coin(new_tile))

        # Remove old tiles/coins
        tiles = [tile for tile in tiles if tile.rect.right > player.rect.x - WIDTH]
        coins = [coin for coin in coins if coin.rect.right > player.rect.x - WIDTH]

    # DRAW
    screen.fill((0, 0, 0))  # prevents leftover UI
    screen.blit(bg, (0, 0))
    screen.blit(ground_img, (0, ground_rect.y))

    if game_state == MENU:
        title = font_big.render("Coin Platformer", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(title, (WIDTH//2 - 200, 150))

        #Animated button ------------
        hover = start_button.collidepoint(mouse_pos)
        color = (4, 176, 4) if hover else (0, 200, 0)
        scale = 1.05 if hover else 1
        
        btn_rect = pygame.Rect(0, 0,
            int(start_button.width * scale),
            int(start_button.height * scale)
        )
        btn_rect.center = start_button.center

        pygame.draw.rect(screen, color, btn_rect, border_radius=25)

        text = font.render("START", True, (0, 0, 0))
        text_rect = text.get_rect(center=btn_rect.center)
        screen.blit(text, text_rect)


    elif game_state == PLAYING:

        for tile in tiles:
            screen.blit(tile.image, (tile.rect.x - camera.offset_x, tile.rect.y))

        for coin in coins:
            coin.draw(screen, camera.offset_x)

        player.draw(screen, camera.offset_x)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    elif game_state == GAME_OVER:
        # Dark overlay ----------
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        #Floating animation -------------
        y_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10

        gameover_text = font_big.render("GAME OVER !", True, (255, 50, 50))
        gameover_rect = gameover_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + y_offset))
        screen.blit(gameover_text, gameover_rect)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(score_text, score_rect)

        #Animated restart button -------------
        hover = restart_button.collidepoint(mouse_pos)
        color = (255, 255, 0) if restart_button.collidepoint(mouse_pos) else (200, 200, 0)
        scale = 1.1 if restart_button.collidepoint(mouse_pos) else 1
        btn_w = int(restart_button.width * scale)
        btn_h = int(restart_button.height * scale)
        btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
        btn_rect.center = restart_button.center
        pygame.draw.rect(screen, color, btn_rect, border_radius=20)
        text = font.render("RESTART", True, (0, 0, 0))
        text_rect = text.get_rect(center=btn_rect.center)
        screen.blit(text, text_rect)

    pygame.display.update()

pygame.quit()
sys.exit()