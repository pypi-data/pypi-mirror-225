board_size = None
pass_move = None
bit_positions = None
bit_moves = None
org_bit_board_black = 0b0
org_bit_board_white = 0b0
z = None
size_folder = None

board_size = 8
pass_move = board_size * board_size
bit_positions = [[y * board_size + x for x in range(board_size)] for y in range(board_size)]
bit_moves = [(0b1 << i) for i in range(board_size * board_size)]
org_bit_board_black = 0b0
org_bit_board_white = 0b0
z = (board_size - 2) // 2
org_bit_board_black |= bit_moves[bit_positions[board_size - 1 - z][z]]
org_bit_board_black |= bit_moves[bit_positions[z][board_size - 1 - z]]
org_bit_board_white |= bit_moves[bit_positions[z][z]]
org_bit_board_white |= bit_moves[bit_positions[board_size - 1 - z][board_size - 1 - z]]
size_folder = str(board_size) + "x" + str(board_size) + "/"


num_processes = 4
num_threads = 2

# episodes = 10000
# seconds = 77.4
# days = episodes * seconds / (60 * 60 * 24)
# print(days)

def create_board_vars(board_size):
    pass_move = board_size * board_size
    bit_positions = [[y * board_size + x for x in range(board_size)] for y in range(board_size)]
    bit_moves = [(0b1 << i) for i in range(board_size * board_size)]
    org_bit_board_black = 0b0
    org_bit_board_white = 0b0
    z = (board_size - 2) // 2
    org_bit_board_black |= bit_moves[bit_positions[board_size - 1 - z][z]]
    org_bit_board_black |= bit_moves[bit_positions[z][board_size - 1 - z]]
    org_bit_board_white |= bit_moves[bit_positions[z][z]]
    org_bit_board_white |= bit_moves[bit_positions[board_size - 1 - z][board_size - 1 - z]]
    size_folder = str(board_size) + "x" + str(board_size) + "/"

# create_board_vars(8)
batch_size = 64
reward_decay = 0.99
layer_size = 256
# population_size = 2
epsilon_increment = 0.001

wipe_frequency = 2
save_frequency = 100