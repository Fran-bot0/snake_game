#!/usr/bin/env python

from turtle import Screen, Turtle
from time import sleep
from random import randint

MOVE_DISTANCE = 10
STARTING_LENGTH = 3
SNAKE_WIDTH = 0.5
LIVES = 5

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("SNAKE GAME")

# Make the screen not update anymore
screen.tracer(0)


class Snake:

    def __init__(self):
        self.snake_segments = []
        self.create()
        self.head = self.snake_segments[0]

    def create(self):
        '''Creates the snake'''
        xcoord = 0
        for num in range(STARTING_LENGTH):
            self.add_segment((xcoord, 0))
            xcoord -= 20

    def move(self):
        '''Makes the snake continuasly move forward'''
        for segment_num in range(len(self.snake_segments) - 1, 0, -1):
            new_x = self.snake_segments[segment_num - 1].xcor()
            new_y = self.snake_segments[segment_num - 1].ycor()
            self.snake_segments[segment_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def turn_up(self):
        '''Turns the snake head up'''
        if self.head.heading() != 270:
            self.head.setheading(90)

    def turn_right(self):
        '''Turns the snake head down'''
        if self.head.heading() != 180:
            self.head.setheading(0)

    def turn_left(self):
        '''Turns the snake head left'''
        if self.head.heading() != 0:
            self.head.setheading(180)

    def turn_down(self):
        '''Turns the snake head right'''
        if self.head.heading() != 90:
            self.head.setheading(270)

    def add_segment(self, coordinates):
        '''Creates a new segment'''
        new_segment = Turtle(shape="square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.shapesize(stretch_wid=SNAKE_WIDTH)
        new_segment.goto(coordinates)
        self.snake_segments.append(new_segment)

    def grow(self):
        '''Adds a new segment to the snake'''
        self.add_segment(self.snake_segments[-1].position())

    def reset(self):
        '''Resets the snake to its original size'''
        for seg in self.snake_segments:
            seg.goto(1000, 1000)
        self.snake_segments.clear()
        self.create()
        self.head = self.snake_segments[0]


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        '''Generates a new food in a random spot on the playing screen'''
        self.goto(randint(-280, 280), randint(-280, 280))


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.points = 0
        self.lives = LIVES
        with open("snake_score.txt", mode="r+") as file:
            self.high_score = int(file.read())
        self.penup()
        self.color("white")
        self.hideturtle()
        self.goto(0, 260)
        self.write(arg=f"Score: {self.points} High Score: {self.high_score} Lives: {self.lives}", move=False,
                   align="center", font=("Courier New", 14, "bold"))

    def keep_score(self):
        '''Keeps the current score on the screen'''
        self.points += 1
        self.clear()
        self.write(arg=f"Score: {self.points} High Score: {self.high_score} Lives: {self.lives-1}", move=False,
                   align="center", font=("Courier New", 14, "bold"))

    def keep_high_score(self):
        '''Keeps the highest score achieved by the player'''
        if self.high_score < self.points:
            self.high_score = self.points
            with open("snake_score.txt", mode="w") as file:
                file.write(f"{self.high_score}")
        self.points = -1
        self.keep_score()


class Referee(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.pencolor("white")
        self.penup()
        self.goto(-290, 290)

    def draw_game_field(self):
        '''Makes the gaming screen'''
        self.pendown()
        self.goto(-290, -290)
        self.goto(290, -290)
        self.goto(290, 290)
        self.goto(-290, 290)
        self.penup()

    def game_over(self):
        '''Creates game over screen'''
        self.goto(0, 0)
        self.pencolor("red")
        self.write(arg="Game Over", move=False, align="center", font=("Courier New", 32, "bold"))


snake = Snake()
food = Food()
score = Score()
referee = Referee()

screen.listen()

# Make the snake move using the keyboard keys
screen.onkey(fun=snake.turn_up, key="Up")
screen.onkey(fun=snake.turn_right, key="Right")
screen.onkey(fun=snake.turn_left, key="Left")
screen.onkey(fun=snake.turn_down, key="Down")

referee.draw_game_field()

# While the player has lives, the game keeps going.
while score.lives > 0:
    screen.update()
    sleep(0.04)
    snake.move()

    # If the snake head is at less than 15 units of distance of the food, consume it.
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.grow()
        score.keep_score()

    # If the snake head gets out of the bounds of the screen, reset the game, keep the high score, and lose a life
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        snake.reset()
        score.keep_high_score()
        score.lives -= 1

    # If the snake head is at less than 5 units of distance from any other snake segment, reset the game, keep the high score, and lose a life.
    for segment in snake.snake_segments[1:]:
        if segment.distance(snake.head.position()) < 5:
            snake.reset()
            score.keep_high_score()
            score.lives -= 1

# When the player has no more lives, stop the game and show the game over screen.
referee.game_over()

screen.exitonclick()
