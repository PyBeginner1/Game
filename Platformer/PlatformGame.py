import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

#mixer is used to add sound effects
pygame.mixer.init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#frame rate
clock = pygame.time.Clock()
fps = 60

width = 1000
height = 1000

#load images
#create window
screen = pygame.display.set_mode((width, height))
#title
pygame.display.set_caption('Platform Game')

#load sounds
pygame.mixer.music.load('Images/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)          #5000 so that music slowly starts noy immediately after starting the game
coin_fx = pygame.mixer.Sound('Images/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('Images/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('Images/game_over.wav')
game_over_fx.set_volume(0.4)



#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bahaus 93', 30)
#define color
white =(255, 255, 255)
blue = (0, 0, 255)


#define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 1           #start on lvl 1 & then advance to further levels
max_levels = 7
score =0



#images
sun_img = pygame.image.load('Images/sun.png')
bg_img = pygame.image.load('Images/sky.png')
#button
restart_img = pygame.image.load('Images/restart_btn.png')
start_img = pygame.image.load('Images/start_btn.png')
exit_img = pygame.image.load('Images/exit_btn.png')


def draw_text(text, font,text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))



#reset level i.e,. lvl1 to lvl 2 & so on
def reset_level(level):
    player.reset(100, height - 130)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    platform_group.empty()

    if path.exists(
            f'level{level}_data'):  # if the file exists do the following code so that it doent get to lvl 8 which doesnt exist
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world



#restart button after player dies
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over & clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:      #[0] means click event on Left Mouse button
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0]  == 0:
                self.clicked = False

        #draw the button
        screen.blit(self.image, self.rect)
        return action


#player
class Player():
    def __init__(self, x, y):
       self.reset(x,y)

    #to display player
    def update(self, game_over):
        #movement through keys
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_threshold = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped  = False
            if key[pygame.K_LEFT]:
                self.counter += 1
                dx -= 5
                self.direction = -1
            if key[pygame.K_RIGHT]:
                self.counter += 1
                dx += 5
                self.direction = 1
            if key[pygame.K_UP]:
                dy -= 5
            if key[pygame.K_DOWN]:
                dy += 5
            #if key is released reset the guy animation to 0
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:             #right arrow pressed then face right
                    self.image = self.images_right[self.index]
                if self.direction == -1:            #left arrow pressed then face left
                    self.image = self.images_left[self.index]



            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #adding gravity for jump
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy = self.vel_y


            #checking collision at new position
            self.in_air = True
            for tile in world.tile_list:
                #checking for x collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #checking for y collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if the player is below the ground i.e., jumping
                    if self.vel_y < 0:      #in y direction -ve values means jumping & +ve values mean falling
                        dy = tile[1].bottom - self.rect.top     #checking for collision betweem bottom of the block( tile[1].bottom) & top of the player( self.rect.top)
                        self.vel_y = 0
                    elif self.vel_y > 0:                          #falling
                        dy = tile[1].top - self.rect.bottom     #checking for collision betweem top of the block & bottom of player since hes falling
                        self.vel_y = 0
                        self.in_air = False

                # check for collision with enemies
                if pygame.sprite.spritecollide(self, blob_group, False):
                    game_over = -1
                    game_over_fx.play()

                # check for collision with lava
                if pygame.sprite.spritecollide(self, lava_group, False):
                    game_over = -1
                    game_over_fx.play()

                #check collision with exit gate
                if pygame.sprite.spritecollide(self, exit_group, False):
                    game_over = 1


                #check collision with moving platform
                for platform in platform_group:
                    #checking collision in x direction
                    if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx =0
                    #checking for collision in y direction
                    if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        #check if below platform
                        if abs((self.rect.top + dy) - platform.rect.bottom) < 20:
                            self.vel_y = 0
                            dy = platform.rect.bottom - self.rect.top
                        #check if above platform
                        elif abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
                            self.rect.bottom = platform.rect.top - 1
                            self.in_air = False
                            dy = 0

                        #move sideways with the platform
                        if platform.move_x != 0:
                            self.rect.x += platform.move_direction



            #new player co-ordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, blue, (width // 2) - 200, height //2)
            if self.rect.y > 200:
                self.rect.y -= 5

        #blit to draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):  # 4 pics--->4 animations so (1,5)
            # load image
            img_right = pygame.image.load(f'Images/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)  # y=true, x=false
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('Images/ghost.png')
        self.image = self.images_right[self.index]
        # rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        # to deny bunny hops
        self.jumped = False
        self.direction = 0  # s.d = 1 if u press RIGHT arrow, -1 if LEFT arrow
        self.in_air = True



class World():
    def __init__(self, data):       #data is world_data
        self.tile_list = []

        #load image -->dirt
        dirt_img = pygame.image.load('Images/dirt.png')
        grass_img = pygame.image.load('Images/grass.png')

        #looping through world_data
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))      #200x200
                    #rectangle
                    img_rect  = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))      #200x200
                    #rectangle
                    img_rect  = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:                                                               #enemy
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)         #+15 to bring the blob down to touch the block
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:                                                               #lava
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + 25, row_count * tile_size + 25)
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size)
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])       #(img, img_rect)


#enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    #movement for enemy
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size //2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.move_x = move_x                                        #platform moves horizontal
        self.move_y = move_y                                        #platform moves vertical

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter *= -1



class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/lava.png')
        self.image = pygame.transform.scale(img,(tile_size, tile_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



player = Player(100, height-130)    #tile_size + player height ---> 50 + 80 = 130
blob_group = pygame.sprite.Group()        #group of enemies
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, 20)
coin_group.add(score_coin)


if path.exists(f'level{level}_data'):               #if the file exists do the following code so that it doent get to lvl 8 which doesnt exist
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

#buttons
restart_button = Button(width // 2 - 50, height // 2 + 100, restart_img)
start_button = Button(width // 2 - 350, height // 2, start_img)
exit_button = Button(width // 2 + 150, height // 2, exit_img)


run = True
while run:
    clock.tick(fps)
    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))

    if main_menu == True:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False


    else:
        world.draw()
        #game is running
        if game_over == 0:
            blob_group.update()
            platform_group.update()
            #update score
            #check if a coiin is collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_fx.play()
                score += 1
            draw_text('X ' +str(score), font_score, white, tile_size - 10, 10 )

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        #if player died
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

        #if player has compeleted the level
        if game_over == 1:
            #reset game & go to next level
            level += 1
            if level <= max_levels:
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!!', font, blue, (width // 2) - 140, height //2)
                #finished all levels & restart game
                if restart_button.draw():
                    level = 1
                    world = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0



        print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #update for blit functions
    pygame.display.update()

pygame.quit()


