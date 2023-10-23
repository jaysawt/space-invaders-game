from turtle import Turtle

HOME_POSITION = (0, -300)
MOVE_DISTANCE = 8


class Earth(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('player_earth/earth.gif')
        self.goto(HOME_POSITION)
        self.move = MOVE_DISTANCE

    def rotate(self):
        self.goto(self.xcor() - self.move, self.ycor())
        self.bounce()

    def bounce(self):
        if self.xcor() <= -395 or self.xcor() >= 395:
            self.move *= -1


class EarthLife:
    def __init__(self):
        self.lives = []
        self.move = MOVE_DISTANCE
        self.create_lives()

    def create_lives(self):
        for i in range(3):
            life = Turtle()
            life.penup()
            life.shape('player_earth/life.gif')
            life.goto(-22+22*i, -340)
            self.lives.append(life)

    def move_life(self):
        for life in self.lives:
            life.goto(life.xcor() - self.move, life.ycor())
        if self.lives[0].xcor() <= -420 or self.lives[0].xcor() >= 378:   # by tweaking the desired affect was achieved
            self.bounce()

    def bounce(self):
        self.move *= - 1
        