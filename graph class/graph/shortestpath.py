import itertools

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def get_all_paths(self, start, end, path=[], path_length=0):
        path = path + [start]
        if start == end:
            return [(path, path_length)]
        if start not in self.graph:
            return []
        paths = []
        for node, weight in self.graph[start]:
            if node not in path:
                new_paths = self.get_all_paths(node, end, path, path_length + weight)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def find_shortest_path(self, start, end):
        paths = self.get_all_paths(start, end)
        if not paths:
            return None, float('inf')
        shortest_path = min(paths, key=lambda x: x[1])
        return shortest_path


g = Graph()

# Adding edges from the provided graph
g.add_edge("Vandel", "Randb\u00f8ldal", 3)
g.add_edge("Vandel", "Billund", 7)
g.add_edge("Randb\u00f8ldal", "B\u00e6kke", 15)
g.add_edge("Randb\u00f8ldal", "Vorbasse", 15)
g.add_edge("B\u00e6kke", "Eskelund", 11)
g.add_edge("Vorbasse", "Lindknud", 10)
g.add_edge("Vorbasse", "Billund", 14)
g.add_edge("Vorbasse", "Hejnsvig", 9)
g.add_edge("Lindknud", "Eskelund", 8)
g.add_edge("Lindknud", "Holsted", 11)
g.add_edge("Lindknud", "Hovborg", 7)
g.add_edge("Hejnsvig", "Hovborg", 12)
g.add_edge("Hovborg", "Holsted", 12)

g.add_edge("Eskelund", "Holsted", 9)

g.add_edge("B\u00e6kke", "Lindknud", 9)

g.add_edge("Vorbasse", "Hovborg", 10)

# Taking user input
start_city = input("Enter the starting city: ")
end_city = input("Enter the destination city: ")

shortest_path, shortest_distance = g.find_shortest_path(start_city, end_city)

if shortest_path:
    print(f"Shortest path from {start_city} to {end_city}: {' -> '.join(shortest_path)} with distance {shortest_distance}")
else:
    print("No path found between the given cities.")
