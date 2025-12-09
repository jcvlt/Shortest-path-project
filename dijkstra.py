# dijkstra.py
import math
import heapq

def build_graph(nodes, edges):
    graph = {name: [] for name in nodes}
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph


def dijkstra(graph, start):
    dist = {node: math.inf for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0

    heap = [(0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            alt = current_dist + weight
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    return dist, prev


def reconstruct_path(prev, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = prev[current]
    path.reverse()
    if not path or path[0] != start:
        return []
    return path
