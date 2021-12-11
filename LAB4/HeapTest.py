import heapq

li = [(9,'A'), (10,'d'),(2,'D')];
minheap = []

for item in li:
    heapq.heappush(minheap, item)

print(minheap)
print(sorted(li))

random_lst = [5, 7, 2, 1, 6, 10, 8, 9]
heap_lst = []

for item in random_lst:
    heapq.heappush(heap_lst, item)

print(heap_lst)