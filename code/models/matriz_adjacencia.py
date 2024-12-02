class MatrizAdjacencia:
    def __init__(self, num_vertices, dirigido=False):
        self.num_vertices = num_vertices
        self.dirigido = dirigido
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def adicionar_aresta(self, u, v, peso=1):
        self.adj_matrix[u][v] = peso
        if not self.dirigido:
            self.adj_matrix[v][u] = peso

    def remover_aresta(self, u, v):
        self.adj_matrix[u][v] = 0
        if not self.dirigido:
            self.adj_matrix[v][u] = 0

    def checar_adjacencia(self, u, v):
        return self.adj_matrix[u][v] != 0

    def exibir(self):
        for row in self.adj_matrix:
            print(row)
