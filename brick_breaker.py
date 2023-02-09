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

# Debug - above paddle
BALL_START_LEFT_X = 590
BALL_START_TOP_Y = 500
BALL_START_RIGHT_X = 610
BALL_START_BOTTOM_Y = 520

# # Debug - Right of paddle
# BALL_START_LEFT_X = 800
# BALL_START_TOP_Y = 700
# BALL_START_RIGHT_X = 820
# BALL_START_BOTTOM_Y = 720

BALL_HEIGHT = 20
BALL_WIDTH = 20

BALL_START_XV = 0
BALL_START_YV = 1

PADDLE_MOVE_SPEED = 30
BALL_MOVE_SPEED = 30

BRICK_HEIGHT = 25
BRICK_WIDTH = 55
BRICK_ROWS = 4
BRICK_OFFSET = 0
BRICK_START_X = 50
BRICK_START_Y = 100
BRICKS_PER_ROW = 20

class RectObj:
    def __init__(self, id, left, right, top, bottom, fill_color, border_color, canvas):
        self.id = id
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.fill_color = fill_color
        self.border_color = border_color
        self.rect_obj = None

        self.draw_rect(canvas)

    def draw_rect(self, canvas):
        if self.rect_obj != None:
            canvas.delete(self.rect_obj)
        self.rect_obj = canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
        fill=self.fill_color, outline=self.border_color)

    def debug_rect(self):
        print("Left: %s, right: %s, top: %s, bottom: %s" % (self.left, self.right, self.top, self.bottom))

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

        self.x_vel = BALL_START_XV
        self.y_vel = BALL_START_YV

        self.fill_color = fill_color
        self.border_color = border_color
        self.ball_obj = None

        self.draw_ball(canvas)

    def draw_ball(self, canvas):
        if self.ball_obj != None:
            canvas.delete(self.ball_obj)
        self.ball_obj = canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
        fill=self.fill_color, outline=self.border_color)

    def debug_ball(self):
        print("last left: %s, last right: %s, last top: %s, last bottom: %s\nLeft: %s, right: %s, top: %s, bottom: %s\n" % (self.last_left, self.last_right, self.last_top, self.last_bottom,
        self.left, self.right, self.top, self.bottom))

    

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
            

    # Obj can be either paddle or brick
    # Returns face of obj that was struck (Left, Right, Top, Bottom)\
    # Should this be a member of the RectObj Class?
    def check_overlap(self, obj):
        # if statement to see if ball is overlapping with the paddle
        width_positive = min(self.ball.right, obj.right) >= max(self.ball.left, obj.left)
        height_positive = min(self.ball.bottom, obj.bottom) >= max(self.ball.top, obj.top)
        return width_positive and height_positive
       

    # Function checks if the ball has impacted the paddle, if so, it returns the side of the paddle that
    #   was hit
    def check_paddle_impact(self):
        
        ball_paddle_overlap = self.check_overlap(self.paddle)
        # print("width: %s, height: %s, overlap: %s" % (width_positive, height_positive, ball_paddle_overlap))
        if ball_paddle_overlap:
            print('--------IMPACT---------')
            last_width_positive = min(self.ball.last_right, self.paddle.right) >= max(self.ball.last_left, self.paddle.left)
            last_height_positive = min(self.ball.last_bottom, self.paddle.bottom) >= max(self.ball.last_top, self.paddle.top)
            print("Last width: %s, last height: %s" % (last_width_positive, last_height_positive))

            # Impact made on side, need to determine which side
            if(not last_width_positive):
                # If we know the impact was on left or right, and left of ball is left of paddle's left before impact, must hit left 
                if self.ball.last_left < self.paddle.left:
                    return "left"
                else:
                    return "right"
            # Impact made on top or bottom
            elif(not last_height_positive):
                # If we know the impact was on top or bottom, and top of ball is above of paddle's top before impact, must hit top
                if self.ball.last_top < self.paddle.top:
                    return "top"
                else:
                    return "bottom"
            # Should not happen
            else:
                print("How did that happen?")
                return "none"
        else:
            return "none"

    def check_bricks(self):
            for brick_id in self.bricks:
                brick = self.bricks[brick_id]
                ball_brick_overlap = self.check_overlap(brick)
                if ball_brick_overlap:
                    print("BRICK %d HIT" %(brick.id))
                    last_width_positive = min(self.ball.last_right, brick.right) >= max(self.ball.last_left, brick.left)
                    last_height_positive = min(self.ball.last_bottom, brick.bottom) >= max(self.ball.last_top, brick.top)
                    print("Last width: %s, last height: %s" % (last_width_positive, last_height_positive))
                    bounce_dir = "none"
                    # Impact made on side, need to determine which side
                    if(not last_width_positive):
                        # If we know the impact was on left or right, and left of ball is left of paddle's left before impact, must hit left 
                        if self.ball.last_left < brick.left:
                            bounce_dir = "left"
                        else:
                            bounce_dir = "right"
                    # Impact made on top or bottom
                    elif(not last_height_positive):
                        # If we know the impact was on top or bottom, and top of ball is above of paddle's top before impact, must hit top
                        if self.ball.last_top < brick.top:
                            bounce_dir = "top"
                        else:
                            bounce_dir = "bottom"
                    # Should not happen
                    else:
                        print("How did that happen?")
                        bounce_dir = "none"
                else:
                    bounce_dir = "none"

                if bounce_dir != "none":
                    print("BRICK FACE: ", bounce_dir)
                    self.ball.last_left = self.ball.left
                    self.ball.last_top = self.ball.top
                    self.ball.last_right = self.ball.right
                    self.ball.last_bottom = self.ball.bottom

                    if bounce_dir == "top":
                        self.ball.top = brick.top - BALL_HEIGHT
                        self.ball.bottom = brick.top
                    if bounce_dir == "bottom":
                        self.ball.top = brick.bottom
                        self.ball.bottom = brick.bottom + BALL_HEIGHT
                    if bounce_dir == "left":
                        self.ball.left = brick.left - BALL_WIDTH
                        self.ball.right = brick.left
                    if bounce_dir == "right":
                        self.ball.left = brick.right
                        self.ball.right = brick.right + BALL_WIDTH

                    self.update_ball_vels(bounce_dir)
                    self.update_bricks(brick_id)
                    break
                    


    # X1Y1 is top left, X2Y2 is bottom right
    def update_ball(self):
        self.ball.last_left = self.ball.left
        self.ball.last_top = self.ball.top
        self.ball.last_right = self.ball.right
        self.ball.last_bottom = self.ball.bottom
        # self.canvas.delete(self.ball.ball_obj)

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

        bounce_dir = "none"
        bounce_dir = self.check_paddle_impact()
        if bounce_dir == "none":
            self.check_bricks()
        else:
            print(bounce_dir)
            if bounce_dir == "top":
                self.ball.top = self.paddle.top - BALL_HEIGHT
                self.ball.bottom = self.paddle.top
            if bounce_dir == "bottom":
                self.ball.top = self.paddle.bottom
                self.ball.bottom = self.paddle.bottom + BALL_HEIGHT
            if bounce_dir == "left":
                self.ball.left = self.paddle.left - BALL_WIDTH
                self.ball.right = self.paddle.left
            if bounce_dir == "right":
                self.ball.left = self.paddle.right
                self.ball.right = self.paddle.right + BALL_WIDTH

            self.update_ball_vels_paddle(bounce_dir)

        if self.ball.bottom >= BOTTOM_BOUND:
            self.game_over = True
        
        self.ball.draw_ball(self.canvas)


    def mouse_input(self, event):
        self.play_again()
    
    def play_again(self):
        self.canvas.delete("all")
        self.initialize_game_objs()

    def initialize_game_objs(self):
        self.game_over = False
        # Initialize paddle
        self.paddle = Paddle(0, PADDLE_START_LEFT_X, PADDLE_START_RIGHT_X, PADDLE_START_TOP_Y, PADDLE_START_BOTTOM_Y,
            RED_COLOR_LIGHT, BLUE_COLOR, self.canvas)
        # Initialize ball
        self.ball = Ball(0, BALL_START_LEFT_X, BALL_START_RIGHT_X, BALL_START_TOP_Y, BALL_START_BOTTOM_Y,
            BLUE_COLOR_LIGHT, RED_COLOR, self.canvas)
        # Initialize Bricks
        self.initialize_bricks()
        return
   
    def update_ball_vels(self, bounce_dir):
            # Get x value for center of ball
            if bounce_dir == "top":
                self.ball.y_vel = self.ball.y_vel * -1
            if bounce_dir == "bottom":
                self.ball.y_vel = self.ball.y_vel * -1
            if bounce_dir == "left" or bounce_dir == "right":
                self.ball.x_vel = self.ball.x_vel * -1


    def update_ball_vels_paddle(self, bounce_dir):
        # Get x value for center of ball
        if bounce_dir == "top":
            ball_center = int((self.ball.right + self.ball.left) /2)
            # Adjust center value to be relative to a hypothetical paddle from 0 to 200
            ball_center_relative = ball_center - self.paddle.left
            ball_dist = ball_center_relative - 100
            ball_dist_scaled = int(ball_dist / 10)
            # print("Ball center relative: %d\nBall dist: %d\nBall dist scaled: %d" %(ball_center_relative, ball_dist, ball_dist_scaled))
            self.ball.x_vel = ball_dist_scaled / 10
            self.ball.y_vel = self.ball.y_vel * -1
        if bounce_dir == "bottom":
            self.ball.y_vel = self.ball.y_vel * -1
        if bounce_dir == "left" or bounce_dir == "right":
            self.ball.y_vel = -1
            self.ball.x_vel = self.ball.x_vel * -1
        

    # Done goofed - X1Y1 is top right, X2Y2 is bottom left

    def update_paddle(self, mouse_x):
        paddle_center = (self.paddle.left + self.paddle.right) / 2
        x_delta = mouse_x - paddle_center
        self.paddle.left += x_delta
        self.paddle.right += x_delta
        
        self.paddle.draw_rect(self.canvas)

    def motion(self, event):
        if not self.game_over:
            self.update_paddle(event.x)

    def initialize_bricks(self):
        self.bricks = {}
        cur_brick_x = BRICK_START_X
        cur_brick_y = BRICK_START_Y
        for i in range(0, BRICK_ROWS):
            for j in range(0, BRICKS_PER_ROW):
                # X1 X2 Y1 Y2
                self.bricks[len(self.bricks)] = Brick(len(self.bricks), cur_brick_x, cur_brick_x + BRICK_WIDTH, cur_brick_y, cur_brick_y + BRICK_HEIGHT, GREEN_COLOR, BLUE_COLOR_LIGHT, self.canvas)
                cur_brick_x += BRICK_WIDTH
            cur_brick_x = BRICK_START_X    
            cur_brick_y += BRICK_HEIGHT

    def update_bricks(self, dead_brick):
        for brick_id in self.bricks:
            self.canvas.delete(self.bricks[brick_id].rect_obj)
        self.bricks.pop(dead_brick) 
        for brick_id in self.bricks:
            self.bricks[brick_id].draw_rect(self.canvas)
        if len(self.bricks) == 0:
            self.game_over = True

    def update_game(self):
        self.update_ball()
        self.check_bricks()

    def display_gameover(self):
        self.canvas.delete("all")
        score_text = "Game Over\nClick to play again \n"
        self.canvas.create_text(
            400,
            600,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                if not self.game_over:
                    self.window.after(DELAY, self.update_game())
                    self.last_key = "None"
                else:
                    self.begin = False
                    self.display_gameover()


game_instance = BrickBreaker()
game_instance.mainloop()