import networkx as nx
import matplotlib.pyplot as plt

# networkx version 2.3
# matplotlib version 2.2.3
# !!! When dealing with nodes under the same distance/situation, pop them by alphabet order
# eg.When BFS face with A and B with same distance, pop A first then pop B
# Finish one of the three search method is enough for lab exercise but try more if you want to get familar with python quickly.
# Modify any code you want to modify, try to make your hands dirty.
# Author Jimmy Gao


def vis(colors, position,G):
    fig, ax = plt.subplots()
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    nx.draw(G, pos=position, with_labels=True, node_color=colors)  # get positions
    nx.draw_networkx_edge_labels(G, position, edge_labels=edge_labels)  # draw edge
    ax.xaxis.set_major_locator(plt.NullLocator())  # delete x axis
    ax.yaxis.set_major_locator(plt.NullLocator())  # delete y axis
    plt.show()


def BFS(Graph):
    """
    Write your BFS in python and get familar with python dictionary structure

    Args
    - Graph: a node dict contains all edges and their weights. keys are nodes' names. values are tuple (End_node,weight).
    - eg: Graph["S"]:[('R', '80'), ('F', '99')]
    - means there is an edge from S to R with weight 80 and an edge from S to F with weight 99
    Returns
    - do not need to return,but don't forget to yield the list
    - eg. queue:['S']

    """
    queue = ['S']
    # TODO: write your code :)
    # Initialize queue here

    while len(queue) != 0:
        yield queue  # yield queue whenever before an element popped out from the queue
        next_nd = queue.pop(0)
        if next_nd in Graph:
            for nd in sorted(Graph[next_nd]):
                if nd[0] not in queue:
                    queue.append(nd[0])


    # TODO: write your code :)
    # write your algorithm

def DFS(Graph):
    """
    Write your DFS in python and get familar with python dictionary structure

    Args
    - Graph: a node dict contains all edges and their weights. keys are nodes' names. values are tuple (End_node,weight).
    - eg: Graph["S"]:[('R', '80'), ('F', '99')]
    - means there is an edge from S to R with weight 80 and an edge from S to F with weight 99
    Returns
    - do not need to return,but don't forget to yield the list
    - eg. stack:['S']

    """

    stack = []
    # TODO: write your code :)
    # Initialize stack here
    yield stack  # yield stack whenever before an element popped out from the stack
    # TODO: write your code :)
    # write your algorithm

def UCS(Graph):
    """
    Write your UCS in python and get familar with python dictionary structure

    Args
    - Graph: a node dict contains all edges and their weights. keys are nodes' names. values are tuple (End_node,weight).
    - eg: Graph["S"]:[('R', '80'), ('F', '99')]
    - means there is an edge from S to R with weight 80 and an edge from S to F with weight 99
    Returns
    - do not need to return,but don't forget to yield the list
    - eg. queue:['S']

    """

    queue = []
    # TODO: write your code :)
    # Initialize queue here
    yield queue  # yield queue whenever before an element popped out from the queue
    # TODO: write your code :)
    # write your algorithm

if __name__ == '__main__':

    test_case = 1  # TODO: change here to test another case
    G = nx.DiGraph()  # for visualization
    position = {}
    result = []

    """
    sample:
    input file description:
    S A B C D E F G H =>names of all nodes
    13                =>total number of edges, next N lines are edges
    S A 3             =>(Start,End,Weight) means an edge from node'S'to node'N' with weight 3  
    A D 3             =>an edge from node'A'to node'D' with weight 3 
    S B 6             =>an edge from node'S'to node'B' with weight 6 
    S C 2             =>an edge from node'S'to node'C' with weight 2 
    B D 4             =>an edge from node'B'to node'D' with weight 4 
    B G 9             =>an edge from node'B'to node'G' with weight 9 
    B E 2             =>an edge from node'B'to node'E' with weight 2 
    D F 5             =>an edge from node'D'to node'F' with weight 5 
    E F 6             =>an edge from node'E'to node'F' with weight 6 
    E H 5             =>an edge from node'E'to node'H' with weight 5 
    F G 5             =>an edge from node'F'to node'G' with weight 5 
    H G 8             =>an edge from node'H'to node'G' with weight 8 
    C E 1             =>an edge from node'C'to node'E' with weight 1 
    -1 0 0 1 0 0 0 -1 1 1 1 -1 1.8 1 2.5 0 1.8 -1 
    # Positions in visualization (x,y)
    # -1 0 means node'S' position at (-1,0)
    # 0 1 means node 'A' position at (0,1)
    # ...

    """

    # read file
    with open(f'./test_cases/{test_case}.txt', 'r') as f:
        line = f.readline()
        all_nodes = line.strip().split(" ")
        line = f.readline()
        for i in range(int(line)):
            line = f.readline()
            edge = line.strip().split(" ")
            G.add_edge(edge[0], edge[1], weight=int(edge[2]))
        pos = f.readline().strip().split(" ")
        for i in range(len(all_nodes)):
            position[all_nodes[i]] = (float(pos[i * 2]), float(pos[2 * i + 1]))
    Graph = dict([(u, []) for u, v, d in G.edges(data=True)])
    for u, v, d in G.edges(data=True):
        Graph[u].append((v, d["weight"]))

    #Visualization
    gray = (0.5, 0.5, 0.5)
    brown = (0.5, 0.25, 0)
    white = (1, 1, 1)
    colors_list = [(_i, white) for _i in G.nodes]
    colors_dict = dict(colors_list)
    res = BFS(Graph)  # TODO: change here to your implemented algorithm
    q = next(res)
    last_node = None
    while True:
        try:
            for node in G.nodes:
                if node in q and colors_dict[node] == white:
                    colors_dict[node] = brown
                elif node not in q and colors_dict[node] == brown:
                    colors_dict[node] = gray
                    result.append(node)
            nodes, colors = zip(*colors_dict.items())
            vis(colors, position, G)
            if white not in colors:
                last_node = q[0]
            q = next(res)
        except StopIteration:
            break
    for node in G.nodes:
        if node == last_node:
            colors_dict[node] = gray
    result.append(last_node)
    nodes, colors = zip(*colors_dict.items())
    vis(colors, position, G)
    print(result)