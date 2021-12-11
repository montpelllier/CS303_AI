# 模拟退火算法
import argparse
import heapq
import random
import time

import numpy as np
# from matplotlib import pyplot as plt
from matplotlib import pyplot as plt


class Graph:  # 无向图
    def __init__(self, edges):  # labels为标点名称
        self.Edges = edges  # 字典表示边 {(a,b):int}, a<=b
        self.VertexNum = len(edges)  # 默认1开始
        self.Vertex = [i for i in range(self.VertexNum)]
        self.ShortestCost = {}  # 起点出发到各点的最短距离{(a,b):int}, a<=b

    def dijkstra(self, start_node: int, end_node: int):  # 计算最短路径并写入ShortestCost
        min_heap = [(0, start_node)]
        is_shortest = set()
        distance = {start_node: 0}
        # 加入起点
        while len(min_heap) != 0:
            pop_node = heapq.heappop(min_heap)[1]  # 出来的点
            is_shortest.add(pop_node)
            cost = distance[pop_node]
            self.ShortestCost[(min(start_node, pop_node)), max(start_node, pop_node)] = cost
            if pop_node is end_node:
                break
            for node in self.Vertex:
                if node in is_shortest or node is pop_node:  # 不是最短，且不是同一个点
                    continue
                min_node = min(node, pop_node)
                max_node = max(node, pop_node)
                if (min_node, max_node) in self.Edges and (node not in distance or (
                        node in distance and cost + self.Edges[(min_node, max_node)] < distance[node])):  # 相邻,比原来小才更新
                    heapq.heappush(min_heap, (cost + self.Edges[(min_node, max_node)], node))
                    distance[node] = cost + self.Edges[(min_node, max_node)]  # 更新距离


    def dijkstra(self, nodes: list):#只记录有必要的边
        for i in range(len(nodes)-1):
            j = i + 1
            start_node, end_node = nodes[i], nodes[j]
            min_heap = [(0, start_node)]
            is_shortest = set()
            distance = {start_node: 0}

            while len(min_heap) != 0:
                pop_node = heapq.heappop(min_heap)[1]  # 出来的点
                is_shortest.add(pop_node)
                cost = distance[pop_node]
                self.ShortestCost[(min(start_node, pop_node)), max(start_node, pop_node)] = cost
                if pop_node is end_node:
                    if end_node == nodes[-1]:
                        break
                    while j + 1 < len(nodes):
                        j += 1
                        end_node = nodes[j]
                        if (start_node, end_node) not in self.ShortestCost:
                            break

                for node in self.Vertex:
                    if node in is_shortest or node is pop_node:  # 不是最短，且不是同一个点
                        continue
                    min_node = min(node, pop_node)
                    max_node = max(node, pop_node)
                    if (min_node, max_node) in self.Edges and (node not in distance or (
                            node in distance and cost + self.Edges[(min_node, max_node)] < distance[
                        node])):  # 相邻,比原来小才更新
                        heapq.heappush(min_heap, (cost + self.Edges[(min_node, max_node)], node))
                        distance[node] = cost + self.Edges[(min_node, max_node)]  # 更新距离


def TotalCost(state):
    cost, s = 0, [0]
    capa, prev_node = capacity, depot

    for edge in state:
        cor_edge = (min(edge[0], edge[1]), max(edge[0], edge[1]))
        if capa - requiredCost[cor_edge] < 0:  # 装满了返程
            # 计算回去的路程
            back_path = (min(depot, prev_node), max(depot, prev_node))

            if prev_node == depot:
                shortest = 0
            elif back_path not in graph.ShortestCost:
                print("unreachable")
                graph.dijkstra(back_path[0], back_path[1])
                shortest = graph.ShortestCost[back_path]
            else:
                shortest = graph.ShortestCost[back_path]

            cost += shortest
            prev_node = depot
            s.append(0)
            s.append(0)
            capa = capacity  # 切割线路

        next_node = edge[0]
        min_node = min(prev_node, next_node)
        max_node = max(prev_node, next_node)
        # 前一个边右边点到现在边左边点的最短路径+该边cost
        if prev_node == next_node:  # 同一个点距离为0
            shortest = 0
        elif (min_node, max_node) not in graph.ShortestCost:  # 没有记录跑dij
            print("unreachable")
            graph.dijkstra(min_node, max_node)
            shortest = graph.ShortestCost[(min_node, max_node)]
        else:  # 有记录直接取值
            shortest = graph.ShortestCost[(min_node, max_node)]

        cost += shortest + graph.Edges[cor_edge]
        capa -= requiredCost[cor_edge]
        s.append(edge)
        prev_node = edge[1]
        if edge == state[-1]:  # 结束后返程
            back_path = (min(depot, prev_node), max(depot, prev_node))
            if prev_node == depot:
                shortest = 0
            elif back_path not in graph.ShortestCost:
                print("unreachable")
                graph.dijkstra(back_path[0], back_path[1])
                shortest = graph.ShortestCost[back_path]
            else:
                shortest = graph.ShortestCost[back_path]
            cost += shortest

    return s, cost


