from grafo import Grafo
import random

class GeradorGrafos:
    @staticmethod
    def gerar_grafos_prontos():
        grafos = []
        for i in range(1, 9):
            num_vertices = random.randint(10, 20)
            dirigido = random.choice([True, False])
            grafo = Grafo(num_vertices, dirigido, nome=f"Grafo {i}")
            probabilidade_aresta = random.uniform(0.3, 0.7)
            for u in range(num_vertices):
                for v in range(u + 1, num_vertices):
                    if random.random() < probabilidade_aresta:
                        if dirigido:
                            if random.choice([True, False]):
                                grafo.adicionar_aresta(u, v)
                            else:
                                grafo.adicionar_aresta(v, u)
                        else:
                            grafo.adicionar_aresta(u, v)
            grafos.append(grafo)
        return grafos

    @staticmethod
    def gerar_grafo_aleatorio(num_vertices, probabilidade_aresta, dirigido):
        grafo = Grafo(num_vertices, dirigido, nome="Grafo Aleatório")
        for u in range(num_vertices):
            for v in range(u + 1, num_vertices):
                if random.random() < probabilidade_aresta:
                    if dirigido:
                        if random.choice([True, False]):
                            grafo.adicionar_aresta(u, v)
                        else:
                            grafo.adicionar_aresta(v, u)
                    else:
                        grafo.adicionar_aresta(u, v)
        return grafo
