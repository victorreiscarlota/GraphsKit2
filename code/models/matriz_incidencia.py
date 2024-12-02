class MatrizIncidencia:
    def __init__(self, num_vertices, dirigido=False):
        self.num_vertices = num_vertices
        self.dirigido = dirigido
        self.inc_matrix = []  
        self.edge_list = []   

    def adicionar_aresta(self, u, v, peso=1, label=None):
        self.edge_list.append({'u': u, 'v': v, 'peso': peso, 'label': label})
        edge_index = len(self.edge_list) - 1

        for row in self.inc_matrix:
            row.append(0)
        
        nova_coluna = [0] * self.num_vertices
        nova_coluna[u] = 1
        if not self.dirigido:
            nova_coluna[v] = 1
        else:
            nova_coluna[v] = -1
        self.inc_matrix.append(nova_coluna)

    def remover_aresta(self, u, v):
        for i, edge in enumerate(self.edge_list):
            if edge['u'] == u and edge['v'] == v:
                del self.edge_list[i]
                del self.inc_matrix[i]
                for row in self.inc_matrix:
                    del row[i]
                break

    def checar_adjacencia(self, u, v):
        for edge in self.edge_list:
            if edge['u'] == u and edge['v'] == v:
                return True
            if not self.dirigido and edge['u'] == v and edge['v'] == u:
                return True
        return False

    def exibir(self):
        print("Matriz de Incidência:")
        for row in self.inc_matrix:
            print(row)
