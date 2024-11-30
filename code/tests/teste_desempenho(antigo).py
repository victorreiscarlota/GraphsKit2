import time
from grafo import Grafo

def teste_desempenho():
    tamanhos = [100, 1000, 10000, 100000]
    for tamanho in tamanhos:
        grafo = Grafo(tamanho)
        num_componentes = 5
        tamanho_componente = tamanho // num_componentes
        vertices_componentes = []

        for i in range(num_componentes):
            vertices = list(range(i * tamanho_componente, (i + 1) * tamanho_componente))
            vertices_componentes.append(vertices)
            for j in range(len(vertices)):
                u = vertices[j]
                v = vertices[(j + 1) % len(vertices)]
                grafo.adicionar_aresta(u, v)

        for i in range(num_componentes - 1):
            u = vertices_componentes[i][-1]
            v = vertices_componentes[i + 1][0]
            grafo.adicionar_aresta(u, v)

        print(f"\nTeste para {tamanho} vértices e {grafo.contar_vertices_arestas()[1]} arestas:")
        inicio_naive = time.time()
        pontes_naive = grafo.identificar_pontes_naive()
        fim_naive = time.time()
        tempo_naive = fim_naive - inicio_naive
        print(f"Método Naive: {len(pontes_naive)} pontes encontradas em {tempo_naive:.4f} segundos.")
        inicio_tarjan = time.time()
        pontes_tarjan = grafo.identificar_pontes_tarjan()
        fim_tarjan = time.time()
        tempo_tarjan = fim_tarjan - inicio_tarjan
        print(f"Método Tarjan: {len(pontes_tarjan)} pontes encontradas em {tempo_tarjan:.4f} segundos.")
