import pygame
import time
import random

#initialize
pygame.init()

#colors
white = (255,255,255)   #snake
black = (0,0,0)         #bg
orange = (255, 165, 0)  #food
red = (255, 0, 0)       #score

#screen w & h
width = 600
height = 400
game_display = pygame.display.set_mode((width,  height))     #width & height

clock = pygame.time.Clock()

pygame.display.set_caption('Snake Game')

snake_size = 10
snake_speed = 15

message_font = pygame.font.SysFont('Ubuntu', 30)
score_font = pygame.font.SysFont('Ubuntu', 25)
#time.sleep(5)


#score
def print_score(score):
    text = score_font.render('Score:' +str(score), True, orange)
    game_display.blit(text, [0, 0])


def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, white, [pixel[0], pixel[1], snake_size, snake_size])


def run_game():
    #initially
    game_over = False
    game_close = False

    #starting pos of snake
    x =  width / 2
    y = height / 2

    x_speed = 0
    y_speed = 0

    #snake blocks after eating
    snake_pixels = []
    snake_length = 1    #initially

    food_x = round(random.randrange(0 , width - snake_size) / 10.0 ) * 10.0
    food_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0


    while not game_over:

        while game_close:
            game_display.fill(black)
            game_over_message = message_font.render('Game Over', True, red)
            game_display.blit(game_over_message)
            print_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:                 # press 1 for quit
                        game_over = True
                        game_close =False
                    if event.key == pygame.K_2:                 #press 2 to restart
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_size                   # -ve because we move to the left & y axis doesnt change moving vertically
                    y_speed = 0
                if event.key == pygame.K_RIGHT:
                    x_speed = snake_size                    #moving right it becomes +ve
                    y_speed = 0
                if event.key == pygame.K_UP:
                    x_speed = 0
                    y_speed = -snake_size
                if event.key ==pygame.K_DOWN:
                    x_speed = 0
                    y_speed = snake_size

        #if snake goes out the border
        if x >= width or x < 0 or  y >= height or y < 0:
            game_close = True

        #speed after click
        x += x_speed
        y += y_speed


        #draw into game window
        game_display.fill(black)
        pygame.draw.rect(game_display, orange, [food_x, food_y, snake_size, snake_size])

        #add a snake while also removing its tail but not when its eating
        #movement deletion of tail
        snake_pixels.append([x,y])
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]
        #if snake runs into itself
        for pixel in snake_pixels[:-1]:
            if pixel == [x,y]:
                game_close = True

        draw_snake(snake_size, snake_pixels)
        print_score(snake_length - 1)

        pygame.display.update()

        #snake eats food
        if x == food_x and  y == food_y:
            food_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

run_game()












