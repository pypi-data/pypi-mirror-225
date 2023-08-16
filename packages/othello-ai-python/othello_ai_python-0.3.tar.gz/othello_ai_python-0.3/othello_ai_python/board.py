import copy
from othello_ai_python.config import *

class Board:

    def __init__(self):
        self.reset()
        self._create_masks()

    def _create_masks(self):
        self.left_right_mask = 0b0
        self.top_bottom_mask = 0b0
        for i in range(board_size):
            for j in range(board_size):
                bit_piece = bit_moves[bit_positions[i][j]]
                if(0 < j < board_size - 1):
                    self.left_right_mask |= bit_piece
                if(0 < i < board_size - 1):
                    self.top_bottom_mask |= bit_piece

        self.corner_mask = self.left_right_mask & self.top_bottom_mask

    # def to_bit(self, color):
    #     bit_board = 0
    #     for y in range(size):
    #         for x in range(size):
    #             if self.board[y][x] == color:
    #                 bit_board |= setup.bit_moves[setup.bit_positions[y][x]]
    #     return bit_board

    def bits_to_board(self):
        array_black = self._bit_to_array(self.bit_board_black)
        array_white = self._bit_to_array(self.bit_board_white)
        board = [[array_black[bit_positions[i][j]] - array_white[bit_positions[i][j]] for j in range(board_size)] for i in range(board_size)]
        return board

    def _bit_to_array(self, bit_board):
        size = board_size * board_size
        board = [int(x) for x in list(reversed((("0" * size) + bin(bit_board)[2:])[-size:]))]
        return board

    def move(self, move, color):
        new = self.new()
        new.to_play *= -1
        if(move == pass_move):
            new.passes += 1
            return new
        player, opponent = self._find_player_and_opponent(color)
        flipped_pieces = new.get_flipped_pieces(move, player, opponent)
        if(flipped_pieces == 0b0):
            print(color)
            print(move)
            raise ValueError("Move is not Legal")
        bit_move = bit_moves[move]
        player |= flipped_pieces | bit_move
        opponent &= ~flipped_pieces
        if(color == 1):
            new.bit_board_black = player
            new.bit_board_white = opponent
        else:
            new.bit_board_black = opponent
            new.bit_board_white = player
        return new

    def moves(self, color):
        player, opponent = self._find_player_and_opponent(color)
        moves = 0b0
        moves |= self._get_moves_left(player, opponent, self.left_right_mask, 1)
        moves |= self._get_moves_left(player, opponent, self.corner_mask, board_size + 1)
        moves |= self._get_moves_left(player, opponent, self.top_bottom_mask, board_size)
        moves |= self._get_moves_left(player, opponent, self.corner_mask, board_size - 1)
        moves |= self._get_moves_right(player, opponent, self.left_right_mask, 1)
        moves |= self._get_moves_right(player, opponent, self.corner_mask, board_size + 1)
        moves |= self._get_moves_right(player, opponent, self.top_bottom_mask, board_size)
        moves |= self._get_moves_right(player, opponent, self.corner_mask, board_size - 1)
        moves &= ~(player | opponent)
        if(moves == 0b0):
            return [pass_move]
        moves = [position for position, is_move in enumerate(self._bit_to_array(moves)) if is_move]
        return moves

    def _get_moves_left(self, player, opponent, mask, offset):
        return self._get_line_left(player, opponent, mask, offset) >> offset

    def _get_moves_right(self, player, opponent, mask, offset):
        return self._get_line_right(player, opponent, mask, offset) << offset

    def get_flipped_pieces(self, move, player, opponent):
        bit_move = bit_moves[move]
        flipped = 0b0
        flipped |= self._get_flipped_pieces_left(bit_move, player, opponent, self.left_right_mask, 1)
        flipped |= self._get_flipped_pieces_left(bit_move, player, opponent, self.corner_mask, board_size + 1)
        flipped |= self._get_flipped_pieces_left(bit_move, player, opponent, self.top_bottom_mask, board_size)
        flipped |= self._get_flipped_pieces_left(bit_move, player, opponent, self.corner_mask, board_size - 1)
        flipped |= self._get_flipped_pieces_right(bit_move, player, opponent, self.left_right_mask, 1)
        flipped |= self._get_flipped_pieces_right(bit_move, player, opponent, self.corner_mask, board_size + 1)
        flipped |= self._get_flipped_pieces_right(bit_move, player, opponent, self.top_bottom_mask, board_size)
        flipped |= self._get_flipped_pieces_right(bit_move, player, opponent, self.corner_mask, board_size - 1)
        return flipped

    def _get_flipped_pieces_left(self, move, player, opponent, mask, offset):
        flipped = self._get_line_left(move, opponent, mask, offset)
        if(player & (flipped >> offset) == 0b0):
            return 0b0
        else:
            return flipped

    def _get_flipped_pieces_right(self, move, player, opponent, mask, offset):
        flipped = self._get_line_right(move, opponent, mask, offset)
        if (player & (flipped << offset) == 0):
            return 0
        else:
            return flipped

    def _get_line_left(self, move, opponent, mask, offset):
        o = opponent & mask
        s = o & (move >> offset)
        s |= o & (s >> offset)
        s |= o & (s >> offset)
        s |= o & (s >> offset)
        s |= o & (s >> offset)
        s |= o & (s >> offset)
        return s

    def _get_line_right(self, move, opponent, mask, offset):
        o = opponent & mask
        s = o & (move << offset)
        s |= o & (s << offset)
        s |= o & (s << offset)
        s |= o & (s << offset)
        s |= o & (s << offset)
        s |= o & (s << offset)
        return s

    # def reverse(self):
    #     d = {1: -1, 0: 0, -1: 1}
    #
    #     for i in range(len(self.board)):
    #         for j in range(len(self.board[i])):
    #             self.board[i][j] = d[self.board[i][j]]

    def _find_player_and_opponent(self, color):
        if(color == 1):
            return self.bit_board_black, self.bit_board_white
        return self.bit_board_white, self.bit_board_black

    def find_winner(self):
        positives = str(bin(self.bit_board_black)).count('1')
        negatives = str(bin(self.bit_board_white)).count('1')

        if (positives == negatives):
            return 0
        elif (positives > negatives):
            return 1
        else:
            return -1

    def step(self, move, color):
        # observation, reward, done, info
        reward = 0
        done = False
        new = self.move(move, color)
        if (self.passes >= 2):
            # Two passes in a row
            done = True
            reward = self.find_winner()
        return new, reward, done, {}

    def reset(self):
        self.passes = 0
        self.to_play = 1
        self.bit_board_black = org_bit_board_black
        self.bit_board_white = org_bit_board_white

    def new(self):
        return copy.deepcopy(self)

    def __str__(self):
        board = self.bits_to_board()
        seperation = ' '
        board_str = seperation * 3 + seperation.join([str(x) for x in range(board_size)]) + '\n' * 2
        d = {1: 1, -1: 2, 0: 0}
        for y in range(board_size):
            row = str(y) + seperation*2
            for x in range(board_size):
                row += str(d[board[y][x]])
                row += seperation
            row += '\n' if y < board_size - 1 else ''
            board_str += row
        return board_str

    def __getstate__(self):
        # Convert the current state of the board to a dictionary that will be pickled
        state = self.__dict__.copy()
        # Remove the masks from the state, as they are not pickleable
        state.pop('left_right_mask', None)
        state.pop('top_bottom_mask', None)
        state.pop('corner_mask', None)
        return state

    def __setstate__(self, state):
        # Reconstruct the object from the pickled state dictionary
        self.__dict__.update(state)
        # Recreate the masks using the existing method
        self._create_masks()

# def f1(val1, val2):
#     print(val1 + val2)
# args = [(1, 2), (3, 4), (5, 6), (7, 8)]
# t1 = time()
# for arg in args:
#     f1(*arg)
# t2 = time()
# print(t2 - t1)
# if __name__ == '__main__':
#     t1 = time()
#     with multiprocessing.Pool(processes=4) as pool:
#         pool.starmap(f1, args)
#     t2 = time()
#     print(t2 - t1)