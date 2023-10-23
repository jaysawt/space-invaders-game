from turtle import Turtle, Screen
import time
import random
from player import Player, PlayerMissile
from earth import Earth, EarthLife
from aliens import AlienSoldiers, AlienGenerals, AlienBoss, AlienSoldierMissile, AlienGeneralMissile, AlienBossMissile,\
    ALL_MISSILES, BossLife
from score_life import ScoreLife
import threading

LEVEL = 1
GAME_OVER = False
global soldiers, generals, boss, game_on, defender, defender_missile, earth, life, score


screen = Screen()
screen.bgpic(picname='galaxy/0.gif')
screen.setup(880, 710, 350, 0)
screen.title('Earth Defender from Space Invaders')
background_on = True
screen.addshape('player_earth/rocket.gif')
screen.addshape('missile/player_missile.gif')
screen.addshape('player_earth/earth.gif')
screen.addshape('player_earth/life.gif')
screen.addshape('opponent/soldier.gif')
screen.addshape('opponent/general.gif')
screen.addshape('opponent/boss.gif')
screen.addshape('missile/soldier_missile.gif')
screen.addshape('missile/general_missile.gif')
screen.addshape('missile/boss_missile.gif')


# ##########background image gif#####################
# Loading the frame images as shapes for background
for i in range(52):
    screen.addshape(f'galaxy/{i}.gif')
screen.tracer(0)


def back_change():
    while True:
        for i in range(52):
            screen.bgpic(f'galaxy/{i}.gif')
            screen.update()
            time.sleep(0.1)


def update_background():
    # Update the background image every 0.1 seconds
    back_change()
    screen.ontimer(update_background, 100)

################################################


def fire():
    global soldiers, generals, boss
    try:
        soldier = random.choice(soldiers.soldiers)
        AlienSoldierMissile(soldier.xcor(), soldier.ycor())
    except IndexError:
        pass
    try:
        if generals.generals:
            general = random.choice(generals.generals)
            AlienGeneralMissile(general.xcor(), general.ycor())
    except NameError:
        pass
    try:
        AlienBossMissile(boss.xcor(), boss.ycor())
    except ValueError and NameError:
        pass


