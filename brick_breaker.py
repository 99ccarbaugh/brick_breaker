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
# BALL_START_LEFT_X = 590
# BALL_START_TOP_Y = 680
# BALL_START_RIGHT_X = 610
# BALL_START_BOTTOM_Y = 700

# Debug
BALL_START_LEFT_X = 10
BALL_START_TOP_Y = 205
BALL_START_RIGHT_X = 30
BALL_START_BOTTOM_Y = 225

BALL_START_XV = 1
BALL_START_YV = 0

PADDLE_MOVE_SPEED = 30
BALL_MOVE_SPEED = 30

class RectObj:
    def __init__(self, id, left, right, top, bottom, fill_color, border_color, canvas):
        self.id = id
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.fill_color = fill_color
        self.border_color = border_color

        self.draw_rect(canvas)

    def draw_rect(self, canvas):
        self.rect_obj = canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
        fill=self.fill_color, outline=self.border_color)

class Brick(RectObj):
    pass

class Paddle(RectObj):
    pass
    
class Ball(RectObj):
    def __init__(self, id, left, right, top, bottom, fill_color, border_color, canvas):
        self.id = id
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.last_left = left
        self.last_right = right
        self.last_top = top
        self.last_bottom = bottom

        self.x_vel = 0
        self.y_vel = -1

        self.fill_color = fill_color
        self.border_color = border_color

        self.draw_ball(canvas)

    def draw_ball(self, canvas):
        self.ball_obj = canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
        fill=self.fill_color, outline=self.border_color)

    

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


    # X1Y1 is top left, X2Y2 is bottom right
    def update_ball(self):
        self.ball.last_left = self.ball.left
        self.ball.last_top = self.ball.top
        self.ball.last_right = self.ball.right
        self.ball.last_bottom = self.ball.bottom
        self.canvas.delete(self.ball.ball_obj)

        # Normal Update
        self.ball.left = self.ball.last_left + (self.ball.x_vel * BALL_MOVE_SPEED)
        self.ball.top = self.ball.last_top + (self.ball.y_vel * BALL_MOVE_SPEED)
        self.ball.right = self.ball.last_right + (self.ball.x_vel * BALL_MOVE_SPEED)
        self.ball.bottom = self.ball.last_bottom + (self.ball.y_vel * BALL_MOVE_SPEED)

        # Impacts with walls
        
        # Impact with top
        if self.ball.top <= TOP_BOUND:
            self.ball.top = 0
            self.ball.bottom = 20
            self.ball.y_vel = self.ball.y_vel * -1


        # Impact with Left
        if self.ball.left <= LEFT_BOUND:
            self.ball.left = 0
            self.ball.right = 20
            self.ball.x_vel = self.ball.x_vel * -1

        # Impact with right
        if self.ball.right >= RIGHT_BOUND:
            self.ball.left = 1180
            self.ball.right = 1200
            self.ball.x_vel = self.ball.x_vel * -1

        
        # Impact with Paddle possible
        if self.ball.bottom >= PADDLE_TOP and self.ball.top <= self.paddle.top:
            # Impact with top
            # print("BALL\nLEFT: %d RIGHT: %d TOP: %d BOTTOM: %d \nPADDLE\nLEFT: %d RIGHT: %d TOP: %d BOTTOM: %d"
            # % (self.ball_left_x, self.ball_right_x, self.ball_top_y, self.ball_bottom_y, self.paddle_left_x, self.paddle_right_x, self.paddle_top_y, self.paddle_bottom_y))

            if self.ball.right >= self.paddle.left and self.ball.left <= self.paddle.right:
                print(PADDLE_TOP, "BEFORE IMPACT y1: %d, y2: %d" % (self.ball.top, self.ball.bottom))
                self.ball.top = PADDLE_TOP - 20
                self.ball.bottom = PADDLE_TOP
                self.update_ball_vels()
                self.ball.y_vel = self.ball.y_vel * -1
                print("AFTER IMPACT y1: %d, y2: %d" % (self.ball.top, self.ball.bottom))\

            # Believe this problem will be solved by adding paddle physics

            # Potential collision issues with 2 moving objects
            # # Impact with left side
            # if self.ball_right_x >= self.paddle_left_x and self.ball_left_x < self.paddle_left_x and self.ball_top_y >= self.paddle_bottom_y and self.ball_bottom_y <= self.paddle_top_y:
            #     print("left side impact")
        

            # # Impact with right side
        self.ball.draw_ball(self.canvas)



    def mouse_input(self, event):
        self.play_again()
    
    def play_again(self):
        self.canvas.delete("all")
        self.initialize_game_objs()

    def initialize_game_objs(self):
        # Initialize paddle
        self.paddle = Paddle(0, PADDLE_START_LEFT_X, PADDLE_START_RIGHT_X, PADDLE_START_TOP_Y, PADDLE_START_BOTTOM_Y,
            RED_COLOR_LIGHT, BLUE_COLOR, self.canvas)
        # Initialize ball
        self.ball = Ball(0, BALL_START_LEFT_X, BALL_START_RIGHT_X, BALL_START_TOP_Y, BALL_START_BOTTOM_Y,
            BLUE_COLOR_LIGHT, RED_COLOR, self.canvas)
        # Initialize Bricks
        self.initialize_bricks()
        return
   

    def update_ball_vels(self):
        # Get x value for center of ball
        ball_center = int((self.ball.right + self.ball.left) /2)
        # Adjust center value to be relative to a hypothetical paddle from 0 to 200
        ball_center_relative = ball_center - self.paddle.left
        ball_dist = ball_center_relative - 100
        ball_dist_scaled = int(ball_dist / 10)
        print("Ball center relative: %d\nBall dist: %d\nBall dist scaled: %d" %(ball_center_relative, ball_dist, ball_dist_scaled))
        self.ball.x_vel = ball_dist_scaled / 10
        return

    # Done goofed - X1Y1 is top right, X2Y2 is bottom left

    def update_paddle(self, mouse_x):
        paddle_center = (self.paddle.left + self.paddle.right) / 2
        x_delta = mouse_x - paddle_center
        self.paddle.left += x_delta
        self.paddle.right += x_delta
        
        self.canvas.delete(self.paddle.rect_obj)
        self.paddle.draw_rect(self.canvas)

    def motion(self, event):
        # print("Mouse position: (%s %s)" % (event.x, event.y))
        self.update_paddle(event.x)

    def initialize_bricks(self):
        self.bricks = []
        for i in range(0, 1):
            print("i: %s" % i)
            self.bricks.append(Brick(i, 580, 620, 200, 220, GREEN_COLOR, BLUE_COLOR_LIGHT, self.canvas))
            # self.bricks[i].draw_brick(self.canvas)

    def check_bricks(self):
        for brick in self.bricks:
            # Could nest some of these ifs (TOP/Bottom + Left/Right)
            # Bottom
            if self.ball.top <= brick.bottom and self.ball.bottom >= brick.bottom and self.ball.right >= brick.left and self.ball.left <= brick.right:
                print("IMPACT Bottom")
                self.ball_yv = self.ball_yv * -1
                self.ball_last_top_y = self.ball_top_y
                self.ball_last_bottom_y = self.ball_bottom_y

                self.ball_top_y = brick.bottom
                self.ball_bottom_y = brick.bottom + 20


            # Top
            elif self.ball_top_y <= brick.top and self.ball_bottom_y >= brick.top and self.ball_right_x >= brick.left and self.ball_left_x <= brick.right:
                print("IMPACT Top")
                self.ball_yv = self.ball_yv * -1
                self.ball_last_top_y = self.ball_top_y
                self.ball_last_bottom_y = self.ball_bottom_y

                self.ball_top_y = brick.top - 20
                self.ball_bottom_y = brick.top

            # Left

            elif self.ball_right_x >= brick.left and self.ball_left_x <= brick.left and self.ball_top_y <= brick.bottom and self.ball_bottom_y >= brick.top:
                print("IMPACT Left")
                self.ball_xv = self.ball_xv * -1
                self.ball_last_left_x = self.ball_left_x
                self.ball_last_right_x = self.ball_right_x

                self.ball_left_x = brick.left - 20
                self.ball_right_x = brick.left

            # Right


            self.canvas.delete(self.ball_obj)
            self.ball_obj = self.canvas.create_rectangle(
                self.ball_left_x, self.ball_top_y, self.ball_right_x, self.ball_bottom_y, 
                fill=BLUE_COLOR_LIGHT, outline=RED_COLOR
            )
            return


    def update_game(self):
        self.update_ball()
        # self.check_bricks()

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