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

            print(pop_node, end_node)

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
            print(distance)
            print(min_heap)


graph = {(1, 8): 9, (1, 9): 4, (1, 10): 13, (1, 11): 12, (2, 1): 11, (2, 3): 15, (2, 4): 18, (2, 5): 8, (3, 4): 8,
         (3, 8): 18, (3, 9): 6, (4, 1): 7, (4, 6): 10, (4, 11): 17, (5, 1): 9, (5, 6): 15, (6, 11): 3, (7, 2): 6,
         (7, 4): 11, (7, 5): 5, (8, 9): 14, (8, 12): 5, (9, 10): 19, (10, 12): 2, (11, 12): 7}

a = Graph(graph)
start = time.time()
a.dijkstra(7, 11)
print(a.ShortestCost[(7, 11)])
print(time.time() - start)
