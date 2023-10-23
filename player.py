from turtle import Turtle

HOME = (0, -230)
MOVE_DISTANCE = 20


class Player(Turtle):
    def __init__(self):
        super().__init__(shape='square')
        self.penup()
        self.shape('player_earth/rocket.gif')    # 20*50(wxh)
        self.goto(HOME)

    def move_left(self):
        if self.xcor() >= -405:
            self.goto(self.xcor() - MOVE_DISTANCE, self.ycor())

    def move_right(self):
        if self.xcor() <= 405:
            self.goto(self.xcor() + MOVE_DISTANCE, self.ycor())


class PlayerMissile:
    def __init__(self):
        self.bullets = []
        self.fire = 'fire'

    def fire_missile(self, x, y):
        if self.fire == 'fire':
            missile = Turtle()
            missile.left(90)
            missile.penup()
            missile.shape('missile/player_missile.gif')
            missile.goto(x, y + 25)  # h(25)rocket
            self.bullets.append(missile)
            self.fire = 'stop fire'

    def move_missile(self):
        for bullet in self.bullets:
            bullet.forward(10)
