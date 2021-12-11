import numpy as np
import Reversi_AlphaBeta2 as reversi
import time

size = 8
player_color = -1  # -1 means white, 1 means black
now_turn = 1  # 默认黑先手
chessboard = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0,-1, 1, 0, 0, 0],
    [0, 0, 0, 1,-1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

# chessboard = np.array([
#     [0, 1, -1, -1, -1, -1, -1, 0],
#     [0, -1, -1, -1, -1, -1, -1, 0],
#     [0, -1, -1, -1, -1, 1, -1, 0],
#     [-1, 0, -1, 1, -1, 1, -1, 1],
#     [0, 0, 1, 1, -1, -1, -1, 1],
#     [0, 0, 1, 1, -1, -1, -1, 1],
#     [0, 0, 0, 0, -1, -1, -1, -1],
#     [0, 0, 0, 0, 0, 0, -1, 0]
# ])

AItest = reversi.AI(size, -player_color, time_out=0)

def player_go(chessboard):
    while True:
        print("please input your move:")
        move = eval(input())
        if reversi.AI.validMove(move, chessboard, player_color):
            print("your move is: ", move)
            break
        else:
            print("invalid move!")

    return move


while (not reversi.AI.isTerminal(chessboard)):

    if player_color == now_turn:
        player_action = reversi.AI.actions(chessboard, player_color)
        #player_action = reversi.AI.sortActions(player_action)
        if len(player_action) > 0:
            print("player action: ", player_action)
            player_move = player_go(chessboard)
            chessboard = reversi.AI.gameResult(chessboard, player_move, player_color)
        else:
            print("player has no place to play.")

        now_turn = -now_turn

    else:
        start = time.time()
        AItest.go(chessboard)
        if len(AItest.candidate_list) > 0:
            AI_move = AItest.candidate_list[-1]
            print("AI moves to: ", AI_move, "time cost: ", time.time() - start)
            print(AItest.candidate_list)
            chessboard = reversi.AI.gameResult(chessboard, AI_move, -player_color)
        else:
            print("AI has no place to play.")

        now_turn = -now_turn
    print(chessboard)

# if np.sum(chessboard) == 0:
#     print("game draw!")
# elif np.sum(chessboard) > 0:
#     if player_color > 0:
#         print("player win!")
#     else:
#         print("AI win!")
# elif np.sum(chessboard) < 0:
#     if player_color < 0:
#         print("player win!")
#     else:
#         print("AI win!")
if np.sum(chessboard) * player_color == 0:
    print("game draw!")
elif np.sum(chessboard) * player_color > 0:
    print("AI wins!")
else:
    print("player wins!")
