from models.lista_adjacencia import ListaAdjacencia
from models.matriz_adjacencia import MatrizAdjacencia
from models.matriz_incidencia import MatrizIncidencia
from utils.graphml_exporter import GraphMLExporter
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
        self.vertex_weights = {i: 1 for i in range(num_vertices)}
        self.tempo = 0
        self.frame_count = 0
        self.desenhador = Desenhador()

    def adicionar_vertice(self, label=None, peso=1):
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
        self.vertex_weights[v] = peso

    def remover_vertice(self, v):
        if v < 0 or v >= self.num_vertices:
            print(f"Erro: Vértice inválido. Deve estar entre 1 e {self.num_vertices}.")
            return
        arestas_para_remover = [edge for edge in self.edge_list if edge['u'] == v or edge['v'] == v]
        for edge in arestas_para_remover:
            self.remover_aresta(edge['u'], edge['v'])
        del self.lista_adj.adjacencias[v]
        self.matriz_adj.adj_matrix.pop(v)
        for row in self.matriz_adj.adj_matrix:
            row.pop(v)
        self.matriz_inc.inc_matrix.pop(v)
        for row in self.matriz_inc.inc_matrix:
            row.pop(v)
        del self.vertex_labels[v]
        del self.vertex_weights[v]
        self.num_vertices -= 1

    def definir_rotulo_vertice(self, v, novo_rotulo):
        if v < 0 or v >= self.num_vertices:
            print(f"Erro: Vértice inválido. Deve estar entre 1 e {self.num_vertices}.")
            return
        self.vertex_labels[v] = novo_rotulo

    def definir_peso_vertice(self, v, novo_peso):
        if v < 0 or v >= self.num_vertices:
            print(f"Erro: Vértice inválido. Deve estar entre 1 e {self.num_vertices}.")
            return
        self.vertex_weights[v] = novo_peso

    def obter_rotulo_vertice(self, v):
        return self.vertex_labels.get(v, f"V{v + 1}")

    def obter_peso_vertice(self, v):
        return self.vertex_weights.get(v, 1)

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
            adjacentes = list(self.lista_adj.adjacencias[u])
            for v, peso in adjacentes:
                if (u < v) or self.dirigido:
                    self.lista_adj.adjacencias[u] = [w for w in self.lista_adj.adjacencias[u] if w[0] != v]
                    if not self.dirigido:
                        self.lista_adj.adjacencias[v] = [w for w in self.lista_adj.adjacencias[v] if w[0] != u]
                    if not self.grafo_conexo():
                        pontes.append((u, v))
                    self.lista_adj.adjacencias[u].append((v, peso))
                    if not self.dirigido:
                        self.lista_adj.adjacencias[v].append((u, peso))
        return pontes

    def identificar_pontes_naive_novo(self):
        pontes = []
        N = self.num_vertices + 1
        gr1 = {}
        gr2 = {}
        vist1 = [0] * N
        vist2 = [0] * N

        for edge in self.edge_list:
            self.add_edge(edge['u'] + 1, edge['v'] + 1, gr1, gr2)

        for edge in self.edge_list:
            self.remove_edge_naive(edge['u'] + 1, edge['v'] + 1, gr1, gr2)
            if not self.is_connected(N - 1, vist1, vist2, gr1, gr2):
                pontes.append((edge['u'], edge['v']))
            self.add_edge(edge['u'] + 1, edge['v'] + 1, gr1, gr2)

        return pontes

    def remove_edge_naive(self, u, v, gr1, gr2):
        if u not in gr1 or v not in gr2:
            return
        if v in gr1[u]:
            gr1[u].remove(v)
        if u in gr2[v]:
            gr2[v].remove(u)

    def add_edge(self, u, v, gr1, gr2):
        if u not in gr1:
            gr1[u] = []
        if v not in gr2:
            gr2[v] = []
        gr1[u].append(v)
        gr2[v].append(u)

    def dfs1(self, x, gr1):
        global vis1
        vis1[x] = True
        if x not in gr1:
            gr1[x] = {}
        for i in gr1[x]:
            if not vis1[i]:
                self.dfs1(i, gr1)

    def dfs2(self, x, gr2):
        global vis2
        vis2[x] = True
        if x not in gr2:
            gr2[x] = {}
        for i in gr2[x]:
            if not vis2[i]:
                self.dfs2(i, gr2)

    def is_connected(self, n, vist1, vist2, gr1, gr2):
        global vis1
        global vis2
        vis1 = [False] * len(vist1)
        self.dfs1(1, gr1)
        vis2 = [False] * len(vist2)
        self.dfs2(1, gr2)
        for i in range(1, n + 1):
            if not vis1[i] and not vis2[i]:
                return False
        return True

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

    def identificar_pontes_tarjan_novo(self):
        num = [0] * self.num_vertices
        low = [0] * self.num_vertices
        self.tempo = 1
        pontes = []
        visited = [False] * self.num_vertices
        parent = [-1] * self.num_vertices
        for u in range(self.num_vertices):
            if not visited[u]:
                self._tarjan_novo_dfs(u, visited, parent, num, low, pontes)
        return pontes

    def _tarjan_novo_dfs(self, u, visited, parent, num, low, pontes):
        visited[u] = True
        num[u] = low[u] = self.tempo
        self.tempo += 1
        for v, _ in self.lista_adj.adjacencias[u]:
            if not visited[v]:
                parent[v] = u
                self._tarjan_novo_dfs(v, visited, parent, num, low, pontes)
                low[u] = min(low[u], low[v])
                if low[v] > num[u]:
                    pontes.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], num[v])

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
            print("O grafo não é Euleriano ou Semi-Euleriano.")
            return []
        grafo_aux = self.criar_copia()
        vertice_inicial = self.definir_vertice_inicial()
        caminho = []
        atual = vertice_inicial
        while grafo_aux.contar_vertices_arestas()[1] > 0:
            proximo = self.selecionar_aresta_valida(grafo_aux, atual)
            if proximo is not None:
                caminho.append((atual, proximo))
                atual = proximo
            else:
                break
        return caminho

    def grafo_euleriano(self):
        if not self.grafo_conexo():
            return False
        graus = [len(self.lista_adj.adjacencias[v]) for v in self.lista_adj.adjacencias]
        impares = sum(g % 2 for g in graus)
        return impares in [0, 2]

    def criar_copia(self):
        grafo_aux = Grafo(self.num_vertices, self.dirigido, self.nome)
        grafo_aux.lista_adj.adjacencias = {v: list(self.lista_adj.adjacencias[v]) for v in self.lista_adj.adjacencias}
        grafo_aux.edge_list = list(self.edge_list)
        grafo_aux.vertex_labels = dict(self.vertex_labels)
        grafo_aux.vertex_weights = dict(self.vertex_weights)
        return grafo_aux

    def definir_vertice_inicial(self):
        graus = [len(self.lista_adj.adjacencias[v]) for v in self.lista_adj.adjacencias]
        for v, g in enumerate(graus):
            if g % 2 != 0:
                return v
        return 0

    def selecionar_aresta_valida(self, grafo_aux, atual):
        for vizinho, _ in list(grafo_aux.lista_adj.adjacencias[atual]):
            grafo_aux.remover_aresta(atual, vizinho)
            if not grafo_aux.grafo_conexo():
                grafo_aux.adicionar_aresta(atual, vizinho)
            else:
                return vizinho
        return None

    def exportar(self, nome_base="grafo", formatos=["graphml", "ppm", "txt"]):
        if isinstance(formatos, str):
            formatos = [formatos]
        for formato in formatos:
            self._exportar_formato(nome_base, formato)

    def _exportar_formato(self, nome_base, formato):
        formato = formato.lower()
        if formato == 'graphml':
            nome_arquivo = f"{nome_base}.graphml"
            GraphMLExporter.exportar(self, nome_arquivo)
        elif formato == 'ppm':
            nome_arquivo = f"{nome_base}.ppm"
            PPMExporter.exportar(self, nome_arquivo)
        elif formato == 'txt':
            nome_arquivo = f"{nome_base}.txt"
            TXTExporter.exportar(self, nome_arquivo)
        else:
            raise ValueError(f"Formato de exportação '{formato}' não suportado")

    def exibir_lista_adjacencia(self):
        print("Lista de Adjacência:")
        for vertice, adj in self.lista_adj.adjacencias.items():
            vertice_exibicao = f"{self.vertex_labels[vertice]} (Peso: {self.vertex_weights[vertice]})"
            adj_exibicao = [(f"{self.vertex_labels[v]} (Peso: {self.vertex_weights[v]})", peso) for v, peso in adj]
            print(f"{vertice_exibicao}: {adj_exibicao}")

    def exibir_matriz_adjacencia(self):
        print("Matriz de Adjacência:")
        header = "      " + " ".join([f"{self.vertex_labels[i]:5}" for i in range(self.num_vertices)])
        print(header)
        for i, row in enumerate(self.matriz_adj.adj_matrix):
            linha = f"{self.vertex_labels[i]:5} " + " ".join([f"{val:5}" for val in row])
            print(linha)

    def exibir_matriz_incidencia(self):
        print("Matriz de Incidência:")
        header = "      " + " ".join([f"{edge['label'] or 'A'+str(idx+1):5}" for idx, edge in enumerate(self.edge_list)])
        print(header)
        for i, row in enumerate(self.matriz_inc.inc_matrix):
            linha = f"{self.vertex_labels[i]:5} " + " ".join([f"{val:5}" for val in row])
            print(linha)

    def exibir_representacoes(self):
        self.exibir_lista_adjacencia()
        print()
        self.exibir_matriz_adjacencia()
        print()
        self.exibir_matriz_incidencia()

    def exibir_vertices(self):
        print("Vértices:")
        for v in range(self.num_vertices):
            print(f"{v + 1}. {self.vertex_labels[v]} (Peso: {self.vertex_weights[v]})")

    def exportar_completo(self, nome_base="grafo", formatos=["graphml", "ppm", "txt"]):
        self.exportar(nome_base, formatos)
        print(f"Grafo '{self.nome}' exportado para os formatos {', '.join(formatos).upper()} no diretório 'dados'.")
