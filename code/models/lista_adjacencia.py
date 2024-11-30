class ListaAdjacencia:
    def __init__(self, num_vertices, dirigido=False):
        self.num_vertices = num_vertices
        self.dirigido = dirigido
        self.adjacencias = {i: [] for i in range(num_vertices)}

    def adicionar_aresta(self, u, v, peso=1, label=None):
        if not self.checar_adjacencia(u, v):
            self.adjacencias[u].append((v, peso))
            if not self.dirigido:
                self.adjacencias[v].append((u, peso))

    def remover_aresta(self, u, v):
        self.adjacencias[u] = [w for w in self.adjacencias[u] if w[0] != v]
        if not self.dirigido:
            self.adjacencias[v] = [w for w in self.adjacencias[v] if w[0] != u]

    def checar_adjacencia(self, u, v):
        return any(w == v for w, _ in self.adjacencias[u])

    def exibir(self):
        for vertice, adj in self.adjacencias.items():
            print(f"{vertice}: {adj}")
