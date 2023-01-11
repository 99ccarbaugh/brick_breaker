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
Green_color = "#7BC043"
BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'

TOP_BOUND = 0
BOTTOM_BOUND = 800
LEFT_BOUND = 0
RIGHT_BOUND = 1200


PADDLE_START_X1 = 700
PADDLE_START_Y1 = 725
PADDLE_START_X2 = 500
PADDLE_START_Y2 = 700

PADDLE_TOP = 700

# Normal
# BALL_START_X1 = 590
# BALL_START_Y1 = 680
# BALL_START_X2 = 610
# BALL_START_Y2 = 700

#Debug
BALL_START_X1 = 590
BALL_START_Y1 = 640
BALL_START_X2 = 610
BALL_START_Y2 = 660

BALL_START_XV = 0
BALL_START_YV = 1

PADDLE_MOVE_SPEED = 30
BALL_MOVE_SPEED = 30



class BrickBreaker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Brick Breaker")
        self.canvas = tk.Canvas(self.window, width=1200, height=800)
        self.canvas.pack()
        self.window.bind("<Key>", self.key_input)
        self.window.bind("<Button-1>", self.mouse_input)
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
        # self.initialize_board()
        self.initialize_paddle()
        self.initialize_ball()
        self.initialize_bricks()

    def initialize_paddle(self):
        self.paddle_heading = "None"
        self.paddle_x1 = PADDLE_START_X1
        self.paddle_y1 = PADDLE_START_Y1 
        self.paddle_x2 = PADDLE_START_X2
        self.paddle_y2 = PADDLE_START_Y2
        self.paddle_obj = self.canvas.create_rectangle(
            self.paddle_x1, self.paddle_y1, self.paddle_x2, self.paddle_y2, 
            fill=RED_COLOR_LIGHT, outline=BLUE_COLOR
        )

    def initialize_ball(self):
        # Save ball initial coordinates as global variables
        # will need ball current position, past position from last iteration and x,y vel
        self.ball_x1 = BALL_START_X1
        self.ball_y1 = BALL_START_Y1
        self.ball_x2 = BALL_START_X2
        self.ball_y2 = BALL_START_Y2

        self.ball_last_x1 = BALL_START_X1
        self.ball_last_y1 = BALL_START_Y1
        self.ball_last_x2 = BALL_START_X2
        self.ball_last_y2 = BALL_START_Y2

        self.ball_xv = BALL_START_XV
        self.ball_yv = BALL_START_YV

        self.ball_obj = self.canvas.create_rectangle(
            self.ball_x1, self.ball_y1, self.ball_x2, self.ball_y2, 
            fill=BLUE_COLOR_LIGHT, outline=RED_COLOR
        )

    # X1Y1 is top left, X2Y2 is bottom right
    def update_ball(self):
        self.ball_last_x1 = self.ball_x1
        self.ball_last_y1 = self.ball_y1
        self.ball_last_x2 = self.ball_x2
        self.ball_last_y2 = self.ball_y2
        self.canvas.delete(self.ball_obj)

        # Normal Update
        self.ball_x1 = self.ball_last_x1 + (self.ball_xv * BALL_MOVE_SPEED)
        self.ball_y1 = self.ball_last_y1 + (self.ball_yv * BALL_MOVE_SPEED)
        self.ball_x2 = self.ball_last_x2 + (self.ball_xv * BALL_MOVE_SPEED)
        self.ball_y2 = self.ball_last_y2 + (self.ball_yv * BALL_MOVE_SPEED)

        # Impacts with walls
        
        # Impact with top
        if self.ball_y1 <= TOP_BOUND:
            self.ball_y1 = 0
            self.ball_y2 = 20
            self.ball_yv = self.ball_yv * -1


        # Impact with Left
        if self.ball_x1 <= LEFT_BOUND:
            self.ball_x1 = 0
            self.ball_x2 = 20
            self.ball_xv = self.ball_xv * -1

        # Impact with right
        if self.ball_x2 >= RIGHT_BOUND:
            self.ball_x1 = 1180
            self.ball_x2 = 1200
            self.ball_xv = self.ball_xv * -1

        
        # Impact with Paddle
        if (self.ball_y2 >= PADDLE_TOP and self.ball_x1 >= self.paddle_x2 and self.ball_x2 <= self.paddle_x1):
            print(PADDLE_TOP, "BEFORE IMPACT y1: %d, y2: %d" % (self.ball_y1, self.ball_y2))
            self.ball_y1 = PADDLE_TOP - 20
            self.ball_y2 = PADDLE_TOP
            self.ball_yv = self.ball_yv * -1
            print("AFTER IMPACT y1: %d, y2: %d" % (self.ball_y1, self.ball_y2))

        self.ball_obj = self.canvas.create_rectangle(
            self.ball_x1, self.ball_y1, self.ball_x2, self.ball_y2, 
            fill=BLUE_COLOR_LIGHT, outline=RED_COLOR
        )

        
    # Done goofed - X1Y1 is top right, X2Y2 is bottom left
    def update_paddle(self, key):

        if key == 'Right':
            if self.paddle_x1 + PADDLE_MOVE_SPEED <= 1200:
                self.paddle_x1 += PADDLE_MOVE_SPEED
                self.paddle_x2 += PADDLE_MOVE_SPEED
            else:
                self.paddle_x1 = 1200
                self.paddle_x2 = 1000
        if key == 'Left':
            if self.paddle_x2 - PADDLE_MOVE_SPEED >= 0:
                self.paddle_x1 -= PADDLE_MOVE_SPEED
                self.paddle_x2 -= PADDLE_MOVE_SPEED
            else:
                self.paddle_x1 = 200
                self.paddle_x2 = 0

        self.canvas.delete(self.paddle_obj)
        self.paddle_obj = self.canvas.create_rectangle(
            self.paddle_x1, self.paddle_y1, self.paddle_x2, self.paddle_y2, 
            fill=RED_COLOR_LIGHT, outline=BLUE_COLOR
        )

    def initialize_bricks(self):
        return

    def update_game(self):
        self.update_paddle(self.last_key)
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