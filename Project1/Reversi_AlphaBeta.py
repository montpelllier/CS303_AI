import math
import random
import time

import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
step = 0


WeightMap = np.array([
    [500, -25, 10, 5, 5, 10, -25, 500],
    [-25, -45, 1, 1, 1, 1, -45, -25],
    [10, 1, 3, 2, 2, 3, 1, 10],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [10, 1, 3, 2, 2, 3, 1, 10],
    [-25, -45, 1, 1, 1, 1, -45, -25],
    [500, -25, 10, 5, 5, 10, -25, 500]
])

WeightMap2 = np.array([
    [-850, 125, -50, -12, -12, -50, 125, -850],
    [ 125,  -5,  10,   6,   6,  10,  -5,  125],
    [ -50,  10,   5,   3,   3,   5,  10,  -50],
    [ -12,   6,   3,   2,   2,   3,   6,  -12],
    [ -12,   6,   3,   2,   2,   3,   6,  -12],
    [ -50,  10,   5,   3,   3,   5,  10,  -50],
    [ 125,  -5,  10,   6,   6,  10,  -5,  125],
    [-850, 125, -50, -12, -12, -50, 125, -850]
])

direction = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent

    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your
        # decision.
        self.candidate_list = []
        self.corner = [(0, 0), (0, chessboard_size - 1), [chessboard_size - 1, 0],
                       (chessboard_size - 1, chessboard_size - 1)]
        self.star = [(0, 1), (1, 0), (1, 1), (1, chessboard_size - 1), (0, chessboard_size - 2),
                     (1, chessboard_size - 2),
                     (chessboard_size - 2, 0), (chessboard_size - 1, 1),
                     (chessboard_size - 2, 1),
                     (chessboard_size - 2, chessboard_size - 1), (chessboard_size - 1, chessboard_size - 2),
                     (chessboard_size - 2, chessboard_size - 2)]

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()

        # ==================================================================
        self.time_out = time.time() + 5.0
        self.candidate_list = AI.actions(chessboard, self.color)
        cornerMove = []
        otherMove = []
        starMove = []
        # global step
        # step = 0
        for move in self.candidate_list:
            if move in self.corner:
                cornerMove.append(move)
            elif move in self.star:
                starMove.append(move)
            else:
                otherMove.append(move)

        # Write your algorithm here
        maxStep = 1500
        emptyPos = np.where(chessboard == COLOR_NONE)
        emptyPos = list(zip(emptyPos[0], emptyPos[1]))

        if len(self.candidate_list) > 1:
            depth = int( math.log(maxStep, len(self.candidate_list) ) )
            if len(emptyPos) < 4:
                depth += 5
            elif len(emptyPos) < 8:
                depth += 4
            elif len(emptyPos) < 16:
                depth += 1
        else:
            depth = 0
        # move_time = (self.time_out - time.time()) / len(self.candidate_list)
        # print(move_time)

        print("search depth: ",depth)
        bestScore, worstScore, bestMove = -math.inf, math.inf, None
        for move in starMove + otherMove + cornerMove:

            # time_limit = self.time_out - time.time() - move_time
            NextBoard = AI.gameResult(chessboard, move, self.color)
            #print(self.time_out - time.time())
            # print(time_limit)
            tempScore = self.minValue(NextBoard, depth, -self.color, bestScore, worstScore)
            print("alpha: ", bestScore, "beta: ", worstScore)
            print(move, ": ",tempScore, " time is: ", self.time_out-time.time())
            if tempScore > bestScore:
                bestScore, bestMove = tempScore, move

        if bestMove is not None:
            self.candidate_list.append(bestMove)
        #print("steps: ", step)
        # AI算法

        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, the system will return error.
        # Add your decision into candidate_list, Records the chess board
        # You need add all the positions which is valid
        # candidate_list example: [(3,3),(4,4)]
        # You need append your decision at the end of the candidate_list,
        # we will choice the last element of the candidate_list as the position you choose
        # If there is no valid position, you must return an empty list.

    @staticmethod
    def inChessboard(size, x, y):
        if 0 <= x < size and 0 <= y < size:
            return True
        return False

    @staticmethod
    def validMove(move, chessboard, color) -> bool:
        x, y = move
        if chessboard[move] != COLOR_NONE:
            return False
        size = len(chessboard)
        for dire in direction:
            temp_x = x + dire[0]
            temp_y = y + dire[1]
            if AI.inChessboard(size, temp_x, temp_y) and chessboard[temp_x][temp_y] == -color:
                while AI.inChessboard(size, temp_x + dire[0], temp_y + dire[1]):
                    temp_x += dire[0]
                    temp_y += dire[1]
                    if chessboard[temp_x][temp_y] == color:
                        return True
                    elif chessboard[temp_x][temp_y] == COLOR_NONE:
                        break

        return False

    @staticmethod
    def actions(chessboard, color):
        actions = []
        emptyPos = np.where(chessboard == COLOR_NONE)
        emptyPos = list(zip(emptyPos[0], emptyPos[1]))

        for move in emptyPos:
            if AI.validMove(move, chessboard, color):
                actions.append(move)
        return actions

    @staticmethod
    def gameResult(chessboard, move, color):  # self color
        new_board = chessboard.copy()
        new_board[move] = color
        turn_pos = []

        for dire in direction:
            x, y = move
            while AI.inChessboard(len(new_board), x + dire[0], y + dire[1]):
                x += dire[0]
                y += dire[1]
                if new_board[x][y] == color:
                    for pos in turn_pos:
                        new_board[pos] = color
                    turn_pos.clear()
                    break
                elif new_board[x][y] == COLOR_NONE:
                    turn_pos.clear()
                    break
                elif new_board[x][y] == -color:
                    turn_pos.append((x, y))
        return new_board

    @staticmethod
    def isTerminal(chessboard):
        whiteMove = AI.actions(chessboard, COLOR_WHITE)
        blackMove = AI.actions(chessboard, COLOR_BLACK)
        if len(whiteMove) == len(blackMove) == 0:
            return True
        return False

    def maxValue(self, chessboard, depth, color, alpha, beta):
        # print("depth max", depth)
        nextDepth = depth - 1
        if self.isTerminal(chessboard) or time.time() > self.time_out - 0.3 or depth == 0:
            return self.evaluate(chessboard, color)
        # if self.isTerminal(chessboard) or self.time_out - time.time() < time_limit:
        #     #print("return")
        #     return self.evaluate(chessboard, color)
        #print(self.time_out - time.time())
        value = -math.inf
        actions = AI.actions(chessboard, color)

        curLength = len(actions)

        # if time.time() < self.time_out - 1.5:
        #     nextDepth = depth
        # else:nextDepth = depth - 1

        if curLength == 0:
            value = max(self.minValue(chessboard, depth, -color, alpha, beta), value)
            if value >= beta:
                return value
            alpha = max(alpha, value)

        for a in actions:
            nextBoard = self.gameResult(chessboard, a, color)
            value = max(self.minValue(nextBoard, nextDepth, -color, alpha, beta), value)
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value


    def minValue(self, chessboard, depth, color, alpha, beta):

        # print("depth min", depth)
        nextDepth = depth - 1
        if self.isTerminal(chessboard) or time.time() > self.time_out - 0.3 or depth == 0:
            return self.evaluate(chessboard, color)

        # if self.isTerminal(chessboard) or self.time_out - time.time() < time_limit - 0.2:
        #     return self.evaluate(chessboard, color)

        value = math.inf
        actions = AI.actions(chessboard, color)
        curLength = len(actions)
        if curLength == 0:
            value = min(self.maxValue(chessboard, depth, -color, alpha, beta), value)
            if value <= alpha:
                return value
            beta = min(beta, value)
        # print(len(actions))
        for a in actions:
            nextBoard = self.gameResult(chessboard, a, color)
            value = min(self.maxValue(nextBoard, nextDepth, -color, alpha, beta), value)
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    @staticmethod
    def mobility(chessboard, color):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))

        mobilityCoef = 1
        if len(idx) > 30:
            mobilityCoef = 180
        elif len(idx) > 16:
            mobilityCoef = 150
        elif len(idx) > 8:
            mobilityCoef = 120
        elif len(idx) > 4:
            mobilityCoef = 75

        myMobility = len(AI.actions(chessboard, color))
        oppMobility = len(AI.actions(chessboard, -color))
        # 行动力的价值计算
        if oppMobility == 0:
            return -700
        if myMobility == 0:
            return 700

        return mobilityCoef * (myMobility - oppMobility)

    @staticmethod
    def checkDirection(chessboard, point, dire):#无子返回false,
        color = chessboard[point]
        size = len(chessboard)
        x, y = point
        dx, dy = dire
        while AI.inChessboard(size, x + dx, y + dy):
            x += dx
            y += dy
            if chessboard[x][y] == COLOR_NONE:
                return False
            elif chessboard[x][y] == color:
                pass
            elif chessboard[x][y] == -color:
                return True
        return True

    @staticmethod
    def isStable(chessboard, point, stableMap):  # 稳定子计算
        # 1.如果一个子的两边都是同色的稳定子或边，则其在该方向上稳定
        # 2.如果一个子的两边都是对方色的子或边，则其在该方向上稳定
        # 3.如果四个方向都稳定，则该子为稳定子·
        if chessboard[point] == COLOR_NONE:
            return False
        elif stableMap[point] == 100:
            return True
        elif stableMap[point] != 0:
            return False
        else:
            count = 0
            oppColor = -chessboard[point]
            myColor = chessboard[point]

            for dire in direction[:4]:
                px, py = point
                dx, dy = dire
                p1 = (px + dx, py + dy)
                p2 = (px - dx, py - dy)
                size = len(chessboard)
                if AI.inChessboard(size, p1[0], p1[1]) and AI.inChessboard(size, p2[0], p2[1]):
                    if chessboard[p1] == chessboard[p2] == oppColor:
                        count += 1
                    elif chessboard[p1] == chessboard[p2] == COLOR_NONE:
                        pass
                    elif chessboard[p1] == chessboard[p2] == myColor:
                        if AI.checkDirection(chessboard, point, dire) or AI.checkDirection(chessboard, point,
                                                                                           (-dx, -dy)):
                            count += 1
                    elif chessboard[p1] == myColor and chessboard[p2] == oppColor:
                        if AI.checkDirection(chessboard, point, dire):
                            count += 1
                    elif chessboard[p2] == myColor and chessboard[p1] == oppColor:
                        if AI.checkDirection(chessboard, point, (-dx, -dy)):
                            count += 1
                #elif AI.inChessboard(size, p1[0], p1[1]) and AI.isStable(chessboard, p1, stableMap):  # 遇边则稳
                else:
                    count += 1

            if count == 4:
                stableMap[point] = 100
                return True
            elif count == 3:
                stableMap[point] = 5
            elif count == 2:
                stableMap[point] = -5
            elif count == 1:
                stableMap[point] = -15
            elif count == 0:
                stableMap[point] = -30
            return False

    @staticmethod
    def stability(chessboard, color):
        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        size = len(chessboard)
        value = 0

        stabilityCoef = -1
        if len(idx) > 30:
            stabilityCoef = -1.5
        elif len(idx) > 16:
            stabilityCoef = -2
        elif len(idx) > 8:
            stabilityCoef = -4
        elif len(idx) > 4:
            stabilityCoef = -10

        stableMap = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])

        for point in idx:
            AI.isStable(chessboard, point, stableMap)
        for i in range(size):
            for j in range(size):
                value += stableMap[i][j] * chessboard[i][j]

        return value * color * stabilityCoef

    def evaluate(self, chessboard, color):  # 估值函数 少子方胜
        # global step
        # step += 1
        if AI.isTerminal(chessboard):  # 终局直接判断胜负
            Result = np.sum(chessboard) * self.color
            if Result > 0:
                return -99999
            elif Result < 0:
                return 99999
            else:
                return 0

        weight = 0
        weightMap = WeightMap2.copy()
        for i in range(4):
            if chessboard[self.star[3*i]] == chessboard[self.star[3*i+1]] == self.color:
                weightMap[self.star[3*i+2]] += 50
            #elif chessboard[self.star[3*i]] == chessboard[self.star[3*i+1]] == -self.color:

        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                weight += weightMap[i][j] * chessboard[i][j]

        weight = weight * self.color
        # 所占位置的价值估算 （取反

        # 稳定子的价值估算
        Stability = AI.stability(chessboard, self.color)
        Mobility = AI.mobility(chessboard, self.color)  # 行动力越高越好？

        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        if len(idx) % 2 == 1 and color == self.color:
            isLastStep = -500
        else:
            isLastStep = 500

        return weight + Mobility + Stability + isLastStep

        # 设计评估函数G(s) = action行动力 + 稳定子 + 位置估计值，权重系数
        # 一个已获得的子的稳定度
        # 不稳定说明为对方提供了更多的行动力
        # ，奇偶：控制最后一步棋，控线
        # No.34 65points 10-18 21:43
        #
