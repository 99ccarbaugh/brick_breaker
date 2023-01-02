# Author: 99ccarbaugh
# Created: 12/31/22
# Email: chasecarbaugh@gmail.com


import tkinter as tk
import random
import time
import numpy as np

class BrickBreaker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Brick Breaker")
        self.canvas = tk.Canvas(self.window, width=1200, height=800).pack()
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
        self.initialize_board()
        self.initialize_paddle()
        self.initialize_bricks()

    def initialize_board(self):
        return

    def initialize_paddle(self):
        return

    def initialize_bricks(self):
        return