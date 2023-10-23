from turtle import Turtle
import time


class ScoreLife(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.lives = ['❤', '❤', '❤']
        self.level = 1
        self.penup()
        self.hideturtle()
        self.lives_update()

    def score_update(self):
        self.color('white')
        self.goto(-400, 310)
        self.write(f'Score:{self.score}', align='left', font=('lucid', 20, 'bold'))

    def high_score(self):
        self.color('green')
        self.goto(-250, 310)
        with open('high score.txt', 'r') as f:
            high_score = f.read()
        self.write(f'Highest Score:{high_score}', align='left', font=('lucid', 20, 'bold'))

    def lives_update(self):
        self.clear()
        self.score_update()
        self.high_score()
        self.level_up()
        self.goto(230, 310)
        self.color('red')
        if not self.lives:
            self.write('Lives:➖➖➖', align='left', font=('lucid', 20, 'bold'))
        else:
            self.write(f'Lives:{"".join(self.lives)}', align='left', font=('lucid', 20, 'bold'))

    def level_up(self):
        self.color('yellow')
        self.goto(50, 310)
        self.write(f'Level:{self.level}', align='left', font=('lucid', 20, 'bold'))

    def check_highscore(self):
        with open('high score.txt', 'r') as f:
            high_score = f.read()
        if self.score > int(high_score):
            with open('high score.txt', 'w') as f:
                f.write(f'{self.score}')

    def game_over(self):
        self.lives_update()
        self.goto(0, 0)
        self.color('red')
        self.write('Game Over ❌', align='center', font=('arial', 30, 'bold'))
        self.check_highscore()

    def game_winner(self):
        self.lives_update()
        self.goto(0, 0)
        self.color('yellow')
        self.write('You Win 🏆', align='center', font=('arial', 30, 'bold'))
        self.check_highscore()

    def level_complete(self):
        self.color('yellow')
        self.goto(0, 0)
        self.write("Level Completed\nLet's Move To Next Level", align='center', font=('lucid', 20, 'bold'))
        time.sleep(2)
        self.lives_update()
