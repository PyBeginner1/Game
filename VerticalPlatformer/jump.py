import pygame
import random

#initialise
pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jump')

clock = pygame.time.Clock()
FPS = 60

#game variables
SCROLL_THRESH = 200         #trigger vertical scrolling when players rectangle touches it
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

#define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

#define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

#load images
bg_img = pygame.image.load('Assets/bg.png').convert_alpha()
jump_img = pygame.image.load('Assets/jump.png').convert_alpha()
platform_img = pygame.image.load('Assets/wood.png').convert_alpha()

#function for displaying text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)

#function for drawing background
def draw_bg(bg_scroll):
    screen.blit(bg_img, (0, 0 + bg_scroll))
    screen.blit(bg_img, (0, -600 + bg_scroll))

#player
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jump_img,(45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        #reset variables
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx -= 10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        #gravity
        self.vel_y += GRAVITY
        dy = self.vel_y

        #ensure player doesnt go off edge
        if self.rect.left + dx < 0:
            dx = -self.rect.x
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #check collision with platform
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        #check if players has reaches top of screen
        if self.rect.top <= SCROLL_THRESH:
            #scroll only when player is jumping
            if self.vel_y < 0:
                scroll = -dy


        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)

#platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #update platform vertical pos
        self.rect.y += scroll

        #check if platform has gone off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

jumpy = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()

#create starting platforms
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)


#game loop
run = True
while run:
    clock.tick(FPS)

    if game_over == False:

        scroll = jumpy.move()

        #draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(scroll)

        #generate platforms
        if len(platform_group) <  MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)

        #update platform
        platform_group.update(scroll)

        #update score
        if scroll > 0:
            score += scroll

        #draw images
        platform_group.draw(screen)
        jumpy.draw()

        draw_panel()

        #check game over
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True

    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
        draw_text('GAME OVER!', font_big, WHITE, 130, 200)
        draw_text('SCORE:' + str(score), font_big, WHITE, 130, 250)
        draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            #reset variable
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
            #reposition character
            jumpy.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150)
            #reset platform
            platform_group.empty()
            # create starting platforms
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
            platform_group.add(platform)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

pygame.quit()