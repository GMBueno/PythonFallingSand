import time
import random
from map import board as drawn_board

# try:
#     h = int(input('how many rows? \t (5-200, default is 10)'))
#     if h < 5 or h > 200:
#         h = 10
# except:
#     h = 10
#
# try:
#     w = int(input('how many columns? \t (5-500, default is 40)'))
#     if w < 5 or w > 500:
#         w = 40
# except:
#     w = 40
#
# try:
#     bps = int(input('boards per second? \t (1-50, default is 1)'))
#     if bps < 1 or bps > 50:
#         bps = 1
# except:
#     bps = 1

h = len(drawn_board)
w = len(drawn_board[0])
bps = 10

'''
we add a 'mask' to ease count of neighbors on func 'count_neighbors()'.
This mask is a row and a col of air cells before and after the board that
do not influence the logic (count of neighbors will be the same).
'''

def test_board():
    '''
    Just for testing. 1 is sand. 0 is air.
    '''
    h, w  = 10, 40
    board = {}
    for row in range(h+2):
        for col in range(w+2):
            board[row, col] = 0

    ''' shapes/patterns '''

    # (oscillator) blinker
    board[3, 2] = 1
    board[3, 3] = 1
    board[3, 4] = 1

    # (oscillator) toad
    board[2,20] = 1
    board[2,21] = 1
    board[2,22] = 1
    board[3,19] = 1
    board[3,20] = 1
    board[3,21] = 1

    # (spaceship) glider
    board[2,10] = 1
    board[3,11] = 1
    board[4,11] = 1
    board[4,10] = 1
    board[4,9] = 1

    # (still life) bee-hive
    board[7,5] = 1
    board[7,6] = 1
    board[8,4] = 1
    board[8,7] = 1
    board[9,5] = 1
    board[9,6] = 1

    return board

def random_board():
    '''1 is sand. 0 is air. 2 '''
    board = {}
    for row in range(h+2):
        for col in range(w+2):
            board[row, col] = 0
    for row in range(1, h+1):
        for col in range(1, w+1):
            board[row, col] = random.randint(0, 1)
    return board

def hourglass_board():
    board = {}
    # fill with air
    for row in range(h+2):
        for col in range(w+2):
            board[row, col] = 0
    # draw hourglass
    for row in range(1, h+1):
        for col in range(1, w+1):
            board[row, col] = int(drawn_board[row-1][col-1])

    return board

def strfy(board):
    # we don't print the mask (first and last rows and cols)
    for row in range(1, h+1):
        text = ''
        for col in range(1, w+1):
            if board[row,col] == 1:
                text += '✦'
            elif board[row,col] == 2:
                text += '▣'
            elif board[row,col] == 0:
                # text += '▢'
                text += ' '
            else:
                text += '?'
        print(text)

def next_state(board):
    new_board = board.copy()
    mov_board = {}
    for row in range(h+2):
        for col in range(w+2):
            mov_board[row, col] = False
    # we never iterate/change cells of the mask (first and last rows and cols)
    # we iterate reversed so a sand above another can fall with the one below
    for row in range(h, 0, -1):
        start = ((w-1)/2)+1
        count = 1
        while start != w+1:
            col = start
            cell = board[row, col]
            # if it's sand
            if cell == 1:
                # if row below is air, sand can fall
                if new_board[row+1, col] == 0:
                    new_board[row, col] = 0
                    new_board[row+1, col] = 1
                    mov_board[row+1, col] = True
                elif new_board[row+1, col] != 0:
                    if new_board[row+1, col+1] == 0:
                        new_board[row+1, col+1] = 1
                        new_board[row, col] = 0
                    elif new_board[row+1, col-1] == 0:
                        new_board[row+1, col-1] = 1
                        new_board[row, col] = 0
            start = start + count
            # print(start)
            if count > 0:
                count = (count + 1) * -1
            else:
                count = -count
                count = (count + 1)

    # for row in range(h, 0, -1):
    #     for col in range(w, 0, -1):
    #         cell = new_board[row, col]
    #         # if it's sand
    #         if cell == 1:
    #             # if row below is air, it was already dealt with, so we skip
    #             if new_board[row+1, col] != 0 and mov_board[row, col] == False:
    #                 if new_board[row+1, col+1] == 0:
    #                     new_board[row+1, col+1] = 1
    #                     new_board[row, col] = 0
    #                 elif new_board[row+1, col-1] == 0:
    #                     new_board[row+1, col-1] = 1
    #                     new_board[row, col] = 0
    # print_board(new_board)
    return new_board


def print_board(board):
    row_cells = []
    for row in range(1, h+1):
        for col in range(1, w+1):
            cell = board[row, col]
            # print(cell)
            row_cells.append(cell)
        print(row_cells)
        row_cells = []

def count_neighbors(row, col, board):
    # pretty simple to count. Once we have a mask, we don't need to test edges
    count = 0
    # up, right, down, left
    if board[row-1, col] == 1: # up
        count += 1
    if board[row, col+1] == 1: # right
        count += 1
    if board[row+1, col] == 1: # down
        count += 1
    if board[row, col-1] == 1: # left
        count += 1
    # diagonals
    if board[row-1, col+1] == 1: # up right
        count += 1
    if board[row+1, col+1] == 1: # down right
        count += 1
    if board[row+1, col-1] == 1: # down left
        count += 1
    if board[row-1, col-1] == 1: # up left
        count += 1
    return count

# board = test_board()
board = hourglass_board()
while True:
    print('\n')
    strfy(board)
    board = next_state(board)
    time.sleep(1.0/bps)
