from othello_ai_python.canvas import Canvas
from othello_ai_python.engine import *
import math


class Arena:
    def __init__(self):
        self.screen = Canvas()

        self.env = Board()
        self.env.reset()
        self.screen.set_board(self.env, 1)

        self.controller = Controller(2, epsilon=math.inf)
        self.playing = True

    def move(self, index1, index2, color):

        players = [self.controller.population[index1], self.controller.population[index2]]

        d = {1: 0, -1: 1}
        e = {0: 1, 1: -1}

        # Chose a move and take it

        move = players[d[color]].policy(self.env, color)

        self.env, reward, done, info = self.env.step(move, color)
        self.screen.update(self.env, color)
        return not done, reward

    def play(self):
        playing = True
        self.screen.draw_board()
        self.screen.check_for_quit()
        reward = 0

        while (playing):
            playing, reward = self.move(0, 1, 1)
            if(not playing):
                break
            self.screen.draw_board()
            self.screen.check_for_quit()
            playing, reward = self.move(0, 1, -1)
            if(not playing):
                break
            self.screen.draw_board()
            self.screen.check_for_quit()
        print(reward)
        self.screen.draw_board()
        time.sleep(3)
