from othello_ai_python.canvas import *
from othello_ai_python.engine import *
import math


class Session():
    def __init__(self):
        self.env = Board()
        self.env.reset()

        self.canvas = Canvas()
        self.canvas.set_board(self.env, 1)

        self.controller = Controller(1, epsilon=math.inf)

    def move(self, color):
        if(color == 1):
            move = self.canvas.return_move()
        else:
            move = self.controller.population[0].policy(self.env, color)
        self.env, reward, done, info = self.env.step(move, color)
        self.canvas.update(self.env, color*-1)
        moving = True
        if(done):
            moving = False
        return moving

    def play(self):
        self.controller.load()
        self.controller.population[0].depth = 3

        moving = True

        self.canvas.draw_board()
        self.canvas.check_for_quit()

        while moving:
            moving = self.move(1)
            self.canvas.draw_board()
            self.canvas.check_for_quit()
            moving = self.move(-1)
            self.canvas.draw_board()
            self.canvas.check_for_quit()
