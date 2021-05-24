import turtle as t

#score variables
playerAscore = 0
playerBscore =0

#create window part
window = t.Screen()
window.title('Pong')
window.setup(width = 800, height = 600)
window.bgcolor('black')
#speed up's the game
window.tracer(0)

#creating left paddle
paddle_left = t.Turtle()
paddle_left.speed(0)
paddle_left.shape('square')
paddle_left.color('red')
paddle_left.shapesize(stretch_wid=5,stretch_len=1)
paddle_left.penup()
paddle_left.goto(-350,0)

#right
paddle_right = t.Turtle()
paddle_right.speed(0)
paddle_right.shape('square')
paddle_right.shapesize(stretch_wid=5,stretch_len=1)
paddle_right.color('red')
paddle_right.penup()
paddle_right.goto(350,0)


#creating a ball
ball = t.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('yellow')
ball.penup()
ball.goto(0,0)
ballxdirection = 0.25   # Setting up the pixels for the ball movement.
ballydirection = 0.25


#creating pen for scorecard
pen = t.Turtle()
pen.speed(0)
pen.color('skyblue')
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Player A: 0          Player B: 0 ",align="center",font=('Monaco',24,"normal"))


#moving left paddle
def leftpaddleup():
    y = paddle_left.ycor()
    y = y + 15
    paddle_left.sety(y)

def leftpaddledown():
    y =paddle_left.ycor()
    y = y - 15
    paddle_left.sety(y)

#moving right paddle
def rightpaddleup():
    y = paddle_right.ycor()
    y = y + 15
    paddle_right.sety(y)

def rightpaddledown():
    y = paddle_right.ycor()
    y = y - 15
    paddle_right.sety(y)

#assign keys to play the game
window.listen()
window.onkeypress(leftpaddleup, 'w')
window.onkeyrelease(leftpaddleup, 'w')
window.onkeypress(leftpaddledown, 's')
window.onkeypress(rightpaddleup, 'Up')
window.onkeypress(rightpaddledown, 'Down')


while True:
    #This methods is mandatory to run any game
    window.update()

    #move the ball
    ball.sety(ball.ycor() + ballydirection)
    ball.setx(ball.xcor() + ballxdirection)

    #create border for the ball
    #y axis
    if ball.ycor() > 290:
        ball.sety(290)
        ballydirection = ballydirection * -1  #after hitting top ball moves downward(-1)

    if ball.ycor() < -290:
        ball.sety(-290)
        ballydirection = ballydirection * -1    #-1 so that ball goes opposite side on hitting the border

    #x axis
    if ball.xcor() > 390:
        ball.goto(0,0)
        ballxdirection = ballxdirection
        ball.penup()
        playerAscore += 1
        pen.clear()
        pen.write("Player A:{}      Player: {}".format(playerAscore, playerBscore), align = 'center', font = ('Shanti',  24, 'normal'))

    if ball.xcor() < -390:
        ball.goto(0,0)
        ballxdirection = ballxdirection
        ball.penup()
        playerBscore += 1
        pen.clear()
        pen.write("Player A:{}      Player: {}".format(playerAscore, playerBscore), align = 'center', font = ('Shanti',  24, 'normal'))


    #handling the collisions
    if (ball.xcor() > 340) and (ball.ycor()< 350) and (ball.ycor() < paddle_right.ycor() + 40 and ball.ycor() > paddle_right.ycor() -40):
        ball.setx(340)
        ballxdirection = ballxdirection * -1


    if (ball.xcor() < -340) and (ball.xcor() > -350) and (ball.ycor() < paddle_left.ycor() +40 and ball.ycor() > paddle_left.ycor() -40):
        ball.setx(-340)
        ballxdirection  = ballxdirection * -1








