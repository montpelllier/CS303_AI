import argparse
import heapq
import time


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


parser = argparse.ArgumentParser(description="CARP")
parser.add_argument('file', help="is the absolute path of the test CARP instance file.")
parser.add_argument('-t', help="specifies the termination condition of your algorithm.")
parser.add_argument('-s', help="specifies the random seed used in this run.")

args = parser.parse_args()  # 处理命令行输入参数

# print(args)
f = open(args.file, 'r')
lines = f.readlines()

vertices = int(lines[1].split()[-1].split("\n")[-1])
depot = int(lines[2].split()[-1].split("\n")[-1])
edges = int(lines[3].split()[-1].split("\n")[-1]) + int(lines[4].split()[-1].split("\n")[-1])
capacity = int(lines[6].split()[-1].split("\n")[-1])
# requiredCost = int(lines[7].split()[-1].split("\n")[-1])

# print("edges:", edges, "capacity:", capacity, "requiredCost:", requiredCost)

graph, requiredCost = {}, {}

start = time.time()
for line in lines[9:9 + edges]:
    data = list(map(int, line.split()))
    v1, v2 = min(data[0], data[1]), max(data[0], data[1])
    graph[(v1, v2)] = data[2]
    if data[3] != 0:
        requiredCost[(v1, v2)] = data[3]
# print(time.time() - start)
# print(graph)#字典存边
graph = Graph(graph)

state = list(requiredCost.keys())


# print(state)

def TotalCost(state):
    cost = 0
    capa = capacity
    prev_node = depot
    s = [0]
    for edge in state:

        cor_edge = (min(edge[0], edge[1]), max(edge[0], edge[1]))
        if capa - requiredCost[cor_edge] < 0:  # 装满了返程
            # 计算回去的路程
            back_path = (min(depot, prev_node), max(depot, prev_node))

            if prev_node == depot:
                shortest = 0
            elif back_path not in graph.ShortestCost:
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
            graph.dijkstra(min_node, max_node)
            shortest = graph.ShortestCost[(min_node, max_node)]
        else:  # 有记录直接取值
            shortest = graph.ShortestCost[(min_node, max_node)]

        cost += shortest + graph.Edges[cor_edge]  #
        # print(cost, " ", cor_edge, " ", (prev_node, next_node))
        capa -= requiredCost[cor_edge]
        s.append(edge)
        prev_node = edge[1]
        if edge == state[-1]:  # 结束后返程
            back_path = (min(depot, prev_node), max(depot, prev_node))
            if prev_node == depot:
                shortest = 0
            elif back_path not in graph.ShortestCost:
                graph.dijkstra(back_path[0], back_path[1])
                shortest = graph.ShortestCost[back_path]
            else:
                shortest = graph.ShortestCost[back_path]

            cost += shortest
            # s.append(0)# 切割线路
    return s, cost


s, cost = TotalCost(state)
print("s", end=' ')
for i in s:
    print(i, end=',')
print(0)
print("q %d" % cost)
# print(time.time() - start)