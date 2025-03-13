class Graph:
    def __init__(self, size):
        self.adj_matrix = [[None] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size
    
    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight  # Directed edge with weight
    
    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data
    
    def print_graph(self):
        print("Adjacency Matrix:")
        for row in self.adj_matrix:
            print(' '.join(map(lambda x: str(x) if x is not None else '0', row)))
        
        print('\nVertex Data:')
        for vertex, data in enumerate(self.vertex_data):
            print(f'Vertex {vertex}: {data}')

# Testing the Weighted Directed Graph
g = Graph(4)
g.add_vertex_data(0, 'livingroom')
g.add_vertex_data(1, 'toilet')
g.add_vertex_data(2, 'bedroom')
g.add_vertex_data(3, 'kitchen')

g.add_edge(0, 1, 5)
g.add_edge(0, 2, 3)
g.add_edge(2, 3, 7)
g.add_edge(1, 2, 2)

g.print_graph()