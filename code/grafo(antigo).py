from models.lista_adjacencia import ListaAdjacencia
from models.matriz_adjacencia import MatrizAdjacencia
from models.matriz_incidencia import MatrizIncidencia
from utils.gexf_exporter import GEXFExporter
from utils.ppm_exporter import PPMExporter
from utils.txt_exporter import TXTExporter
from utils.desenhador import Desenhador
import os

class Grafo:
    def __init__(self, num_vertices, dirigido=False, nome=""):
        self.num_vertices = num_vertices
        self.dirigido = dirigido
        self.nome = nome
        self.lista_adj = ListaAdjacencia(num_vertices, dirigido)
        self.matriz_adj = MatrizAdjacencia(num_vertices, dirigido)
        self.matriz_inc = MatrizIncidencia(num_vertices, dirigido)
        self.edge_list = []
        self.vertex_labels = {i: f"V{i + 1}" for i in range(num_vertices)}
        self.tempo = 0
        self.frame_count = 0
        self.desenhador = Desenhador()

    def adicionar_vertice(self, label=None):
        v = self.num_vertices
        self.lista_adj.num_vertices += 1
        self.matriz_adj.num_vertices += 1
        self.matriz_inc.num_vertices += 1
        self.num_vertices += 1
        self.lista_adj.adjacencias[v] = []
        
        for row in self.matriz_adj.adj_matrix:
            row.append(0)
        self.matriz_adj.adj_matrix.append([0] * self.matriz_adj.num_vertices)
        
        for row in self.matriz_inc.inc_matrix:
            row.append(0)
        
        self.vertex_labels[v] = label if label else f"V{v + 1}"

    def adicionar_aresta(self, u, v, peso=1, label=None):
        self.lista_adj.adicionar_aresta(u, v, peso, label)
        self.matriz_adj.adicionar_aresta(u, v, peso)
        self.matriz_inc.adicionar_aresta(u, v, peso, label)
        self.edge_list.append({'u': u, 'v': v, 'peso': peso, 'label': label})

    def remover_aresta(self, u, v):
        self.lista_adj.remover_aresta(u, v)
        self.matriz_adj.remover_aresta(u, v)
        self.matriz_inc.remover_aresta(u, v)
        
        for i, edge in enumerate(self.edge_list):
            if edge['u'] == u and edge['v'] == v:
                del self.edge_list[i]
                break
            if not self.dirigido and edge['u'] == v and edge['v'] == u:
                del self.edge_list[i]
                break

    def checar_adjacencia_vertices(self, u, v):
        return (self.lista_adj.checar_adjacencia(u, v) and
                self.matriz_adj.checar_adjacencia(u, v) and
                self.matriz_inc.checar_adjacencia(u, v))

    def contar_vertices_arestas(self):
        num_vertices = self.num_vertices
        num_arestas = len(self.edge_list)
        return num_vertices, num_arestas

    def grafo_vazio(self):
        return self.contar_vertices_arestas()[1] == 0

    def grafo_completo(self):
        for u in range(self.num_vertices):
            grau = len(self.lista_adj.adjacencias[u])
            if self.dirigido:
                if grau != self.num_vertices - 1:
                    return False
            else:
                if grau != self.num_vertices - 1:
                    return False
        return True

    def identificar_pontes_naive(self):
        pontes = []
        for u in range(self.num_vertices):
            for v, _ in list(self.lista_adj.adjacencias[u]):
                if (u < v) or self.dirigido:
                    self.remover_aresta(u, v)
                    if not self.grafo_conexo():
                        pontes.append((u, v))
                    self.adicionar_aresta(u, v)
        return pontes

    def identificar_pontes_tarjan(self):
        num = [0] * self.num_vertices
        low = [0] * self.num_vertices
        self.tempo = 1
        pontes = []
        visited = [False] * self.num_vertices
        parent = [-1] * self.num_vertices

        for u in range(self.num_vertices):
            if not visited[u]:
                self._tarjan_dfs(u, visited, parent, num, low, pontes)
        return pontes

    def _tarjan_dfs(self, u, visited, parent, num, low, pontes):
        stack = [(u, iter(self.lista_adj.adjacencias[u]))]
        visited[u] = True
        num[u] = low[u] = self.tempo
        self.tempo += 1

        while stack:
            v, children = stack[-1]
            try:
                w, _ = next(children)
                if not visited[w]:
                    parent[w] = v
                    visited[w] = True
                    num[w] = low[w] = self.tempo
                    self.tempo += 1
                    stack.append((w, iter(self.lista_adj.adjacencias[w])))
                elif w != parent[v]:
                    low[v] = min(low[v], num[w])
            except StopIteration:
                stack.pop()
                if parent[v] != -1:
                    low[parent[v]] = min(low[parent[v]], low[v])
                    if low[v] > num[parent[v]]:
                        pontes.append((parent[v], v))

    def identificar_articulacoes(self):
        num = [0] * self.num_vertices
        low = [0] * self.num_vertices
        parent = [-1] * self.num_vertices
        self.tempo = 1
        articulacoes = set()
        visited = [False] * self.num_vertices

        for u in range(self.num_vertices):
            if not visited[u]:
                self._articulacao_dfs(u, visited, parent, num, low, articulacoes)
        return list(articulacoes)

    def _articulacao_dfs(self, u, visited, parent, num, low, articulacoes):
        stack = [(u, iter(self.lista_adj.adjacencias[u]), False)]
        children = 0
        visited[u] = True
        num[u] = low[u] = self.tempo
        self.tempo += 1
        articulation_found = False

        while stack:
            v, children_iter, is_return = stack[-1]
            if not is_return:
                stack[-1] = (v, children_iter, True)
                try:
                    w, _ = next(children_iter)
                    if not visited[w]:
                        parent[w] = v
                        children += 1
                        visited[w] = True
                        num[w] = low[w] = self.tempo
                        self.tempo += 1
                        stack.append((w, iter(self.lista_adj.adjacencias[w]), False))
                    elif w != parent[v]:
                        low[v] = min(low[v], num[w])
                except StopIteration:
                    stack.pop()
                    if parent[v] != -1:
                        low[parent[v]] = min(low[parent[v]], low[v])
                        if low[v] >= num[parent[v]]:
                            articulacoes.add(parent[v])
                    else:
                        if children > 1:
                            articulacoes.add(v)
            else:
                stack.pop()

    def grafo_conexo(self):
        if self.num_vertices == 0:
            return True
        visitados = [False] * self.num_vertices
        stack = [0]
        visitados[0] = True
        while stack:
            v = stack.pop()
            for w, _ in self.lista_adj.adjacencias[v]:
                if not visitados[w]:
                    visitados[w] = True
                    stack.append(w)
        return all(visitados)

    def kosaraju_scc(self):
        visited = [False] * self.num_vertices
        stack = []

        def dfs_fill_order(v):
            visited[v] = True
            for w, _ in self.lista_adj.adjacencias[v]:
                if not visited[w]:
                    dfs_fill_order(w)
            stack.append(v)

        for i in range(self.num_vertices):
            if not visited[i]:
                dfs_fill_order(i)

        transposto = {i: [] for i in range(self.num_vertices)}
        for u in self.lista_adj.adjacencias:
            for v, peso in self.lista_adj.adjacencias[u]:
                transposto[v].append((u, peso))

        visited = [False] * self.num_vertices
        scc_list = []

        def dfs_transpose(v, component):
            visited[v] = True
            component.append(v)
            for w, _ in transposto[v]:
                if not visited[w]:
                    dfs_transpose(w, component)

        while stack:
            v = stack.pop()
            if not visited[v]:
                component = []
                dfs_transpose(v, component)
                scc_list.append(component)

        return scc_list

    def grafo_fortemente_conexo(self):
        if not self.dirigido:
            return self.grafo_conexo()
        scc = self.kosaraju_scc()
        return len(scc) == 1

    def grafo_conexo_fraco(self):
        if not self.dirigido:
            return self.grafo_conexo()
        visitados = [False] * self.num_vertices
        stack = [0]
        visitados[0] = True
        while stack:
            v = stack.pop()
            for w, _ in self.lista_adj.adjacencias[v]:
                if not visitados[w]:
                    visitados[w] = True
                    stack.append(w)
            for u in range(self.num_vertices):
                if self.lista_adj.checar_adjacencia(u, v) and not visitados[u]:
                    visitados[u] = True
                    stack.append(u)
        return all(visitados)

    def grafo_semi_fortemente_conexo(self):
        if not self.dirigido:
            return self.grafo_conexo()
        for i in range(self.num_vertices):
            visitados = [False] * self.num_vertices
            stack = [i]
            visitados[i] = True
            while stack:
                v = stack.pop()
                for w, _ in self.lista_adj.adjacencias[v]:
                    if not visitados[w]:
                        visitados[w] = True
                        stack.append(w)
                for u in range(self.num_vertices):
                    if self.lista_adj.checar_adjacencia(u, v) and not visitados[u]:
                        visitados[u] = True
                        stack.append(u)
            if not all(visitados):
                return False
        return True

    def fleury(self):
        if not self.grafo_euleriano():
            print("O grafo não é Euleriano.")
            return []
        grafo_copia = Grafo(self.num_vertices, self.dirigido, self.nome)
        grafo_copia.lista_adj.adjacencias = {v: list(self.lista_adj.adjacencias[v]) for v in self.lista_adj.adjacencias}
        grafo_copia.matriz_adj.adj_matrix = [row.copy() for row in self.matriz_adj.adj_matrix]
        grafo_copia.matriz_inc.inc_matrix = [row.copy() for row in self.matriz_inc.inc_matrix]
        grafo_copia.edge_list = list(self.edge_list)
        grafo_copia.vertex_labels = dict(self.vertex_labels)

        caminho = []
        atual = 0
        while grafo_copia.contar_vertices_arestas()[1] > 0:
            if not grafo_copia.lista_adj.adjacencias[atual]:
                break
            for vizinho, _ in list(grafo_copia.lista_adj.adjacencias[atual]):
                grafo_copia.remover_aresta(atual, vizinho)
                if not grafo_copia.grafo_conexo():
                    grafo_copia.adicionar_aresta(atual, vizinho)
                else:
                    caminho.append((atual, vizinho))
                    atual = vizinho
                    break
        return caminho

    def grafo_euleriano(self):
        if not self.grafo_conexo():
            return False
        graus = [len(self.lista_adj.adjacencias[v]) for v in self.lista_adj.adjacencias]
        return all(g % 2 == 0 for g in graus)

    def exportar_para_gexf(self, nome_arquivo="grafo.gexf"):
        GEXFExporter.exportar(self, nome_arquivo)

    def exportar_para_ppm(self, nome_arquivo="grafo.ppm"):
        PPMExporter.exportar(self, nome_arquivo)

    def exportar_para_txt(self, nome_arquivo="grafo.txt"):
        TXTExporter.exportar(self, nome_arquivo)

    def exibir_lista_adjacencia(self):
        print("Lista de Adjacência:")
        for vertice, adj in self.lista_adj.adjacencias.items():
            vertice_exibicao = vertice + 1
            adj_exibicao = [(v + 1, peso) for v, peso in adj]
            print(f"{vertice_exibicao}: {adj_exibicao}")

    def exibir_matriz_adjacencia(self):
        print("Matriz de Adjacência:")
        header = "   " + " ".join([f"{i+1:3}" for i in range(self.num_vertices)])
        print(header)
        for i, row in enumerate(self.matriz_adj.adj_matrix):
            linha = f"{i+1:3} " + " ".join([f"{val:3}" for val in row])
            print(linha)

    def exibir_matriz_incidencia(self):
        print("Matriz de Incidência:")
        header = "   " + " ".join([f"{i+1:3}" for i in range(len(self.edge_list))])
        print(header)
        for i, row in enumerate(self.matriz_inc.inc_matrix):
            linha = f"{i+1:3} " + " ".join([f"{val:3}" for val in row])
            print(linha)

    def exibir_representacoes(self):
        self.exibir_lista_adjacencia()
        print()
        self.exibir_matriz_adjacencia()
        print()
        self.exibir_matriz_incidencia()
