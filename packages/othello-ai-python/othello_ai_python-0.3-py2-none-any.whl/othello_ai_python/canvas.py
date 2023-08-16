import pygame
import math
from othello_ai_python.config import *


class Canvas():
    def __init__(self, square_size=75):
        self.SQUARESIZE = square_size
        self.display_bottom = 150
        self.board_width = self.SQUARESIZE * board_size
        self.board_height = self.SQUARESIZE * board_size
        self.WIDTH = self.board_width
        self.HIEGHT = self.board_height + self.display_bottom
        self.FPS = 30

        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BG_COLOR = (10, 128, 14)

        # initalsize pygame and window
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HIEGHT))
        pygame.display.set_caption("Othello")
        self.clock = pygame.time.Clock()
        self.screen.fill(self.BG_COLOR)

        # starting cordinates of the board
        self.x = 0
        self.y = 0

        self.one_x_1 = self.SQUARESIZE
        self.one_y_1 = 0

        self.one_end_x = self.SQUARESIZE
        self.one_end_y = self.SQUARESIZE * board_size

        # Horizontal
        self.two_x_1 = 0
        self.two_y_1 = self.SQUARESIZE

        self.two_end_x = self.SQUARESIZE * board_size
        self.two_end_y = self.SQUARESIZE

        self.RADIUS = int(self.SQUARESIZE / 2 - 5)

        self.max_width = self.WIDTH - 20

    def waiting_screen(self, Text, triggers = {pygame.K_RETURN: "Enter"}):
        return_number = True if pygame.K_RETURN in triggers else False
        # Display the starting screen
        self.screen.fill(self.BG_COLOR)
        font = pygame.font.Font(None, 50)
        text = self._fit_text(font, Text, self.WHITE)
        text_width = text.get_width()
        text_height = text.get_height()
        text_x = (self.WIDTH - text_width) // 2
        text_y = (self.HIEGHT - text_height) // 2
        self.screen.blit(text, (text_x, text_y))
        pygame.display.update()

        # Wait for Enter key press

        number = ""
        waiting = True
        decimal_mode = False
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in triggers:
                        if(return_number):
                            if(len(number) > 0):
                                if decimal_mode and number.count('.') == 1 and number[-1] != '.':
                                    self.screen.fill(self.BG_COLOR)
                                    waiting = False
                                    return float(number)
                                elif not decimal_mode:
                                    self.screen.fill(self.BG_COLOR)
                                    waiting = False
                                    return int(number)
                        elif(not return_number):
                            self.screen.fill(self.BG_COLOR)
                            waiting = False
                            return triggers[event.key]
                    if(return_number):
                        if event.key == pygame.K_BACKSPACE:
                            number = number[:-1]
                            if(decimal_mode):
                                if('.' not in number):
                                    decimal_mode = False
                        elif event.unicode.isdigit() or (event.unicode == '.' and not decimal_mode):
                            number += event.unicode
                            if event.unicode == '.':
                                decimal_mode = True

            self.screen.fill(self.BG_COLOR)
            font = pygame.font.Font(None, 50)
            text = self._fit_text(font, Text + number, self.WHITE)
            text_width = text.get_width()
            text_height = text.get_height()
            text_x = (self.WIDTH - text_width) // 2
            text_y = (self.HIEGHT - text_height) // 2
            self.screen.blit(text, (text_x, text_y))
            pygame.display.update()
            self.clock.tick(self.FPS)

    def set_board(self, board, color):
        self.board = board
        self.color = color

    def draw_board(self):
        board_array = self.board.bits_to_board()
        text_area_width = self.WIDTH
        text_area_height = self.display_bottom
        text_area_rect = pygame.Rect(0, self.board_height, text_area_width, text_area_height)
        pygame.draw.rect(self.screen, self.BG_COLOR, text_area_rect)

        for r in range(board_size + 1):
            start_x = self.x
            start_y = self.y + self.SQUARESIZE * r
            end_x = self.x + self.SQUARESIZE * board_size
            end_y = self.y + self.SQUARESIZE * r
            pygame.draw.line(self.screen, self.GRAY, (start_x, start_y), (end_x, end_y), 3)

        for c in range(board_size + 1):
            start_x = self.x + self.SQUARESIZE * c
            start_y = self.y
            end_x = self.x + self.SQUARESIZE * c
            end_y = self.y + self.SQUARESIZE * board_size
            pygame.draw.line(self.screen, self.GRAY, (start_x, start_y), (end_x, end_y), 3)

        for c in range(board_size):
            for r in range(board_size):
                self._draw_piece(r, c, board_array[r][c])
        black_count = sum(row.count(1) for row in board_array)
        white_count = sum(row.count(-1) for row in board_array)
        font = pygame.font.Font(None, 50)  # Create a font object
        black_text = font.render(f"Black: {black_count}", True, self.BLACK)  # Render the black piece count text
        white_text = font.render(f"White: {white_count}", True, self.WHITE)  # Render the white piece count text
        if(self.color == 1):
            black_text = self._render_text_with_border(black_text, self.GRAY, 3)
        else:
            white_text = self._render_text_with_border(white_text, self.GRAY, 3)
        text_width = black_text.get_width() + white_text.get_width() + 20  # Calculate the total width of the text
        text_height = black_text.get_height()

        self.button_width = 120
        self.button_height = 50

        x_pos = (self.WIDTH - text_width - self.button_width - 50) // 2  # Calculate the x-coordinate to center the text
        y_pos = self.HIEGHT - (self.display_bottom + text_height) // 2

        self.screen.blit(black_text, (x_pos, y_pos)) # Draw the black piece count text
        self.screen.blit(white_text, (x_pos + black_text.get_width() + 20, y_pos))  # Draw text

        self.button_x = x_pos + black_text.get_width() + self.button_width + 70
        self.button_y = self.HIEGHT - (self.display_bottom + self.button_height) // 2

        pygame.draw.rect(self.screen, self.GRAY, (self.button_x, self.button_y, self.button_width, self.button_height))
        button_text = font.render("Pass", True, self.WHITE)
        button_text_x = self.button_x + (self.button_width - button_text.get_width()) // 2
        button_text_y = self.button_y + (self.button_height - button_text.get_height()) // 2
        self.screen.blit(button_text, (button_text_x, button_text_y))

        pygame.display.update()
        self.clock.tick(self.FPS)

    def _render_text_with_border(self, text_surface, border_color, border_width):
        # Render the text surface without a border

        # Create a larger surface to accommodate the border
        border_surface = pygame.Surface((text_surface.get_width() + border_width * 2,
                                         text_surface.get_height() + border_width * 2), pygame.SRCALPHA)

        # Draw the border rectangle
        pygame.draw.rect(border_surface, border_color,
                         (0, 0, border_surface.get_width(), border_surface.get_height()))

        # Blit the text surface onto the border surface
        border_surface.blit(text_surface, (border_width, border_width))

        return border_surface

    def _fit_text(self, font, text, color):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if font.size(current_line + " " + word)[0] <= self.max_width:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip())

        # Render each line of text separately
        rendered_lines = []
        for line in lines:
            rendered_lines.append(font.render(line, True, color))

        text_height = sum(line.get_height() for line in rendered_lines)
        combined_surface = pygame.Surface((self.max_width, text_height), pygame.SRCALPHA)
        line_y = 0
        for line in rendered_lines:
            line_width = line.get_width()
            line_x = (self.max_width - line_width) // 2
            combined_surface.blit(line, (line_x, line_y))
            line_y += line.get_height()
        return combined_surface

    def _draw_piece(self, row, col, color):
        d = {1: self.BLACK, 0: self.BG_COLOR, -1: self.WHITE}
        pygame.draw.circle(self.screen, d[color],
                           (int(col * self.SQUARESIZE + self.SQUARESIZE / 2),
                            int(row * self.SQUARESIZE + self.SQUARESIZE / 2)),
                           self.RADIUS)

    def _return_move_cordinates(self, event):
        posx = event.pos[0]
        posy = event.pos[1]
        if(posy > self.board_height):
            # check for pass

            if self.button_y <= posy <= self.button_y + self.button_height and self.button_x <= posx <= self.button_x + self.button_width:
                return board_size - 1, board_size
            else:
                return None, None

        else:
            col = int(math.floor(posx / self.SQUARESIZE))
            row = int(math.floor(posy / self.SQUARESIZE))
            print(col, row)
            return col, row

    def check_for_quit(self):
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

    def return_move(self):
        running = True
        while running:
            self.draw_board()
            # self.check_for_quit()
            # proses input(events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self._return_move_cordinates(event)
                    if (x != None):
                        move_position = y * board_size + x
                        if (move_position in self.board.moves(self.color)):
                            running = False
                            return move_position

                        if(move_position == pass_move):
                            return move_position
                        print("not valid click")

    def update(self, board, color):
        self.board = board
        self.color = color
        self.draw_board()