def game_start():
    global soldiers, generals, boss, game_on, defender, defender_missile, earth, life, score, GAME_OVER, LEVEL

    if LEVEL == 1:
        soldiers = AlienSoldiers()
    elif LEVEL == 2:
        soldiers = AlienSoldiers()
        generals = AlienGenerals()
    else:
        soldiers = AlienSoldiers()
        generals = AlienGenerals()
        boss = AlienBoss()
        boss_life = BossLife()

    screen.onkeypress(defender.move_left, 'Left')
    screen.onkeypress(defender.move_right, 'Right')
    screen.onkey(lambda: defender_missile.fire_missile(defender.xcor(), defender.ycor()), 'space')

    def player_missile_delete():
        defender_missile.fire = 'fire'
        missile.goto(1000, 1000)
        ind = defender_missile.bullets.index(missile)
        defender_missile.bullets.pop(ind)

    def alien_missile_delete(alien_miss):
        alien_miss.goto(1000, 1000)
        loc = ALL_MISSILES.index(alien_miss)
        ALL_MISSILES.pop(loc)

    fire_count = 0
    while game_on:
        screen.update()
        time.sleep(0.1)

        defender_missile.move_missile()
        earth.rotate()
        life.move_life()

        soldiers.soldiers_move()
        try:
            generals.generals_move()
        except NameError:
            pass
        try:
            boss.move_boss()
            boss_life.move_life()
        except NameError:
            pass

        # the below step provides the timing for aliens to strike the missiles
        if fire_count % 50 == 0:
            fire()

        for alien_missile in ALL_MISSILES:
            alien_missile.attack()
            # the below step is done to memory manage the game as unnecessary objects are built up
            if -1305 >= alien_missile.ycor() >= -1313:
                index = ALL_MISSILES.index(alien_missile)
                ALL_MISSILES.pop(index)
            # detect collision of alien missile with player_earth
            if alien_missile.distance(defender) <= 15:
                alien_missile_delete(alien_missile)
                defender.hideturtle()
                time.sleep(0.5)
                defender.goto(0, -230)
                defender.showturtle()
                score.lives.pop()
                score.lives_update()
            if alien_missile.distance(earth) <= 38 and alien_missile.ycor() >= -280:
                alien_missile_delete(alien_missile)
                earth.hideturtle()
                time.sleep(0.5)
                earth.showturtle()
                life.lives[len(life.lives)-1].goto(1000, 1000)
                screen.update()   # this is introduced so that it captures the goto movement of (last life)
                life.lives.pop()  # when the while loop is turned off.

        for missile in defender_missile.bullets:
            if 355 >= missile.ycor() >= 352:
                defender_missile.fire = 'fire'
            # the below step is done to memory manage the game as unnecessary objects are built up
            if 1305 >= missile.ycor() >= 1300:
                player_missile_delete()
            # the below step is to detect both player and alien missile when they come in proximity with each other
            for alien_missiles in ALL_MISSILES:
                if missile.distance(alien_missiles) <= 15:
                    player_missile_delete()              # delete missile from list to manage memory
                    alien_missile_delete(alien_missiles)  # delete missile from list to manage memory
                    score.score += 1
                    score.lives_update()

            # detect collision of missile with aliens
            for alien in soldiers.soldiers:
                if alien.distance(missile) <= 20:
                    alien.goto(1000, 1000)
                    # memory management for soldiers
                    index = soldiers.soldiers.index(alien)
                    soldiers.soldiers.pop(index)
                    soldiers.distance_right.pop(index)  # deleting corresponding bounce distance of soldiers
                    soldiers.distance_left.pop(index)
                    player_missile_delete()  # delete missile from list to manage memory
                    score.score += 5
                    score.lives_update()

            try:
                for alien in generals.generals:
                    if alien.distance(missile) <= 20:
                        alien.goto(1000, 1000)
                        # memory management for generals
                        index = generals.generals.index(alien)
                        generals.generals.pop(index)
                        generals.distance_left.pop(index)  # deleting corresponding bounce distance of generals
                        generals.distance_right.pop(index)
                        player_missile_delete()
                        score.score += 10
                        score.lives_update()
            except NameError:
                # This is done so that it does not give error for level 1 as generals are not created
                pass

            try:
                if missile.distance(boss) <= 45 and 280 >= missile.ycor() >= 270:
                    boss_life.lives[len(boss_life.lives)-1].goto(1000, 1000)
                    screen.update()
                    boss_life.lives.pop()
                    player_missile_delete()
                    score.score += 15
                    score.lives_update()
                    if not boss_life.lives:
                        boss.goto(1000, 1000)
                        del boss
            except NameError:
                # This is done so that it does not give error for level 2 as boss is not created
                pass

        # Game Over check
        if not life.lives or not score.lives:
            game_on = False
            GAME_OVER = True
            score.game_over()
            score.check_highscore()

        # Game Winning check
        if LEVEL == 3 and not soldiers.soldiers and not generals.generals and not boss_life.lives:
            screen.update()
            game_on = False
            score.game_winner()
            score.check_highscore()

        # Level 2 completion
        if LEVEL == 2 and not soldiers.soldiers and not generals.generals:
            game_on = False
            screen.update()
            score.level_complete()
            score.level += 1
            LEVEL += 1
            del soldiers
            del generals

        # Level 1 completion
        if LEVEL == 1 and not soldiers.soldiers:
            game_on = False
            screen.update()
            score.level_complete()
            score.level += 1
            LEVEL += 1
            del soldiers

        fire_count += 1


def start_game():
    # Delete the below if the working of game is too slow #
    bg_thread = threading.Thread(target=update_background, daemon=True)
    bg_thread.start()
    #                                                     #
    global game_on, defender, defender_missile, earth, life, score, GAME_OVER, LEVEL
    text_turtle.clear()
    screen.onkeypress(None, 'Return')  # this is done so that no more new objects are created when the game is running

    defender = Player()
    defender_missile = PlayerMissile()

    earth = Earth()
    life = EarthLife()

    score = ScoreLife()

    game_on = True
    game_start()
    if LEVEL == 2 and not GAME_OVER:
        game_on = True
        score.lives_update()
        game_start()
    if LEVEL == 3 and not GAME_OVER:
        game_on = True
        score.lives_update()
        game_start()


# introduction text
text_turtle = Turtle()
text_turtle.hideturtle()
text_turtle.penup()
text_turtle.goto(-280, 0)
text_turtle.color('white')
text_turtle.write("Welcome to the game of Space Invaders👽\n\n "
                  "Press 'SIDE KEYS' to navigate ship🚀\n press 'SPACE' to shoot missiles💥\n\n"
                  "Press 'Enter' to start the game🎮....", font=('lucida', 20, 'bold'))

screen.listen()
screen.onkeypress(start_game, 'Return')


screen.mainloop()
