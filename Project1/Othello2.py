import tkinter as tk
import numpy as np
from collections import Counter
from tkinter import StringVar, IntVar

current_player = 0;  # 0 represents the user while 1 represents the algrithm
current_situation = np.zeros([10, 10])
current_situation[4][4] = 1
current_situation[5][4] = -1
current_situation[4][5] = -1
current_situation[5][5] = 1
# current_situation[5][6]=-1
# current_situation[6][6]=1
# current_situation[4][3]=-1
# current_situation[3][5]=-1
'''
current_situation[3][6]=-1
current_situation[5][7]=1
current_situation[5][8]=1
current_situation[4][7]=-1
current_situation[3][7]=-1
current_situation[6][9]=-1'''


def dropchess(event):
    global current_player, current_situation, depth, depthr, turn
    row = int(event.y / 50)
    col = int(event.x / 50)
    drop_points, change_points = get_avalible_drop(current_player, current_situation)
    set_change_points_on(drop_points, change_points, [row, col])
    if current_player == 0 and [row, col] in drop_points:
        current_situation[row][col] = -1
    if current_player == 0:
        current_player = 1
    else:
        current_player = 0

    # 算法下子
    situation = current_situation.copy()
    # print(situation)
    bestdrop = getbestdrop(situation)
    # print(bestdrop)
    drop_points, change_points = get_avalible_drop(current_player, current_situation)
    set_change_points_on(drop_points, change_points, bestdrop)
    current_situation[bestdrop[0]][bestdrop[1]] = 1
    current_player = 0
    depth = 0
    depthr = 0
    # turn.set('轮到你下子o...')
    # 算法下子
    drop_points, change_points = get_avalible_drop(current_player, current_situation)
    set_avalible_drop_on(drop_points)
    draw_Chess_from_Maxtrix(current_situation)
    clear_avalible_drop(drop_points)
    statistical_num(current_situation)
    turn.set(' ')


def draw_Chess_from_Maxtrix(current_situation):
    for i in range(len(current_situation)):
        for j in range(len(current_situation[0])):
            if current_situation[i][j] == 1:
                canvas.create_oval(j * 50 + 6, i * 50 + 6, j * 50 + 44, i * 50 + 44, fill='white')  # 白色是算法，黑色是用户
            if current_situation[i][j] == -1:
                canvas.create_oval(j * 50 + 6, i * 50 + 6, j * 50 + 44, i * 50 + 44, fill='black')
            if current_situation[i][j] == 2:
                canvas.create_oval(j * 50 + 6, i * 50 + 6, j * 50 + 44, i * 50 + 44, outline='red')
            if current_situation[i][j] == 0:
                canvas.create_oval(j * 50 + 6, i * 50 + 6, j * 50 + 44, i * 50 + 44, outline='green')


def set_avalible_drop_on(drop_points):  # 通过可下子位置列表绘制可下子标识
    global current_situation
    for point in drop_points:
        current_situation[point[0]][point[1]] = 2


def clear_avalible_drop(drop_points):  # 每一次绘制完棋子以及可下子标识后，清空当前局面矩阵可下子点
    global current_situation
    for point in drop_points:
        current_situation[point[0]][point[1]] = 0


def set_change_points_on(avalible_drop, change_points, coordinate):
    global current_situation
    idx = avalible_drop.index(coordinate)
    points = change_points[idx]
    for point in points:
        if current_situation[point[0]][point[1]] == 1:
            current_situation[point[0]][point[1]] = -1
        else:
            current_situation[point[0]][point[1]] = 1


def get_avalible_drop(current_player, current_situation):  # 通过当前玩家序号，当前局面矩阵以及落子点计算新的局面矩阵
    ava = []
    ava_row = []
    if current_player == 0:
        current_situation = current_situation * -1;
    for row in range(len(current_situation)):
        for col in range(len(current_situation[0])):
            ava_row = search_row(row, col, current_player, current_situation)
            ava_col = search_col(row, col, current_player, current_situation)
            ava_dig = search_diagonal(row, col, current_player, current_situation)
            ava_fdig = search_fdiagonal(row, col, current_player, current_situation)
            if ava_row != []:
                ava.append(ava_row)
            if ava_col != []:
                ava.append(ava_col)
            if ava_dig != []:
                ava.append(ava_dig)
            if ava_fdig != []:
                ava.append(ava_fdig)
    drop_points, change_points = format_avalible_drop(ava)
    current_situation = current_situation * -1
    return drop_points, change_points


