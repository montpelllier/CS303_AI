"""
Example:
input:
map:
---------
------x--
-x-------
---@-----
---##----
------x--
--x----x-
-x-------
---------
action:
0 0 3 3 0 3 3 1 1 1 1 1 3 1 1 2 2 2 2 2

output:
7 3

"""

if __name__ == '__main__':
    test_case = 1
    while test_case > 0:

        with open(f'test_cases/problem3/{test_case}-map.txt', 'r') as f:
            game_map = [list(line.strip()) for line in f.readlines()]
        # print(game_map)
        with open(f'./test_cases/problem3/{test_case}-actions.txt', 'r') as f:
            actions = [*map(int, f.read().split(' '))]
        # print(actions)
        print(f'case {test_case}')
        test_case = test_case - 1

        count = 0
        flag = True
        sneak = [(3, 3), (3, 4), (4, 4)]
        for act in actions:
            print(sneak)
            if act == 0:

                sneak.pop()
                sneak.insert(0, (sneak[0][0], sneak[0][1] - 1))
                if game_map[sneak[0][0]][sneak[0][1]] != 'x':
                    count = count + 1
                else:
                    print(count)
                    flag = False
                    break
            elif act == 1:
                sneak.pop()
                sneak.insert(0, (sneak[0][0], sneak[0][1] + 1))
                if game_map[sneak[0][0]][sneak[0][1]] != 'x':
                    count = count + 1
                else:
                    print(count)
                    flag = False
                    break
            elif act == 2:
                sneak.pop()
                sneak.insert(0, (sneak[0][0] - 1, sneak[0][1]))
                if game_map[sneak[0][0]][sneak[0][1]] != 'x':
                    count = count + 1
                else:
                    print(count)
                    flag = False
                    break
            elif act == 3:
                sneak.pop()
                sneak.insert(0, (sneak[0][0] + 1, sneak[0][1]))
                if game_map[sneak[0][0]][sneak[0][1]] != 'x':
                    count = count + 1
                else:
                    print(count)
                    flag = False
                    break

        if flag:
            print('%d, %d' % sneak[0])
            print(sneak)
