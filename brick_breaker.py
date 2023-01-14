# Author: 99ccarbaugh
# Created: 12/31/22
# Email: chasecarbaugh@gmail.com


import tkinter as tk
import random
import time
import numpy as np

DELAY = 100
RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
GREEN_COLOR  = "#7BC043"
BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'

TOP_BOUND = 0
BOTTOM_BOUND = 800
LEFT_BOUND = 0
RIGHT_BOUND = 1200


PADDLE_START_RIGHT_X = 700
PADDLE_START_BOTTOM_Y = 725
PADDLE_START_LEFT_X = 500
PADDLE_START_TOP_Y = 700

PADDLE_TOP = 700
PADDLE_WIDTH = 200

# Normal
BALL_START_LEFT_X = 590
BALL_START_TOP_Y = 680
BALL_START_RIGHT_X = 610
BALL_START_BOTTOM_Y = 700

# #Debug
# BALL_START_LEFT_X = 0
# BALL_START_TOP_Y = 710
# BALL_START_RIGHT_X = 20
# BALL_START_BOTTOM_Y = 730

BALL_START_XV = 0
BALL_START_YV = -1

PADDLE_MOVE_SPEED = 30
BALL_MOVE_SPEED = 30


class Brick:
    def __init__(self, id, left, right, top, bottom,):
        self.id = id
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
    
    def draw_brick(self, canvas):
        self.brick_rec = canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
        fill=GREEN_COLOR, outline=BLUE_COLOR)


