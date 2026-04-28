from turtle import *
import random

def generate_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def playing_area():
    pen = Turtle()
    pen.ht()
    pen.speed(0)
    pen.color('teal')
    pen.penup()
    pen.goto(-240, 240)
    pen.pendown()
    pen.begin_fill()
    for i in range(4):
        pen.forward(480)
        pen.right(90)
    pen.end_fill()

class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.shape("arrow")
        self.shapesize(.65)
        self.color("black")
        self.penup()
        self.speed(0)
        self.player = player
        self.goto(player.xcor(), player.ycor())
        self.setheading(player.heading())
        self.alive = True
        self.st()

    def move(self):
        if self.alive:
            self.forward(20)
            if self.xcor() > 235 or self.xcor() < -235 or self.ycor() > 235 or self.ycor() < -235:
                self.die()

    def die(self):
        self.alive = False
        self.ht()
        if self in self.player.bullets:
            self.player.bullets.remove(self)

class Player(Turtle):
    def __init__(self, x, y, start_color, screen, right_key, left_key, fire_key):
        super().__init__()
        self.ht()
        self.speed(0)
        self.color(start_color)
        self.penup()
        self.goto(x, y)
        self.setheading(90)
        self.shape("turtle")
        self.bullets = []
        
        self.health = 3
        self.alive = True
        self.colors = [start_color, "yellow", "red"]
        
        self.st()
        screen.onkeypress(self.turn_left, left_key)
        screen.onkeypress(self.turn_right, right_key)
        screen.onkey(self.fire, fire_key)

    def fire(self):
            self.bullets.append(Bullet(self))

    def turn_left(self):
        self.left(15)

    def turn_right(self):
        self.right(15)

    def move(self):
        self.forward(10)
        if self.xcor() > 230 or self.xcor() < -230:
            self.setheading(180 - self.heading())
        if self.ycor() > 230 or self.ycor() < -230:
            self.setheading(-self.heading())
            
    def take_damage(self):
        self.health -= 1
        if self.health > 0:
            color_index = 3 - self.health
            self.color(self.colors[color_index])
        else:
            self.alive = False
            self.ht()

screen = Screen()
screen.bgcolor("black")
screen.setup(520, 520)
screen.listen()

playing_area()

p1 = Player(-100, 0, "green", screen, "d", "a", "w")
p2 = Player(100, 0, "blue", screen, "Right", "Left", "Up")

players = [p1, p2]

while len(players) == 2:
    for player in players:
        player.move()
    
    i = 0
    while i < len(p1.bullets):
        b = p1.bullets[i]
        b.move()
        if b.alive and b.distance(p2) < 20:
            p2.take_damage()
            b.die()
            if not p2.alive and p2 in players:
                players.remove(p2)
        elif b.alive:
            i += 1

    j = 0
    while j < len(p2.bullets):
        b = p2.bullets[j]
        b.move()
        if b.alive and b.distance(p1) < 20:
            p1.take_damage()
            b.die()
            if not p1.alive and p1 in players:
                players.remove(p1)
        elif b.alive:
            j += 1

screen.exitonclick()