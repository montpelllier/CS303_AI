import random

import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name

class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        enemy_color = -self.color
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        #找到所以可以合法下棋的位置
        for x, y in idx:
            isAvailable = False
            # check 8 directions
            if x + 1 < self.chessboard_size - 1 and chessboard[x + 1][y] == enemy_color:
                temp_x = x + 1
                temp_y = y
                while temp_x + 1 < self.chessboard_size:
                    temp_x = temp_x + 1
                    if chessboard[temp_x][temp_y] == self.color:
                        isAvailable = True
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break  # 为敌方的棋才能继续
            if isAvailable:
                continue
            elif x + 1 < self.chessboard_size - 1 and y + 1 < self.chessboard_size - 1 and chessboard[x + 1][
                y + 1] == enemy_color:
                temp_x = x + 1
                temp_y = y + 1
                while temp_x + 1 < self.chessboard_size or temp_y + 1 < self.chessboard_size:
                    temp_x = temp_x + 1
                    temp_y = temp_y + 1
                    if chessboard[temp_x][temp_y] == self.color:
                        isAvailable = True
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break
            if isAvailable:
                continue
            elif y + 1 < self.chessboard_size - 1 and chessboard[x][y + 1] == enemy_color:
                temp_x = x
                temp_y = y + 1
                while temp_y + 1 < self.chessboard_size:
                    temp_y = temp_y + 1
                    if chessboard[temp_x][temp_y] == self.color:
                        isAvailable = True
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break
            if isAvailable:
                continue
            elif x - 1 > 0 and y + 1 < self.chessboard_size - 1 and chessboard[x - 1][y + 1] == enemy_color:
                temp_x = x - 1
                temp_y = y + 1
                while temp_x - 1 > 0 or temp_y + 1 < self.chessboard_size:
                    temp_x = temp_x - 1
                    temp_y = temp_y + 1
                    if chessboard[temp_x][temp_y] == self.color:
                        isAvailable = True
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break
            if isAvailable:
                continue
            elif x - 1 > 0 and chessboard[x - 1][y] == enemy_color:
                temp_x = x - 1
                temp_y = y
                while temp_x - 1 > 0:
                    temp_x = temp_x - 1
                    if chessboard[temp_x][temp_y] == self.color:
                        isAvailable = True
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break
            if isAvailable:
                continue
            elif x - 1 < self.chessboard_size - 1 and y - 1 > 0 and chessboard[x - 1][y - 1] == enemy_color:
                temp_x = x - 1
                temp_y = y - 1
                while temp_x - 1 > 0 and temp_y - 1 > 0:
                    temp_x = temp_x - 1
                    temp_y = temp_y - 1
                    if chessboard[temp_x][temp_y] == self.color:
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break
            if isAvailable:
                continue
            elif y - 1 > 0 and chessboard[x][y - 1] == enemy_color:
                temp_x = x
                temp_y = y - 1
                while temp_y - 1 > 0:
                    temp_y = temp_y - 1
                    if chessboard[temp_x][temp_y] == self.color:
                        isAvailable = True
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break
            if isAvailable:
                continue
            elif x + 1 < self.chessboard_size - 1 and y - 1 > 0 and chessboard[x + 1][y - 1] == enemy_color:
                temp_x = x + 1
                temp_y = y - 1
                while temp_x + 1 < self.chessboard_size and temp_y - 1 > 0:
                    temp_x = temp_x + 1
                    temp_y = temp_y - 1
                    if chessboard[temp_x][temp_y] == self.color:
                        self.candidate_list.append((x, y))
                        break
                    elif chessboard[temp_x][temp_y] == 0:
                        break

        #AI算法

        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, the system will return error.
        # Add your decision into candidate_list, Records the chess board
        # You need add all the positions which is valid
        # candiidate_list example: [(3,3),(4,4)]
        # You need append your decision at the end of the candiidate_list,
        # we will choice the last element of the candidate_list as the position you choose
        # If there is no valid position, you must return an empty list.
