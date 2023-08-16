import pygame
from othello_ai_python.engine import Controller
from othello_ai_python.canvas import Canvas
from othello_ai_python.arena import Arena
from othello_ai_python.againstAi import Session

class Interface():
    def __init__(self):
        self.canvas = Canvas()

    def start(self):
        text = "Press t to train, h to play against the AI, and a to play AI against AI"
        keys = {pygame.K_t: "t", pygame.K_h: "h", pygame.K_a: "a"}
        key = self.canvas.waiting_screen(text, keys)
        if(key == "t"):
            self.train()
        elif(key == "h"):
            self.human_against_ai()
        elif(key == "a"):
            self.ai_against_ai()

    def train(self):
        text = "Enter the amount of episodes you want to run: "
        episodes = self.canvas.waiting_screen(text, return_number=True)
        text = "Enter the learning rate you want the Neural Network to have: "
        learning_rate = self.canvas.waiting_screen(text, return_number=True)
        controller = Controller(2, learning_rate=learning_rate)
        controller.train(start_episode=0, episodes=300, save_frequency=50, wipe_frequency=2, graph_frequency=25)

    def human_against_ai(self):
        session = Session()
        session.play()

    def ai_against_ai(self):
        arena = Arena()
        arena.play()
#
# interface = Interface()
# while True:
#     interface.start()