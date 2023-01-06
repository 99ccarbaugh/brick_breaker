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
START_X1 = 700
START_Y1 = 725
START_X2 = 500
START_Y2 = 700
MOVEMENT_SPEED = 30

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
        self.initialize_bricks()



    # def initialize_board(self):
        # self.board = []
        # self.apple_obj = []
        # self.old_apple_cell = []

        # for i in range(rows):
        #     for j in range(cols):
        #         self.board.append((i, j))

        # for i in range(rows):
        #     self.canvas.create_line(
        #         i * size_of_board / rows, 0, i * size_of_board / rows, size_of_board,
        #     )

        # for i in range(cols):
        #     self.canvas.create_line(
        #         0, i * size_of_board / cols, size_of_board, i * size_of_board / cols,
        #     )

    def initialize_paddle(self):
        self.paddle = []
        self.paddle_heading = "None"
        self.paddle_x1 = 700
        self.paddle_y1 = 725 
        self.paddle_x2 = 500
        self.paddle_y2 = 700
        self.paddle_obj = self.canvas.create_rectangle(
            self.paddle_x1, self.paddle_y1, self.paddle_x2, self.paddle_y2, 
            fill=RED_COLOR_LIGHT, outline=BLUE_COLOR
        )

    def update_paddle(self, key):
        print(key)
        if key == 'Right':
            if self.paddle_x1 + MOVEMENT_SPEED <= 1200:
                self.paddle_x1 += MOVEMENT_SPEED
                self.paddle_x2 += MOVEMENT_SPEED
            else:
                self.paddle_x1 = 1200
                self.paddle_x2 = 1000
        if key == 'Left':
            if self.paddle_x2 - MOVEMENT_SPEED >= 0:
                self.paddle_x1 -= MOVEMENT_SPEED
                self.paddle_x2 -= MOVEMENT_SPEED
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

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                self.window.after(DELAY, self.update_paddle(self.last_key))
                self.last_key = "None"
                # Define end state later
                # else:
                #     self.begin = False
                #     self.display_gameover()


game_instance = BrickBreaker()
game_instance.mainloop()