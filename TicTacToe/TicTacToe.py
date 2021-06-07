import pygame
from pygame.locals import  *

pygame.init()

screen_width = 300
screen_height = 300

#game variables
markers = []
clicked = False
pos = []
player = 1
winner = 0
game_over = False

#color
green = (0, 255, 0)
red = (255, 0, 0)

#font
font = pygame.font.SysFont(None, 40)

#create play again rectangle
again_rect = Rect(screen_width // 2 -80, screen_height // 2, 160, 50)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('TicTacToe')


def draw_grid():
    bg = (255, 255, 200)
    grid = (50, 50, 50)
    screen.fill(bg)
    for x in range(1, 3):
        pygame.draw.line(screen, grid, (0, x * 100), (screen_width, x * 100), 6)               #horizontal lines & 6 is line width
        pygame.draw.line(screen, grid, (x * 100, 0), (x * 100, screen_height), 6)              #vertical lines


for x in range(3):
    row = [0] * 3
    markers.append(row)


def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:              #player X
                pygame.draw.line(screen, green, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), 6)
                pygame.draw.line(screen, green, (x_pos * 100 + 15, y_pos * 100 + 85), (x_pos * 100 + 85, y_pos * 100 + 15), 6)
            if y == -1:             #player O
                pygame.draw.circle(screen, red, (x_pos * 100 + 50, y_pos * 100 + 50), 38, 6)            #radius = 38px
            y_pos += 1
        x_pos += 1


def check_win():

    global winner
    global game_over

    y_pos = 0
    for x in markers:
        #check column
        if sum(x) == 3:
            winner = 1                                                                                  #Player 1(1)
            game_over = True
        if sum(x) == -3:
            winner = 2                                                                                  #Player 2(-1)
            game_over = True

        #check rows
        if markers[0][y_pos] + markers[1][y_pos] + markers [2][y_pos] == 3:
            winner = 1
            game_over = True
        if markers[0][y_pos] + markers [1][y_pos] + markers [2][y_pos] == -3:
            winner = 2
            game_over = True
        y_pos += 1

    #check diagonal
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[0][2] + markers[1][1] + markers[2][0] == 3:
        winner = 1
        game_over = True
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[0][2] + markers[1][1] + markers[2][0] == -3:
        winner = 2
        game_over = True


def draw_winner(winner):
    win_text = 'Player ' + str(winner) + ' won!!'
    #convert text to image
    win_img = font.render(win_text, True, (0, 0, 255))
    #drawing rect behind the winner display
    pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 50, 200, 35))
    screen.blit(win_img, (screen_width // 2 - 100, screen_height // 2 - 50))

    #play again
    again_text = 'Play Again?'
    #convert to img
    again_img = font.render(again_text, True, (0, 0, 255))
    pygame.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))


run = True
while run:
    draw_grid()
    draw_markers()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_over == False:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                cell_x = pos[0]
                cell_y = pos [1]
                if markers[cell_x // 100][cell_y // 100] == 0:          #not clicked
                    markers[cell_x // 100][cell_y // 100] = player      #if 0 then change it to player X or O
                    player *= -1                                        #players X & O are 1 & -1
                    check_win()

    if game_over == True:
        draw_winner(winner)
        #check for click if user clicked on Play Again
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                #reset variables
                markers = []
                pos = []
                player = 1
                winner = 0
                game_over = False
                for x in range(3):
                    row = [0] * 3
                    markers.append(row)


    pygame.display.update()



pygame.quit()