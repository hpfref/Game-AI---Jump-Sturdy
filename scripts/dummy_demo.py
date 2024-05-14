### To import from src:
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
###
import numpy as np
import pygame as pg
from visuals import load_pieces, draw_board, draw_pieces
from board import fen_to_board
from gamestate import random_move, game_over, generate_new_board

if __name__ == "__main__":
    pg.init()
    size = width, height = 800, 800
    SQUARE = width // 8
    FPS = 2
    window = pg.display.set_mode(size)
    BOARD = np.full((8, 8), "", dtype='U10')
    for y in range(8):
        for x in range(8):
            if (x, y) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                BOARD[y, x] = "X"
            else:
                BOARD[y, x] = ""
                
    starting_fen = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
    PIECES = load_pieces()
    board, player = fen_to_board(starting_fen)
    running = True
    clock = pg.time.Clock()

    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if not game_over(starting_fen):
            move = random_move(starting_fen)
            if move is not None:
                starting_fen = generate_new_board(starting_fen, move)
                board, player = fen_to_board(starting_fen)
        
        window.fill((0, 0, 0))
        draw_board(BOARD, window)
        draw_pieces(board, window, PIECES)
        pg.display.flip()

    pg.quit()