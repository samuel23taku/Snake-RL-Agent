import turtle
from head import Head
import time
import random
import game_constants as gs
import numpy as np

class GameLauncher:
    def __init__(self):
        self.turtle = turtle
        self.boundary = 140  # Game boundary is ±140
        self.cell_size = 20  # Each block in the snake segment is 20 x 20
        
        # Calculate grid size from boundaries and cell size
        # (-140 to +140 = 280 units total, divided by 20 = 14 cells)
        self.grid_size = (self.boundary * 2) // self.cell_size  # Equals 14``
        
        self.setup_window()
        self.segments = []
        self.high_score = 0
        self.head = Head()
        self.setup_pen()
        self.setup_food()
        self.keybindings()
        self.score = 0


        
    def check_wall_collision(self):
        head = self.head
        segments = self.segments
        if head.head.xcor()>140 or head.head.xcor()<-140 or head.head.ycor()>140 or head.head.ycor()<-140:
            time.sleep(1)
            head.head.goto(0,0)
            head.head.direction = "stop"

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)
    
            # Clear the segments list
            segments.clear()

            # Reset the score
            self.score = 0

            # Reset the delay
            self.delay = gs.GAME_SPEED

            self.pen.clear()
            self.pen.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center", font=("Courier", 24, "normal")) 
            return True
        return False

    def check_food_collision(self):
        if self.head.head.distance(self.food) < 20:
            # Move the self.food to a random spot
            x = random.randint(-140, 140)
            y = random.randint(-140, 140)
            self.food.goto(x,y)

            # Add a segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            self. segments.append(new_segment)

            # Shorten the delay
            self.delay -= 0.001

            # Increase the score
            self.score += 10

            if self.score > self.high_score:
                self.high_score = self.score
            
            self.pen.clear()
            self.pen.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center", font=("Courier", 24, "normal")) 

    def state_to_array(self):
        def turtle_to_grid(x, y):
            # Convert from (-140, 140) range to (0, 13) range
            grid_x = int((x + self.boundary) // self.cell_size)
            grid_y = int((y + self.boundary) // self.cell_size)
            # Ensure coordinates are within grid bounds
            grid_x = max(0, min(grid_x, self.grid_size - 1))
            grid_y = max(0, min(grid_y, self.grid_size - 1))
            return grid_x, grid_y

        # Create empty grid
        grid = np.zeros((self.grid_size, self.grid_size, 3))

        # Set head
        head_x, head_y = turtle_to_grid(self.head.head.xcor(), self.head.head.ycor())
        grid[head_y, head_x, 0] = 1
        print(f"Setting head at [{head_y}, {head_x}], value: {grid[head_y, head_x, 0]}")

        # Set body segments
        for segment in self.segments:
            seg_x, seg_y = turtle_to_grid(segment.xcor(), segment.ycor())
            grid[seg_y, seg_x, 1] = 1
            print(f"Setting body segment at [{seg_y}, {seg_x}], value: {grid[seg_y, seg_x, 1]}")

        # Set food
        food_x, food_y = turtle_to_grid(self.food.xcor(), self.food.ycor())
        grid[food_y, food_x, 2] = 1  # Make sure this line is actually setting the value
        print(f"Setting food at [{food_y}, {food_x}], value: {grid[food_y, food_x, 2]}")


        return grid.flatten()

        


    def update_snake_body(self):
        # Move the end segments first in reverse order
        for index in range(len(self.segments)-1, 0, -1):
            x = self.segments[index-1].xcor()
            y = self.segments[index-1].ycor()
            self.segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(self.segments) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.segments[0].goto(x,y)


    def get_random_action(self):
        # This is a placeholder. In a real RL setup, you'd get the action from your model
        return random.choice(['up', 'down', 'left', 'right'])
    
    def get_reward(self, old_score, new_score, collision):
        if collision:
            return -1
        elif new_score > old_score:
            return 1
        else:
            return 0

    def step(self,action):
        old_score = self.score
        head = self.head
        self.delay = gs.GAME_SPEED

        # Score
        segments = self.segments
         
        match action:
            case "up":
                self.head.go_up()
                print("UP")
            case "down":
                self.head.go_down()
            case "left":
                self.head.go_left()
            case _:
                self.head.go_right()

        self.wn.update()
        collision_check = self.check_wall_collision() or self.check_self_collision()
        self.check_food_collision()
        self.update_snake_body()
        head.move()
        new_state = self.state_to_array()
        print("collection check is ",collision_check)
        reward = self.get_reward(old_score, self.score, collision_check)
        print("Reward is ",reward)
        done = collision_check

        return new_state,reward,done
        
    def check_self_collision(self):
        segments = self.segments
        head = self.head
        pen = self.pen

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
                self.score = 0

                # Reset the delay
                self.delay = 0.1
            
                # Update the score display
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center", font=("Courier", 24, "normal"))

                return True
        return False

    def setup_window(self):
        self.wn = self.turtle.Screen()
        self.wn = turtle.Screen()
        self.wn.title("SnaKE")
        self.wn.bgcolor("green")
        self.wn.setup(width=300, height=300)
        self.wn.tracer(0) # Turns off the screen updates

    def setup_pen(self):
        self.pen = self.turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 140)
        self.pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

    def keybindings(self):
        self.wn.listen()
        self.wn.onkeypress(self.go_up, "w")
        self.wn.onkeypress(self.go_down, "s")
        self.wn.onkeypress(self.go_left, "a")
        self.wn.onkeypress(self.go_right, "d")
    
    def go_up(self):
        self.step("up")
    def go_down(self):
        self.step("down")

    def go_left(self):
        self.step("left")

    def go_right(self):
        self.step("right")

    def setup_food(self):
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0,100)



game = GameLauncher()
for i in range(10):
    action = game.get_random_action()
    new_state,reward,done =game.step(action)
    print(f"NEw state is {new_state} | Reward is {reward} | Done is {done}")
    time.sleep(2)