def search_row(row, col, current_player, current_situation):  # 竖向搜索 输入坐标，玩家序号，当前局面矩阵判断是否可以落子
    avalible_row = []
    avalible_row_u = []
    avalible_row_d = []
    if current_situation[row][col] == 0:
        for i in range(row + 1, 10):
            if current_situation[i][col] == -1:
                if i == 9:
                    avalible_row_u = []
                    break
                avalible_row_u.append([i, col])
            else:
                if current_situation[i][col] == 0:
                    avalible_row_u = []
                break
        for i in range(1, row + 1):
            if current_situation[row - i][col] == -1:
                if row - i == 0:
                    avalible_row_d = []
                    break
                avalible_row_d.append([row - i, col])
            else:
                if current_situation[row - i][col] == 0:
                    avalible_row_d = []
                break
    avalible_row = avalible_row_u + avalible_row_d
    if len(avalible_row) > 0:
        return [[row, col], avalible_row]
    else:
        return []


def search_col(row, col, current_player, current_situation):  # 横向搜索
    avalible_col_u = []
    avalible_col_d = []
    avalible_col = []
    if current_situation[row][col] == 0:
        for i in range(col + 1, 10):
            if current_situation[row][i] == -1:
                if i == 9:
                    avalible_col_u = []
                    break
                avalible_col_u.append([row, i])
            else:
                if current_situation[row][i] == 0:
                    avalible_col_u = []
                break
        for i in range(1, col + 1):
            if current_situation[row][col - i] == -1:
                if col - i == 0:
                    avalible_col_d = []
                    break
                avalible_col_d.append([row, col - i])
            else:
                if current_situation[row][col - i] == 0:
                    avalible_col_d = []
                break
    avalible_col = avalible_col_u + avalible_col_d
    if len(avalible_col) > 0:
        return [[row, col], avalible_col]
    else:
        return []


def search_diagonal(row, col, current_player, current_situation):  # 正对角线搜索
    avalible_dig_u = []
    avalible_dig_d = []
    avalible_dig = []
    if current_situation[row][col] == 0:

        if row + col >= 9:
            for i in range(1, 10 - col):
                if current_situation[row - i][col + i] == -1:
                    if col + i == 9:
                        avalible_dig_u = []
                        break
                    avalible_dig_u.append([row - i, col + i])
                else:
                    if current_situation[row - i][col + i] == 0:
                        avalible_dig_u = []
                    break
            for i in range(1, 10 - row):
                if current_situation[row + i][col - i] == -1:
                    if row + i == 9:
                        avalible_dig_d = []
                        break
                    avalible_dig_d.append([row + i, col - i])
                else:
                    if current_situation[row + i][col - i] == 0:
                        avalible_dig_d = []
                    break
        else:
            for i in range(1, row + 1):
                if current_situation[row - i][col + i] == -1:
                    if row - i == 0:
                        avalible_dig_u = []
                        break
                    avalible_dig_u.append([row - i, col + i])
                else:
                    if current_situation[row - i][col + i] == 0:
                        avalible_dig_u = []
                    break
            for i in range(1, col + 1):
                if current_situation[row + i][col - i] == -1:
                    if col - i == 0:
                        avalible_dig_d = []
                        break
                    avalible_dig_d.append([row + i, col - i])
                else:
                    if current_situation[row + i][col - i] == 0:
                        avalible_dig_d = []
                    break
    avalible_dig = avalible_dig_u + avalible_dig_d
    if len(avalible_dig) > 0:
        return [[row, col], avalible_dig]
    else:
        return []


def search_fdiagonal(row, col, current_player, current_situation):  # 副对角线搜索
    avalible_fdig = []
    avalible_fdig_u = []
    avalible_fdig_d = []
    if current_situation[row][col] == 0:

        if row <= col:
            for i in range(1, row + 1):
                if current_situation[row - i][col - i] == -1:
                    if row - i == 0:
                        avalible_fdig_u = []
                        break
                    avalible_fdig_u.append([row - i, col - i])
                else:
                    if current_situation[row - i][col - i] == 0:
                        avalible_fdig_u = []
                    break
            for i in range(1, 10 - col):
                if current_situation[row + i][col + i] == -1:
                    if col + i == 9:
                        avalible_fdig_d = []
                        break
                    avalible_fdig_d.append([row + i, col + i])
                else:
                    if current_situation[row + i][col + i] == 0:
                        avalible_fdig_d = []
                    break
        else:
            for i in range(1, col + 1):
                if current_situation[row - i][col - i] == -1:
                    if col - i == 0:
                        avalible_fdig_u = []
                        break
                    avalible_fdig_u.append([row - i, col - i])
                else:
                    if current_situation[row - i][col - i] == 0:
                        avalible_fdig_u = []
                    break
            for i in range(1, 10 - row):
                if current_situation[row + i][col + i] == -1:
                    if row + i == 9:
                        avalible_fdig_d = []
                        break
                    avalible_fdig_d.append([row + i, col + i])
                else:
                    if current_situation[row + i][col + i] == 0:
                        avalible_fdig_d = []
                    break
    avalible_fdig = avalible_fdig_u + avalible_fdig_d
    if len(avalible_fdig) > 0:
        return [[row, col], avalible_fdig]
    else:
        return []


