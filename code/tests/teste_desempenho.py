import time
from grafo import Grafo
import tracemalloc

def teste_desempenho():
    tamanhos = [100, 1000, 10000, 100000]

    for tamanho in tamanhos:
        print(f"\nIniciando teste para tamanho {tamanho}...")

        grafo = gerar_grafo_conectado(tamanho)
        num_arestas = grafo.contar_vertices_arestas()[1]
        print(f"Grafo gerado com {tamanho} vértices e {num_arestas} arestas.")

        # Iniciar o monitoramento de memória (opcional)
        tracemalloc.start()

        # Teste do método Naive
        inicio_naive = time.perf_counter()
        pontes_naive = grafo.identificar_pontes_naive()
        fim_naive = time.perf_counter()
        tempo_naive = fim_naive - inicio_naive
        memoria_naive = tracemalloc.get_traced_memory()[1] / (1024 * 1024)  # Em MB
        print(f"Método Naive: {len(pontes_naive)} pontes encontradas em {tempo_naive:.4f} segundos.")
        print(f"Uso de memória (Naive): {memoria_naive:.2f} MB")

        tracemalloc.stop()
        tracemalloc.start()

        # Teste do método Tarjan
        inicio_tarjan = time.perf_counter()
        pontes_tarjan = grafo.identificar_pontes_tarjan()
        fim_tarjan = time.perf_counter()
        tempo_tarjan = fim_tarjan - inicio_tarjan
        memoria_tarjan = tracemalloc.get_traced_memory()[1] / (1024 * 1024)  # Em MB
        print(f"Método Tarjan: {len(pontes_tarjan)} pontes encontradas em {tempo_tarjan:.4f} segundos.")
        print(f"Uso de memória (Tarjan): {memoria_tarjan:.2f} MB")

        tracemalloc.stop()

def gerar_grafo_conectado(tamanho):
    """
    Gera um grafo conectado com um determinado número de vértices.
    O grafo consiste em vários componentes cíclicos conectados por pontes.
    """
    grafo = Grafo(tamanho)
    num_componentes = 5
    tamanho_componente = tamanho // num_componentes
    vertices_componentes = []

    # Gerar componentes cíclicos
    for i in range(num_componentes):
        inicio = i * tamanho_componente
        fim = (i + 1) * tamanho_componente if i != num_componentes - 1 else tamanho
        vertices = list(range(inicio, fim))
        vertices_componentes.append(vertices)
        conectar_vertices_em_ciclo(grafo, vertices)

    # Conectar componentes com pontes
    conectar_componentes_com_pontes(grafo, vertices_componentes)

    return grafo

def conectar_vertices_em_ciclo(grafo, vertices):
    """
    Conecta uma lista de vértices em um ciclo.
    """
    num_vertices = len(vertices)
    for i in range(num_vertices):
        u = vertices[i]
        v = vertices[(i + 1) % num_vertices]
        grafo.adicionar_aresta(u, v)

def conectar_componentes_com_pontes(grafo, vertices_componentes):
    """
    Conecta componentes entre si com pontes.
    """
    num_componentes = len(vertices_componentes)
    for i in range(num_componentes - 1):
        u = vertices_componentes[i][-1]
        v = vertices_componentes[i + 1][0]
        grafo.adicionar_aresta(u, v)  # Esta aresta é uma ponte

if __name__ == "__main__":
    teste_desempenho()
