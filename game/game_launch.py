import turtle
from head import Head
import time
import random

class GameLauncher:
    def __init__(self):
        self.turtle = turtle
        self.setup_window()
        self.head = Head()
        self.setup_pen()
        self.setup_food()
        self.keybindings()
        

    def start(self):
        wn = self.wn
        head = self.head
        delay = 0.1

        # Score
        score = 0
        high_score = 0
        segments = []
        pen = self.pen
        while True:
            print("Gameplay")
            self.wn.update()

            # Check for a collision with the border
            if head.head.xcor()>290 or head.head.xcor()<-290 or head.head.ycor()>290 or head.head.ycor()<-290:
                time.sleep(1)
                head.head.goto(0,0)
                head.head.direction = "stop"

                # Hide the segments
                for segment in segments:
                    segment.goto(1000, 1000)
                
                # Clear the segments list
                segments.clear()

                # Reset the score
                score = 0

                # Reset the delay
                delay = 0.1

                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 


            # Check for a collision with the self.food
            if head.head.distance(self.food) < 20:
                # Move the self.food to a random spot
                x = random.randint(-290, 290)
                y = random.randint(-290, 290)
                self.food.goto(x,y)

                # Add a segment
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color("grey")
                new_segment.penup()
                segments.append(new_segment)

                # Shorten the delay
                delay -= 0.001

                # Increase the score
                score += 10

                if score > high_score:
                    high_score = score
                
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

            # Move the end segments first in reverse order
            for index in range(len(segments)-1, 0, -1):
                x = segments[index-1].xcor()
                y = segments[index-1].ycor()
                segments[index].goto(x, y)

            # Move segment 0 to where the head is
            if len(segments) > 0:
                x = head.head.xcor()
                y = head.head.ycor()
                segments[0].goto(x,y)
                
            head.move()    

            # Check for head collision with the body segments
            for segment in segments:
                if segment.distance(head.head) < 20:
                    time.sleep(1)
                    head.head.goto(0,0)
                    head.direction = "stop"
                
                    # Hide the segments
                    for segment in segments:
                        segment.goto(1000, 1000)
                
                    # Clear the segments list
                    segments.clear()

                    # Reset the score
                    score = 0

                    # Reset the delay
                    delay = 0.1
                
                    # Update the score display
                    pen.clear()
                    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

            time.sleep(delay)

    def setup_window(self):
        self.wn = self.turtle.Screen()
        self.wn = turtle.Screen()
        self.wn.title("Snake Game by @TokyoEdTech")
        self.wn.bgcolor("green")
        self.wn.setup(width=600, height=600)
        self.wn.tracer(0) # Turns off the screen updates

    def setup_pen(self):
        self.pen = self.turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

    def keybindings(self):
        self.wn.listen()
        self.wn.onkeypress(self.head.go_up, "w")
        self.wn.onkeypress(self.head.go_down, "s")
        self.wn.onkeypress(self.head.go_left, "a")
        self.wn.onkeypress(self.head.go_right, "d")
    
    
    def setup_food(self):
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0,100)



game = GameLauncher()
game.start()