class BrickBreaker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Brick Breaker")
        self.canvas = tk.Canvas(self.window, width=1200, height=800)
        self.canvas.pack()
        self.window.bind("<Key>", self.key_input)
        self.window.bind("<Button-1>", self.mouse_input)
        self.window.bind("<Motion>", self.motion)
        self.play_again()
        self.begin = False

    def key_input(self, event):
        key_pressed = event.keysym
        if self.check_if_key_valid(key_pressed):
            self.begin = True
            self.last_key = key_pressed

    def check_if_key_valid(self,key):
        valid_keys = ['Left', 'Right']
        if key in valid_keys:
            return True
        else:
            return False


    def mouse_input(self, event):
        self.play_again()
    
    def play_again(self):
        self.canvas.delete("all")
        self.initialize_paddle()
        self.initialize_ball()
        self.initialize_bricks()

    def initialize_paddle(self):
        self.paddle_heading = "None"
        self.paddle_right_x = PADDLE_START_RIGHT_X
        self.paddle_bottom_y = PADDLE_START_BOTTOM_Y 
        self.paddle_left_x = PADDLE_START_LEFT_X
        self.paddle_top_y = PADDLE_START_TOP_Y
        self.paddle_obj = self.canvas.create_rectangle(
            self.paddle_right_x, self.paddle_bottom_y, self.paddle_left_x, self.paddle_top_y, 
            fill=RED_COLOR_LIGHT, outline=BLUE_COLOR
        )

    def initialize_ball(self):
        # Save ball initial coordinates as global variables
        # will need ball current position, past position from last iteration and x,y vel
        self.ball_left_x = BALL_START_LEFT_X
        self.ball_top_y = BALL_START_TOP_Y
        self.ball_right_x = BALL_START_RIGHT_X
        self.ball_bottom_y = BALL_START_BOTTOM_Y

        self.ball_last_left_x = BALL_START_LEFT_X
        self.ball_last_top_y = BALL_START_TOP_Y
        self.ball_last_right_x = BALL_START_RIGHT_X
        self.ball_last_bottom_y = BALL_START_BOTTOM_Y

        self.ball_xv = BALL_START_XV
        self.ball_yv = BALL_START_YV

        self.ball_obj = self.canvas.create_rectangle(
            self.ball_left_x, self.ball_top_y, self.ball_right_x, self.ball_bottom_y, 
            fill=BLUE_COLOR_LIGHT, outline=RED_COLOR
        )


    # X1Y1 is top left, X2Y2 is bottom right
    def update_ball(self):
        self.ball_last_left_x = self.ball_left_x
        self.ball_last_top_y = self.ball_top_y
        self.ball_last_right_x = self.ball_right_x
        self.ball_last_bottom_y = self.ball_bottom_y
        self.canvas.delete(self.ball_obj)

        # Normal Update
        self.ball_left_x = self.ball_last_left_x + (self.ball_xv * BALL_MOVE_SPEED)
        self.ball_top_y = self.ball_last_top_y + (self.ball_yv * BALL_MOVE_SPEED)
        self.ball_right_x = self.ball_last_right_x + (self.ball_xv * BALL_MOVE_SPEED)
        self.ball_bottom_y = self.ball_last_bottom_y + (self.ball_yv * BALL_MOVE_SPEED)

        # Impacts with walls
        
        # Impact with top
        if self.ball_top_y <= TOP_BOUND:
            self.ball_top_y = 0
            self.ball_bottom_y = 20
            self.ball_yv = self.ball_yv * -1


        # Impact with Left
        if self.ball_left_x <= LEFT_BOUND:
            self.ball_left_x = 0
            self.ball_right_x = 20
            self.ball_xv = self.ball_xv * -1

        # Impact with right
        if self.ball_right_x >= RIGHT_BOUND:
            self.ball_left_x = 1180
            self.ball_right_x = 1200
            self.ball_xv = self.ball_xv * -1

        
        # Impact with Paddle possible
        if self.ball_bottom_y >= PADDLE_TOP and self.ball_top_y <= self.paddle_top_y:
            # Impact with top
            # print("BALL\nLEFT: %d RIGHT: %d TOP: %d BOTTOM: %d \nPADDLE\nLEFT: %d RIGHT: %d TOP: %d BOTTOM: %d"
            # % (self.ball_left_x, self.ball_right_x, self.ball_top_y, self.ball_bottom_y, self.paddle_left_x, self.paddle_right_x, self.paddle_top_y, self.paddle_bottom_y))

            if self.ball_right_x >= self.paddle_left_x and self.ball_left_x <= self.paddle_right_x:
                print(PADDLE_TOP, "BEFORE IMPACT y1: %d, y2: %d" % (self.ball_top_y, self.ball_bottom_y))
                self.ball_top_y = PADDLE_TOP - 20
                self.ball_bottom_y = PADDLE_TOP
                self.update_ball_vels()
                self.ball_yv = self.ball_yv * -1
                print("AFTER IMPACT y1: %d, y2: %d" % (self.ball_top_y, self.ball_bottom_y))\

            # Believe this problem will be solved by adding paddle physics

            # Potential collision issues with 2 moving objects
            # # Impact with left side
            # if self.ball_right_x >= self.paddle_left_x and self.ball_left_x < self.paddle_left_x and self.ball_top_y >= self.paddle_bottom_y and self.ball_bottom_y <= self.paddle_top_y:
            #     print("left side impact")
        

            # # Impact with right side

        self.ball_obj = self.canvas.create_rectangle(
            self.ball_left_x, self.ball_top_y, self.ball_right_x, self.ball_bottom_y, 
            fill=BLUE_COLOR_LIGHT, outline=RED_COLOR
        )

    def update_ball_vels(self):
        # Get x value for center of ball
        ball_center = int((self.ball_right_x + self.ball_left_x) /2)
        # Adjust center value to be relative to a hypothetical paddle from 0 to 200
        ball_center_relative = ball_center - self.paddle_left_x
        ball_dist = ball_center_relative - 100
        ball_dist_scaled = int(ball_dist / 10)
        print("Ball center relative: %d\nBall dist: %d\nBall dist scaled: %d" %(ball_center_relative, ball_dist, ball_dist_scaled))
        self.ball_xv = ball_dist_scaled / 10
        return

    # Done goofed - X1Y1 is top right, X2Y2 is bottom left

    def update_paddle(self, mouse_x):
        paddle_center = (self.paddle_left_x + self.paddle_right_x) / 2
        x_delta = mouse_x - paddle_center
        self.paddle_left_x += x_delta
        self.paddle_right_x += x_delta
        
        self.canvas.delete(self.paddle_obj)
        self.paddle_obj = self.canvas.create_rectangle(
            self.paddle_right_x, self.paddle_bottom_y, self.paddle_left_x, self.paddle_top_y, 
            fill=RED_COLOR_LIGHT, outline=BLUE_COLOR
        )

    def motion(self, event):
        # print("Mouse position: (%s %s)" % (event.x, event.y))
        self.update_paddle(event.x)

    def initialize_bricks(self):
        self.bricks = []
        for i in range(0, 1):
            print("i: %s" % i)
            self.bricks.append(Brick(i, 580, 620, 200, 220))
            self.bricks[i].draw_brick(self.canvas)

    def update_game(self):
        self.update_ball()

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                self.window.after(DELAY, self.update_game())
                self.last_key = "None"
                # Define end state later
                # else:
                #     self.begin = False
                #     self.display_gameover()


game_instance = BrickBreaker()
game_instance.mainloop()