import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

START_ENEMIES = 10
START_LEVEL = 1

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')

BORDER_RIGHT = pygame.Rect(WIDTH, 0, 1, HEIGHT)
BORDER_LEFT = pygame.Rect(0, -1, 1, HEIGHT)

BATTLESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'battleship2.png'))
BATTLESHIP = pygame.transform.scale(BATTLESHIP_IMAGE, (50, 50))

ICON_IMAGE = pygame.image.load(os.path.join('Assets', 'ufo.png'))
pygame.display.set_icon(ICON_IMAGE)

ENEMY_IMAGE = pygame.image.load(os.path.join('Assets', 'alien.png'))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (50, 50))

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_FIRE_SOUND.set_volume(0.1)

LEVEL_FONT = pygame.font.SysFont('calibri', 40)
WINNER_FONT = pygame.font.SysFont('calibri', 100)


def draw_window(character, bullets, enemies, level):
    WIN.fill(BLACK)
    WIN.blit(BATTLESHIP, (character.x, character.y))
    pygame.draw.rect(WIN, BLACK, BORDER_RIGHT)
    pygame.draw.rect(WIN, BLACK, BORDER_LEFT)

    level_now = LEVEL_FONT.render('Level: ' + str(level), 1, WHITE)
    WIN.blit(level_now, (10, 10))

    for bullet in bullets:
        pygame.draw.rect(WIN, CYAN, bullet)
    
    for enemy in enemies:
        WIN.blit(ENEMY, (enemy.x, enemy.y))

    pygame.display.update()


def handle_movement(keys_pressed, character):
    if keys_pressed[pygame.K_LEFT] and character.x - VEL > 0: # LEFT
        character.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and character.x + VEL < WIDTH - character.width - 15: # RIGHT
        character.x += VEL


def handle_bullets(bullets, enemies):
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        if bullet.y <= 0:
            bullets.remove(bullet)
        for enemy in enemies:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)


ENEMY_VEL = 3
def move_enemies(enemies):
    global ENEMY_VEL
    for enemy in enemies:
        if enemy.x + enemy.width + ENEMY_VEL >= WIDTH:
            for e in enemies:
                e.y += 50
            ENEMY_VEL = -3
        elif enemy.x + ENEMY_VEL <= 0:
            for e in enemies:
                e.y += 50
            ENEMY_VEL = 3

        enemy.x += ENEMY_VEL


def create_enemies(qtd):
    enemies = []
    y = 10
    linha = 10
    for _ in range(qtd//10):
        for i in range(10, WIDTH - 40, 90):
            if len(enemies) < qtd and len(enemies) < linha:
                enemy = pygame.Rect(i, y, 40, 40)
                enemies.append(enemy)
        y += 50
        linha += 10
    
    return enemies


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main(qtd_enemies, level):
    character = pygame.Rect(WIDTH//2 - 15, HEIGHT - 65, 30, 30)

    bullets = []
    enemies = create_enemies(qtd_enemies)

    run = True
    restart = False
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(character.x + character.width//2 + 8, character.y, 4, 10)
                    bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, character)
        handle_bullets(bullets, enemies)

        draw_window(character, bullets, enemies, level)

        move_enemies(enemies)
        for enemy in enemies:
            if enemy.y + enemy.height >= character.y:
                draw_winner('YOU LOSE!')
                run = False
                restart = True
                break
        
        if len(enemies) == 0:
            draw_winner('YOU WIN!')
            main(qtd_enemies + 10, level + 1)

    if restart:
        main(START_ENEMIES, START_LEVEL)

    pygame.quit()


main(START_ENEMIES, START_LEVEL)
