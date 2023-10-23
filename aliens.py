from turtle import Turtle

MOVE_DISTANCE = 8
ALL_MISSILES = []
# general = 20*20 boss = 20*40 soldier = 20 * 26   bullets


class AlienSoldiers:
    def __init__(self):
        self.soldiers = []
        self.move = MOVE_DISTANCE
        self.create_soldiers()
        # setting -x coordinate of soldier from original position
        self.distance_left = [-417, -332, -247, -162, -77, 8, 93, 178, 263, 348]
        # setting +x coordinate of soldier from original position
        self.distance_right = [-353, -268, -183, -98, -13, 72, 157, 242, 327, 412]

    def create_soldiers(self):
        for i in range(10):
            soldier = Turtle()
            soldier.penup()
            soldier.shape('opponent/soldier.gif')
            soldier.goto(-385 + i * 85, 150)
            self.soldiers.append(soldier)

    def soldiers_move(self):
        for soldier in self.soldiers:
            if self.soldiers.index(soldier) == 0:
                self.bounce()
            soldier.goto(soldier.xcor() - self.move, soldier.ycor())

    def bounce(self):
        if self.soldiers[0].xcor() == self.distance_left[0] or self.soldiers[0].xcor() == self.distance_right[0]:
            self.move *= -1


class AlienSoldierMissile(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.shape('missile/soldier_missile.gif')
        self.goto(x, y)
        ALL_MISSILES.append(self)

    def attack(self):
        self.goto(self.xcor(), self.ycor() - MOVE_DISTANCE)


class AlienGenerals:
    def __init__(self):
        self.generals = []
        self.move = MOVE_DISTANCE
        self.create_generals()
        self.distance_left = [-377, -207, -37, 133, 303]
        self.distance_right = [-313, -143, 27, 197, 367]

    def create_generals(self):
        for i in range(5):
            general = Turtle()
            general.penup()
            general.shape('opponent/general.gif')
            # general.shapesize(2, 2)
            general.goto(-345 + i * 170, 200)
            self.generals.append(general)

    def generals_move(self):
        for general in self.generals:
            if self.generals.index(general) == 0:
                self.bounce()
            general.goto(general.xcor() + self.move, general.ycor())

    def bounce(self):
        if self.generals[0].xcor() == self.distance_left[0] or self.generals[0].xcor() == self.distance_right[0]:
            self.move *= -1


class AlienGeneralMissile(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.shape('missile/general_missile.gif')
        self.goto(x, y)
        ALL_MISSILES.append(self)

    def attack(self):
        self.goto(self.xcor(), self.ycor() - MOVE_DISTANCE)


class AlienBoss(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('opponent/boss.gif')
        # self.shapesize(stretch_wid=3, stretch_len=5)
        self.goto(0, 270)
        self.move = MOVE_DISTANCE

    def move_boss(self):
        self.goto(self.xcor() + self.move, self.ycor())
        self.bounce()

    def bounce(self):
        if self.xcor() <= -390 or self.xcor() >= 380:
            self.move *= -1


class AlienBossMissile(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.shape('missile/boss_missile.gif')
        ALL_MISSILES.append(self)

    def attack(self):
        self.goto(self.xcor(), self.ycor() - MOVE_DISTANCE)


class BossLife:
    def __init__(self):
        self.lives = []
        self.move = MOVE_DISTANCE
        self.create_life()

    def create_life(self):
        for i in range(3):
            life = Turtle()
            life.penup()
            life.shape('player_earth/life.gif')
            life.goto(-22+22*i, 250)
            self.lives.append(life)

    def move_life(self):
        for life in self.lives:
            life.goto(life.xcor() + self.move, life.ycor())
        if self.lives[0].xcor() <= -408 or self.lives[0].xcor() >= 358:  # by tweaking the desired affect was achieved
            self.bounce()

    def bounce(self):
        self.move *= - 1
