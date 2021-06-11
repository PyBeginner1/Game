import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width,screen_height ))
pygame.display.set_caption('Final Fantasy')


#game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion =False
potion_effect = 15
clicked = False
game_over = 0           #-1 player(knight) lost, 1 is player win


#define font
font = pygame.font.SysFont('Times New Roman', 26)

#define color
red = (255, 0, 0)
green = (0, 255, 0)


#load images
#background
bg_img = pygame.image.load('Img/Icons/background.png').convert_alpha()
#panel
panel_img = pygame.image.load('Img/Icons/panel.png').convert_alpha()
#sword
sword_img = pygame.image.load('Img/Icons/sword.png').convert_alpha()
#potion
potion_img  = pygame.image.load('Img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('Img/Icons/restart.png').convert_alpha()
#victory & defeat imahes
victory_img = pygame.image.load('Img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('Img/Icons/defeat.png').convert_alpha()



#converting text to img
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for drawing background
def draw_bg():
    screen.blit(bg_img, (0,0))

def draw_panel():
    screen.blit(panel_img, (0,400))
    #draw knights stats
    draw_text(f'{knight.name} HP : {knight.hp}', font, red, 100, screen_height - bottom_panel + 30)
    #draw bandits stats
    for count, i in enumerate(bandit_list):
        draw_text(f'{i.name} HP : {i.hp}', font, red, 550, (screen_height - bottom_panel + 30) + count * 60)


#fight class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp =max_hp
        self.strength = strength
        self.start_potion = potions
        self.potions = potions
        self.alive = True
        self.animations_list = []
        self.frame_index = 0
        self.action = 0                                                           #0 = Idle, 1 = Attack, 2 = Hurt, 3 = Dead
        self.update_time = pygame.time.get_ticks()
        #load Idle Images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animations_list.append(temp_list)
        #load attack Images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animations_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animations_list.append(temp_list)
        #load death images
        temp_list = []
        for i in range(9):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animations_list.append(temp_list)
        self.image = self.animations_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        animations_cooldown = 100
        #handle animation
        self.image = self.animations_list[self.action][self.frame_index]
        #checking if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animations_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation has run out then reset to 0
        if self.frame_index >= len(self.animations_list[self.action]):
            if self.action == 3:                                #dead
                self.frame_index = len(self.animations_list[self.action]) - 1
            else:
                self.idle()


    def idle(self):
        # set to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        #se to attack animation
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #run enemy hurt animation
        target.hurt()
        #check if target is dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def hurt(self):
        #set to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #set to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def reset(self):
        self.alive = True
        self.potions = self.start_potion
        self.action = 0
        self.hp =self.max_hp
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0


    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):                                     #update hp after every single hit
        #update new health
        self.hp = hp
        #calcualte health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))                            #total health
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))                  #new health after getting hit


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #move text upwards
        self.rect.y -= 0.5
        #delete text after few secs
        self.counter += 1
        if self.counter > 80:
            self.kill()



damage_text_group = pygame.sprite.Group()

knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 15, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 15, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 75, bandit2.hp, bandit2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel +70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)


run = True
while run:

    clock.tick(fps)

    #draw backgriund
    draw_bg()
    draw_panel()

    #draw health bar
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)


    #draw fighters
    knight.draw()
    knight.update()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    #draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #control player actions
    #reset actions
    action = False
    potion = False
    target = None
    #make mouse visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide the mouse
            pygame.mouse.set_visible(False)
            #show sword in mouses place
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:                         #click on the bandit to hurt
                attack = True
                target = bandit_list[count]
    if potion_button.draw():
        potion = True
    #show number of potions
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel +70)


    if game_over == 0:
        #knight action
        if knight.alive == True:
            if current_fighter == 1:                     #1 is knight
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #attack
                    if attack == True and target != None:
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #potion
                    if potion == True:
                        if knight.potions > 0:
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1                      #game lost


        #enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #cgheck if bandit needs to heal
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            #check if potions health exceeds the max hp
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        else:
                            #attack
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1            #if bandit not alive set to next bandit

        #if all the fighter had a turn then reset it back to the first
        if current_fighter > total_fighters:
            current_fighter = 1

    #check if all bandits are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1                       #game won

    #check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img,(250, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()


pygame.quit()