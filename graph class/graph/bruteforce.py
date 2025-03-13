from itertools import permutations

def get_distance(graph, path):
    """Calculate the total distance of a given path."""
    distance = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if v in graph[u]:
            distance += graph[u][v]
        else:
            return float('inf')  # Invalid path
    return distance

def brute_force_shortest_path(graph, start, end):
    """Find the shortest path using brute force approach."""
    nodes = list(graph.keys())
    nodes.remove(start)
    nodes.remove(end)
    
    min_distance = float('inf')
    best_path = None
    
    for perm in permutations(nodes):
        path = [start] + list(perm) + [end]
        distance = get_distance(graph, path)
        if distance < min_distance:
            min_distance = distance
            best_path = path
    
    return best_path, min_distance

# Defining the graph as an adjacency dictionary with weights
graph = {
    'Vandel': {'Randbøldal': 3, 'Billund': 7},
    'Randbøldal': {'Vandel': 3, 'Vorbasse': 15, 'Bække': 15},
    'Billund': {'Vandel': 7, 'Vorbasse': 14, 'Hejnsvig': 9},
    'Vorbasse': {'Billund': 14, 'Randbøldal': 15, 'Hejnsvig': 9, 'Bække': 8, 'Lindknud': 10},
    'Hejnsvig': {'Billund': 9, 'Vorbasse': 9, 'Hovborg': 12},
    'Bække': {'Randbøldal': 15, 'Vorbasse': 8, 'Eskelund': 11, 'Lindknud': 9},
    'Eskelund': {'Bække': 11, 'Lindknud': 8, 'Holsted': 9},
    'Lindknud': {'Vorbasse': 10, 'Bække': 9, 'Eskelund': 8, 'Hovborg': 7, 'Holsted': 11},
    'Hovborg': {'Hejnsvig': 12, 'Lindknud': 7, 'Holsted': 12},
    'Holsted': {'Eskelund': 9, 'Lindknud': 11, 'Hovborg': 12}
}

# Find the shortest path from Vandel to Holsted
shortest_path, distance = brute_force_shortest_path(graph, 'Vandel', 'Holsted')
print(f"Shortest Path: {shortest_path}")
print(f"Total Distance: {distance}")