def format_avalible_drop(drop_list):
    drop_points = []
    change_points = []
    for i in range(len(drop_list)):
        if drop_list[i][0] in drop_points:
            change_points[len(change_points) - 1].append(drop_list[i][1][0])
        else:
            drop_points.append(drop_list[i][0])
            change_points.append(drop_list[i][1])
    return drop_points, change_points


##############################################建立博弈树##########################################

def MultipleTree(r):  # 建立一棵新树，根节点为r
    return [r, []]


def insertTree(root, newBranch):  # 在树的root节点（不一定是根节点）插入新枝newBranch
    root[root.index([])] = [newBranch, [], [], [], []]
    return root


def LoadTree(root):  # 递归建立一棵博弈树，当深度为depth时停止递归
    global depth, search_depth
    # print((depth)%2)
    depth += 1
    # print(depth)
    bs = getbranch((depth) % 2, root[0][0])
    if len(bs) == 0:
        return root
    elif depth >= search_depth:
        return root
    for b in bs:
        root.insert(root.index([]), LoadTree(b))
        depth -= 1
    return root


def getbranch(player, situation):  # 获得root节点（不一定是根节点）的所有叶子节点的值
    # 这里可以代入每一个局面的所有可下子点
    rr = []
    # print('situation is')
    # print('player is'+str(player))
    # print(situation)
    drop_points, change_points = get_avalible_drop_rc(player, situation.copy())
    # print('drop_points is'+str(drop_points))
    for drop in drop_points:
        new = get_new_situation(player, situation.copy(), drop)
        # print('new_situation is')
        # print('player is'+str(player))
        # print(new)
        rr.append([new, []])
    # print(rr)
    return rr


def getChildren(root):  # 获取一个节点的所有子节点
    c = []
    for i in range(1, 100):
        if root[i] != []:
            c.append(root[i])
        else:
            break
    return c


def hasChild(root):  # 判断一个节点是否有子节点
    if root[1] == []:
        return False
    else:
        return True


def getMaxChild(root):  # 或者一个节点所有子节点的最大值
    ma = -9999999999
    c = getChildren(root)
    if len(c) > 0:
        for cc in c:
            if cc[0][2] > ma:
                ma = cc[0][2]
        return ma
    else:
        return root[0][2]


def getMinChild(root):  # 或者一个节点所有子节点的最小值
    mi = 9999999999
    c = getChildren(root)
    if len(c) > 0:
        for cc in c:
            if cc[0][2] < mi:
                mi = cc[0][2]
        return mi
    else:
        return root[0][2]


def getMaxChildDrop(root):  # 获得Max and Min的下子点
    ma = -9999999999
    drop = [-1, -1]
    c = getChildren(root)
    if len(c) > 0:
        for cc in c:
            # print(cc[0][2],cc[0][1])
            if cc[0][2] > ma:
                ma = cc[0][2]
                drop = cc[0][1]
        return drop
    else:
        return root[0][1]


def Max_and_Min(root):
    global depthr
    depthr += 1
    if hasChild(root):
        for i in range(1, len(root) - 1):
            root[i][0][0] = ''
            root[i][0][2] = Max_and_Min(root[i])[0]
            depthr -= 1
    if depthr % 2 == 1:
        mc = getMaxChild(root)
    else:
        mc = getMinChild(root)
    root[0][0] = ''
    root[0][2] = mc
    return [mc, root]


###########################################用于递归函数的子函数#########################################

def set_change_points_on_rc(avalible_drop, change_points, situation, coordinate):
    # print('set_change_points_on_rc..............')
    # print('avalible_drop is:'+str(avalible_drop))
    idx = avalible_drop.index(coordinate)
    points = change_points[idx]
    for point in points:
        if situation[point[0]][point[1]] == 1:
            situation[point[0]][point[1]] = -1
        else:
            situation[point[0]][point[1]] = 1
    return situation


