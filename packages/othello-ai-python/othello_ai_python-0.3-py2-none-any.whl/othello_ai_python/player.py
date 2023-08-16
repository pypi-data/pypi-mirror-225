import keras
from keras.layers import BatchNormalization, Dense, Activation, Conv2D, Flatten
from keras.layers import Input, Add
from keras.optimizers import Adam
import random
import numpy as np
from othello_ai_python.board import *
from othello_ai_python.alphabeta import AlphaBeta, process
import os
import json
from othello_ai_python.config import *
# import othello_ai_python as othello

def rotate_array(array):
    array[0] = rotate_90(array[0])
    array[1] = rotate_90(array[1])
    array[2] = rotate_90(array[2])

    return array


def rotate_90(array):
    # Array is a 8x8 array.
    # ccw rotation
    size = len(array)

    new_array = []

    for i in range(size):
        row = []
        for j in range(size):
            row.append(array[size - 1 - j][i])
        new_array.append(row)

    return new_array

def reverse(board):
    size = len(board[0])
    newBoard = [[0 for i in range(size)] for j in range(size)]
    d = {0: 0, 1: -1, -1: 1}
    for i in range(size):
        for j in range(size):
            newBoard[i][j] = d[board[i][j]]

    return newBoard


class Player:
    def __init__(self, index, depth, path, parent=None, learning_rate=0.00005, epsilon=2):
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.experience = []
        self.parent = parent
        self.index = index
        self.depth = depth
        self.iterative = True
        self.path = path
        self.loss_tracker = []

        self.create_model()
        # self.load_total_history()

        self.decision_tree = AlphaBeta(self.parent)

    def create_model(self):
        main_input = Input(shape=(3, board_size, board_size))

        c1 = Conv2D(layer_size, (3, 3), activation='relu', padding='same')(main_input)
        b1 = BatchNormalization()(c1)
        c2 = Conv2D(layer_size, (3, 3), activation='relu', padding='same')(b1)
        b2 = BatchNormalization()(c2)
        c3 = Conv2D(layer_size, (3, 3), activation='relu', padding='same')(b2)
        b3 = BatchNormalization()(c3)

        a3 = Add()([b3, b1])

        c4 = Conv2D(layer_size, (3, 3), activation='relu', padding='same')(a3)
        b4 = BatchNormalization()(c4)
        c5 = Conv2D(layer_size, (3, 3), activation='relu', padding='same')(b4)
        b5 = BatchNormalization()(c5)

        a5 = Add()([b5, a3])

        b6 = Conv2D(layer_size, (3, 3), activation='relu', padding='same')(a5)

        f1 = Flatten()(b6)
        d1 = Dense(layer_size, activation='relu')(f1)
        d2 = Dense(1, activation='tanh')(d1)

        self.model = keras.models.Model(inputs=main_input, outputs=d2)

        self.model.compile(Adam(self.learning_rate), "mse")

    def add_to_history(self, state_array, reward):
        game_states = []
        history = self.experience

        current_reward = reward

        processed_array = []

        for i in range(len(state_array)):
            processed_array.append(process(state_array[i]))

        state_array = processed_array

        for i in range(len(state_array)):
            current_array = state_array[len(state_array) - i - 1]

            game_states.append([current_array,
                            current_reward])
            current_array = rotate_array(current_array)
            game_states.append([current_array,
                            current_reward])
            current_array = rotate_array(current_array)
            game_states.append([current_array,
                            current_reward])
            current_array = rotate_array(current_array)
            game_states.append([current_array,
                            current_reward])
            current_reward *= reward_decay
        history.extend(game_states)
        # self.total_history.append(game_states)
        # self.save_game_to_total_history(game_states)

    def wipe_history(self):
        self.experience = []

    def train_model(self):
        inputs = []
        answers = []
        history = self.experience

        for i in range(batch_size):
            lesson = random.choice(history)
            inputs.append(lesson[0])
            answers.append(lesson[1])

        inputs = np.array(inputs)
        answers = np.array(answers)
        self.model.fit(x=inputs, y=answers)

        # Saves the model's weights.

    def save(self, s):
        self.model.save(s)

    # Loads the weights of a previous model.
    def load(self, s):
        self.model = keras.models.load_model(s)

    def policy(self, board, color):

        possible_moves = board.moves(color)

        if (len(possible_moves) == 0):
            return pass_move

        variation = random.random()

        if (variation < 1 / self.epsilon):
            self.epsilon += epsilon_increment
            return random.choice(possible_moves)
        else:
            move = self.decision_tree.search(board, self.depth, color, self.index, iterative=self.iterative)

            if (move == None):
                return pass_move
            return move

    def load_total_history(self):
        self.total_history = []
        history_folder = size_folder + self.path + "/Total_History"
        if os.path.exists(history_folder):
            game_files = os.listdir(history_folder)
            game_files.sort()
            for game_file in game_files:
                with open(history_folder + "/"+ game_file, "r") as file:
                    self.total_history.append(json.load(file))

    def save_game_to_total_history(self, game):
        history_folder = size_folder + self.path + "/Total_History"
        if not os.path.exists(history_folder):
            # Create the folder
            os.makedirs(history_folder)
        game_index = self.total_history.index(game)
        game_file = history_folder + "/game_"+str(game_index + 1) + ".json"
        if os.path.exists(game_file):
            with open(game_file, "w") as file:
                json.dump(game, file)
        else:
            with open(game_file, "a") as file:
                json.dump(game, file)


class RandomPlayer(Player):
    def __init__(self):
        pass

    def add_to_history(self, state_array, reward):
        pass

    def wipe_history(self):
        pass

    def train_model(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def policy(self, observation, color):

        possibleMoves = Board.find_moves(observation, color)

        if (len(possibleMoves) == 0):
            return pass_move

        return random.choice(possibleMoves)


class BasicPlayer(RandomPlayer):
    def __init__(self):
        self.board = Board()
        self.weights = [[1000, 50, 100, 100, 100, 100, 50, 1000],
                        [50, -20, -10, -10, -10, -10, -20, 50],
                        [100, -10, 1, 1, 1, 1, -10, 100],
                        [100, -10, 1, 1, 1, 1, -10, 100],
                        [100, -10, 1, 1, 1, 1, -10, 100],
                        [100, -10, 1, 1, 1, 1, -10, 100],
                        [50, -20, -10, -10, -10, -10, -20, 50],
                        [1000, 50, 100, 100, 100, 100, 50, 1000]]

    def calculateScore(self, board):

        score = 0
        for i in range(board_size):
            for j in range(board_size):
                score += board.bits_to_board()[i][j] * self.weights[i][j]
        return score

    def policy(self, board, color):

        possibleMoves = board.moves(color)

        bestScore = -1000
        bestMove = (-1, -1)

        for move in possibleMoves:
            new_board = board
            new_board = new_board.move(move, color)
            tempScore = self.calculateScore(new_board)
            if (tempScore > bestScore):
                bestScore = tempScore
                bestMove = move

        return bestMove