import pygame
import random
from time import sleep

pygame.init()
pygame.mixer.init()

background_music = pygame.mixer.music.load("background_sound.mp3")
background_music = pygame.mixer.music.play(-1)

coin_sound = pygame.mixer.Sound("coin_sound.mp3")
coin_sound.set_volume(0.5)

win_sound = pygame.mixer.Sound("win_sound.mp3")

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Pygame")

clock = pygame.time.Clock()

BACKGROUND_COLOR = (255, 255, 255)

background_img = pygame.image.load("Background.png")
background_img = pygame.transform.scale(background_img, (800, 600))

player_img = pygame.image.load("slime.png")
player_img = pygame.transform.scale(player_img, (80, 80))

win_scenerio = pygame.image.load("WINGS.png")
win_scenerio = pygame.transform.scale(win_scenerio, (800, 600))

level_2_scenerio = pygame.image.load("level2.png")
level_2_scenerio = pygame.transform.scale(level_2_scenerio, (800, 600))

coin_png = pygame.image.load("coin.png")
coin = pygame.Rect(450, 400, 80, 80)
coin_png = pygame.transform.scale(coin_png, (100, 100))

score = 0
font = pygame.font.SysFont(None, 30)

coin_visible = True

player = pygame.Rect(50, 50, 40, 40)
player_speed = 5

win_platform = pygame.Rect(500000, 500000, 50, 50)

walls = [
    pygame.Rect(200, 200, 20, 200),
    pygame.Rect(400, 200, 150, 20),
    pygame.Rect(200, 400, 200, 20)
]

old_x = player.x
old_y = player.y

red = random.randint(0, 255)
green = random.randint(0, 255)
blue = random.randint(0, 255)

running = True
win1 = False
level_2 = False
show_level2_screen = False
level2_screen_shown = False
level2_start_time = None

while running:
    clock.tick(60)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_s]:
        player.y += player_speed

    # საზღვრების კონტროლი
    if player.x < 0:
        player.x = 0
    if player.y < 0:
        player.y = 0
    if player.x + player.width > WIDTH:
        player.x = WIDTH - player.width
    if player.y + player.height > HEIGHT:
        player.y = HEIGHT - player.height

    # კედლებთან შეჯახება
    for wall in walls:
        if player.colliderect(wall):
            player.x = old_x
            player.y = old_y
            score = 0

    # მონეტა
    if player.colliderect(coin):
        score += 1
        coin.x = random.randint(50, 700)
        coin.y = random.randint(50, 500)
        coin_sound.play()

    for wall in walls:
        if coin.colliderect(wall):
            coin.x = random.randint(50, 700)
            coin.y = random.randint(50, 500)

    if score >= 3:
        win_platform = pygame.Rect(700, 200, 70, 70)
    else:
        win_platform = pygame.Rect(50000, 400, 80, 80)

    if player.colliderect(win_platform) and not win1:
        win1 = True
        win_sound.play()
        show_level2_screen = True
        level2_start_time = pygame.time.get_ticks()  # დროის დამახსოვრება

    # მეორე ლეველის ფოტოს ჩვენება
    if show_level2_screen and not level2_screen_shown:
        screen.blit(level_2_scenerio, (0, 0))
        pygame.display.flip()
        pygame.time.delay(3000)  # აჩვენებს 3 წამით
        level2_screen_shown = True
        level_2 = True
        # მეორე დონისთვის მოთამაშის პოზიცია, რომ შეიცვალოს
        player.x = 50
        player.y = 50
        score = 0
        coin.x = random.randint(50, 700)
        coin.y = random.randint(50, 500)
        walls = [
            pygame.Rect(150, 0, 20, 500),
            pygame.Rect(300, 200, 20, 800),
            pygame.Rect(450, 0, 20, 500),
            pygame.Rect(600, 200, 20, 800),
            #pygame.Rect(400, 400, 200, 20),
            #pygame.Rect(400, 400, 200, 20),
        ]


    screen.fill(BACKGROUND_COLOR)
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, (player.x, player.y))
    screen.blit(score_text, (50, 50))

    if coin_visible:
        screen.blit(coin_png, (coin.x, coin.y))

        for wall in walls:
            pygame.draw.rect(screen,(red, green, blue), wall)

        pygame.draw.rect(screen, (90, 87, 35), win_platform)

    pygame.display.flip()

old_x = player.x
old_y = player.y

pygame.quit()