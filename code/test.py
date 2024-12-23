from grafo import Grafo
from utils import GRAPHMLExporter, PPMExporter, TXTExporter

grafo = Grafo(num_vertices=5, dirigido=False, nome="Grafo_Exemplo")

grafo.adicionar_aresta(0, 1)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 0)

grafo.exibir_representacoes()

grafo.exportar("grafo_exemplo")
