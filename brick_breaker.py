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

    def key_input(self):
        return

    def mouse_input(self):
        return
    
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
        x1 = 700
        y1 = 725 
        x2 = 500
        y2 = 700
        self.paddle_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=RED_COLOR_LIGHT, outline=BLUE_COLOR
        )

    def initialize_bricks(self):
        return

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                if not self.crashed:
                    self.window.after(DELAY, self.update_snake(self.last_key))
                else:
                    self.begin = False
                    self.display_gameover()


game_instance = BrickBreaker()
game_instance.mainloop()