def LocalSearch(state, turn):
    new_state = state.copy()
    if turn % 2 == 1:  # 交换边
        res = random.sample(range(len(new_state)), 2)
        new_state[res[0]], new_state[res[1]] = new_state[res[1]], new_state[res[0]]  # swap
    else:
        index = random.randint(0, len(new_state) - 1)
        new_state[index] = (new_state[index][1], new_state[index][0])
    return new_state


def SimulatedAnnealing(initial, schedule, halt, log_interval=200):
    t = 0  # time step
    T = schedule(t)  # temperature
    state = initial
    f = []
    min_value, path = float('inf'), None
    cnt = 0
    while not halt(T):
        _, value = TotalCost(state)
        new_state = LocalSearch(state, t)

        T = schedule(t)
        if value < min_value:
            min_value = value
            path = state

        if cnt == 1600:
            # print("restart", t)
            for i in range(int(len(state))*2):
                new_state = LocalSearch(new_state, i)
            t = 0
            cnt = 0

        # TODO: implement the replacement here
        _, new_value = TotalCost(new_state)

        if new_value < value:

            cnt = 0
            state = new_state
            f.append(new_value)
        else:
            cnt += 1
            # if len(state) < 10:
            #     coef = len(state) / 3
            # elif len(state) < 30:
            #     coef = len(state) / 8
            # elif len(state) < 65:
            #     coef = len(state) / 16
            # elif

            P = np.exp(-(new_value - value) / (T * 3.0))
            # print((-(new_value - value) / T), P, T)
            ret = random.random()
            if ret < P:
                state = new_state
                f.append(new_value)
            else:
                f.append(value)
        if time.time() - start > float(args.t) - 0.2:
            # print("time up")
            break
        # update time and temperature
        # if t % log_int erval == 0:
        #     print(f"step {t}: T={T}, current_value={new_value}")
        t += 1
        T = schedule(t)

    # _, v = TotalCost(state)
    # print(f"step {t}: T={T}, current_value={v}")
    return path, f


start = time.time()  # 开始计时

parser = argparse.ArgumentParser(description="CARP")
parser.add_argument('file', help="is the absolute path of the test CARP instance file.")
parser.add_argument('-t', help="specifies the termination condition of your algorithm.")
parser.add_argument('-s', help="specifies the random seed used in this run.")
args = parser.parse_args()  # 处理命令行输入参数
#random.seed(args.s)

f = open(args.file, 'r')
lines = f.readlines()
vertices = int(lines[1].split()[-1].split("\n")[-1])
depot = int(lines[2].split()[-1].split("\n")[-1])
edges = int(lines[3].split()[-1].split("\n")[-1]) + int(lines[4].split()[-1].split("\n")[-1])
capacity = int(lines[6].split()[-1].split("\n")[-1])
graph, requiredCost = {}, {}

for line in lines[9:9 + edges]:
    data = list(map(int, line.split()))
    v1, v2 = min(data[0], data[1]), max(data[0], data[1])
    graph[(v1, v2)] = data[2]
    if data[3] != 0:
        requiredCost[(v1, v2)] = data[3]

graph = Graph(graph)
state = list(requiredCost.keys())
requiredEdges = sorted(state)
nodes = set()
for edge in requiredEdges:
    nodes.add(edge[0])
    nodes.add(edge[1])
nodes = sorted(list(nodes))
graph.dijkstra(nodes)#得到所有可能需要的边

solution, record = SimulatedAnnealing(state,
                                      schedule=lambda t: 0.999 ** t,
                                      halt=lambda T: T < 1e-9)
s, c = TotalCost(solution)

# 格式化输出
print("s", end=' ')
for i in s:
    print(i, end=',')
print(0)
print("q %d" % c)

print(time.time() - start)
# print(solution)
plt.plot(record)
plt.xlabel("time step")
plt.ylabel("value")
plt.show()