def get_avalible_drop_rc(player, situation):  # 通过当前玩家序号，当前局面矩阵以及落子点计算新的局面矩阵
    # print('get_avalible_drop_rc..............')
    # print('player ='+str(player))
    # print('situation='+str(situation))
    ava = []
    ava_row = []
    # print(player)
    if player == 0:
        situation = situation * -1;
    for row in range(len(situation)):
        for col in range(len(situation[0])):
            ava_row = search_row(row, col, player, situation)
            ava_col = search_col(row, col, player, situation)
            ava_dig = search_diagonal(row, col, player, situation)
            ava_fdig = search_fdiagonal(row, col, player, situation)
            if ava_row != []:
                ava.append(ava_row)
            if ava_col != []:
                ava.append(ava_col)
            if ava_dig != []:
                ava.append(ava_dig)
            if ava_fdig != []:
                ava.append(ava_fdig)
    drop_points, change_points = format_avalible_drop(ava)
    situation = situation * -1
    # print('++++++++++++++++'+str(drop_points))
    return drop_points, change_points


def get_new_situation(player, situation, drop):  # 根据可下子列表设置当前局面矩阵
    drop_points, change_points = get_avalible_drop_rc(player, situation)
    set_change_points_on_rc(drop_points, change_points, situation, drop)
    if player == 1 and drop in drop_points:
        situation[drop[0]][drop[1]] = 1
    if player == 0 and drop in drop_points:
        situation[drop[0]][drop[1]] = -1
    player_algrithm, player_user = statistical(situation)
    advantage = player_algrithm - player_user
    return [situation, drop, advantage]


def getbestdrop(situation):
    roott = MultipleTree([situation, [-1, -1], 0])
    r = LoadTree(roott)
    mc, rr = Max_and_Min(r)
    bestdrop = getMaxChildDrop(rr)
    return bestdrop


def statistical(situation):  # 根据一个局面矩阵计算黑白子的数量
    global white_num
    global black_num
    player_algrithm = 0
    player_user = 0
    for row in situation:
        for val in row:
            if val == 1:
                player_algrithm += 1
            if val == -1:
                player_user += 1
    return player_algrithm, player_user


def statistical_num(situation):  # 根据一个局面矩阵计算黑白子的数量
    global white_num
    global black_num
    player_algrithm = 0
    player_user = 0
    for row in situation:
        for val in row:
            if val == 1:
                player_algrithm += 1
            if val == -1:
                player_user += 1
    white_num.set(str(player_algrithm))
    black_num.set(str(player_user))
    return player_algrithm, player_user


###########################################用于递归函数的子函数#########################################

#####################设置搜索深度###############

global search_depth
search_depth = 3

#####################设置搜索深度###############


global depthr
global depth
global white_num
global black_num
global turn
depth = 0
depthr = 0
white_num = 2
black_num = 2

canvas = ''
white_label = ''
black_label = ''
playerturn_label = ''

rt = tk.Tk(className="bw")
rt.resizable(0, 0)

white_num = StringVar()
white_num.set('2')
black_num = StringVar()
black_num.set('2')
turn = StringVar()
turn.set('轮到你下子...')

canvas = tk.Canvas(rt, width=700, height=500, bg='green')
canvas.bind()
canvas.pack(padx=10, pady=10)

white_label = tk.Label(rt, width=4, height=1, textvariable=white_num)
white_label.place(x=600, y=220)
black_label = tk.Label(rt, width=4, height=1, textvariable=black_num)
black_label.place(x=600, y=290)
drop_label = tk.Label(rt, width=7, height=1, text='可下子点')
drop_label.place(x=600, y=360)
playerturn_label = tk.Label(rt, width=10, height=2, bg='green', textvariable=turn)
playerturn_label.place(x=550, y=150)

canvas.create_line(0, 0, 0, 500, fill='black', width=10)
canvas.create_line(0, 0, 500, 0, fill='black', width=10)
canvas.create_line(500, 500, 0, 500, fill='black', width=3)
canvas.create_line(500, 500, 500, 0, fill='black', width=3)
for i in range(10):
    canvas.create_line(50 * i, 0, 50 * i, 500, fill='black', width=2)
    canvas.create_line(0, 50 * i, 500, 50 * i, fill='black', width=2)
canvas.bind(sequence='<Button-1>', func=dropchess)
canvas.create_oval(540, 200, 580, 240, fill='white')  # 白色是算法，黑色是用户
canvas.create_oval(540, 270, 580, 310, fill='black')  # 白色是算法，黑色是用户
canvas.create_oval(540, 340, 580, 380, outline='red')  # 白色是算法，黑色是用户
drop_points, change_points = get_avalible_drop(current_player, current_situation)
set_avalible_drop_on(drop_points)
draw_Chess_from_Maxtrix(current_situation)
clear_avalible_drop(drop_points)
rt.mainloop()