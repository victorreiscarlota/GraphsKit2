# models/lista_adjacencia.py

class ListaAdjacencia:
    def __init__(self, num_vertices, dirigido=False):
        self.num_vertices = num_vertices
        self.dirigido = dirigido
        # Armazena uma lista de tuplas (v, peso, label) para cada vértice
        self.adjacencias = {i: [] for i in range(num_vertices)}

    def adicionar_aresta(self, u, v, peso=1, label=None):
        if not self.checar_adjacencia(u, v):
            # Adiciona a aresta com vértice, peso e rótulo
            self.adjacencias[u].append((v, peso, label))
            if not self.dirigido:
                self.adjacencias[v].append((u, peso, label))
            # Mensagem removida para evitar duplicação

    def remover_aresta(self, u, v):
        # Remove a aresta removendo todas as tuplas que têm o vértice v
        self.adjacencias[u] = [w for w in self.adjacencias[u] if w[0] != v]
        if not self.dirigido:
            self.adjacencias[v] = [w for w in self.adjacencias[v] if w[0] != u]
        # Mensagem removida para evitar duplicação

    def checar_adjacencia(self, u, v):
        # Verifica se existe alguma tupla com vértice v
        return any(w[0] == v for w in self.adjacencias[u])

    def exibir(self):
        print("Lista de Adjacência:")
        for vertice, adj in self.adjacencias.items():
            # Converte para exibição 1-based
            vertice_exibicao = vertice + 1
            # Cria uma lista de rótulos para as arestas adjacentes
            adj_exibicao = [f"{v + 1} ({label})" if label else f"{v + 1}" for v, _, label in adj]
            print(f"{vertice_exibicao}: {adj_exibicao}")
