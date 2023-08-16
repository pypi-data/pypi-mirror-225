import numpy as np
from othello_ai_python.config import *
import math


def process(array):
    size = len(array[0])
    new_array = []
    pieces = [0, 1, -1]

    for i in range(3):
        board = []
        for j in range(size):
            row = []
            for k in range(size):
                row.append(int(array[j][k] == pieces[i]))
            board.append(row)
        new_array.append(board)

    return new_array


def reverse(board):
    size = len(board[0])
    newBoard = [[0 for i in range(size)] for j in range(size)]
    d = {0: 0, 1: -1, -1: 1}
    for i in range(size):
        for j in range(size):
            newBoard[i][j] = d[board[i][j]]

    return newBoard


class AlphaBeta:
    def __init__(self, controller):
        self.controller = controller

    def search(self, board, depth, color, index, iterative=True):
        alpha = -math.inf
        beta = math.inf
        if(iterative):
            best_move = None
            best_value = -math.inf * color
            for iterative_depth in range(1, depth + 1):
                value, move = self.alphabeta(board, iterative_depth, alpha, beta, color, index, False)
                if(value * color > best_value * color):
                    best_move = move
                    best_value = value
            return best_move
        else:
            _, move = self.alphabeta(board, depth, alpha, beta, color, index, False)
            return move

    def policy(self, board, color, index):
        processedBoard = process(board.bits_to_board())
        processedBoard = np.array([processedBoard])
        return self.controller.population[index].model.predict(processedBoard)[0][0]

    def alphabeta(self, board, depth, alpha, beta, color, index, done):
        if (depth == 0 or done):
            return self.policy(board, color, index), None

        moves = board.moves(color)

        if len(moves) == 0:
            move = pass_move
            newboard, _, done, _ = board.step(move, color)
            score, m = self.alphabeta(newboard, depth - 1, alpha, beta, -color, index, done)

            return score, m

        if (color == 1):
            return_move = None

            for move in moves:
                newboard, _, done, _ = board.step(move, color)

                score, m = self.alphabeta(newboard, depth - 1, alpha, beta, -1, index, done)

                if (score > alpha):
                    alpha = score
                    return_move = move

                if (beta <= alpha):
                    break
            return alpha, return_move
        elif (color == -1):
            return_move = None

            for move in moves:
                newboard, _, done, _ = board.step(move, color)

                score, m = self.alphabeta(newboard, depth - 1, alpha, beta, 1, index, done)

                if (score < beta):
                    beta = score
                    return_move = move

                if (beta <= alpha):
                    break
            return beta, return_move
        else:
            print("Error in AlphaBeta, Color is not 1 or -1")
            print("Color is: " + color)
            raise (Exception("Color Error in Alpha Beta"))
