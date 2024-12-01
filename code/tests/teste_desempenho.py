import time
import tracemalloc
import multiprocessing
import sys
import threading
from grafo import Grafo

def worker_naive(grafo, queue):
    pontes_naive = grafo.identificar_pontes_naive()
    queue.put(pontes_naive)

def worker_tarjan(grafo, queue):
    pontes_tarjan = grafo.identificar_pontes_tarjan()
    queue.put(pontes_tarjan)

def mostrar_feedback(processo, metodo):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while processo.is_alive():
        sys.stdout.write(f'\r{spinner[idx % len(spinner)]} Executando {metodo}...')
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write('\r')  # Limpa a linha ao terminar

def teste_desempenho():
    tamanhos = [100, 1000, 10000, 100000]

    for tamanho in tamanhos:
        print(f"\Gerando grafo para teste de tamanho {tamanho}...")

        grafo = gerar_grafo_conectado(tamanho)
        num_arestas = grafo.contar_vertices_arestas()[1]
        print(f"Grafo gerado com {tamanho} vértices e {num_arestas} arestas.")

        # Definir o timeout em segundos
        timeout_seconds = 10  # Ajuste conforme necessário

        # Iniciar o monitoramento de memória
        tracemalloc.start()

        # Teste do método Naive com timeout e feedback
        queue_naive = multiprocessing.Queue()
        p_naive = multiprocessing.Process(target=worker_naive, args=(grafo, queue_naive))
        inicio_naive = time.perf_counter()
        p_naive.start()

        # Iniciar o feedback visual em um thread separado
        feedback_naive = threading.Thread(target=mostrar_feedback, args=(p_naive, 'Método Naive'))
        feedback_naive.start()

        p_naive.join(timeout_seconds)
        if p_naive.is_alive():
            p_naive.terminate()
            p_naive.join()
        feedback_naive.join()

        fim_naive = time.perf_counter()
        tempo_naive = fim_naive - inicio_naive
        memoria_naive = tracemalloc.get_traced_memory()[1] / (1024 * 1024)  # Em MB

        if p_naive.exitcode != 0:
            print(f"Método Naive: Não conseguiu completar em {tempo_naive:.4f} segundos.")
            print(f"Uso de memória (Naive): {memoria_naive:.2f} MB")
            pontes_naive = []
        else:
            pontes_naive = queue_naive.get()
            print(f"Método Naive: {len(pontes_naive)} pontes encontradas em {tempo_naive:.4f} segundos.")
            print(f"Uso de memória (Naive): {memoria_naive:.2f} MB")

        tracemalloc.stop()

        # Reiniciar o monitoramento de memória para o próximo método
        tracemalloc.start()

        # Teste do método Tarjan com timeout e feedback
        queue_tarjan = multiprocessing.Queue()
        p_tarjan = multiprocessing.Process(target=worker_tarjan, args=(grafo, queue_tarjan))
        inicio_tarjan = time.perf_counter()
        p_tarjan.start()

        # Iniciar o feedback visual em um thread separado
        feedback_tarjan = threading.Thread(target=mostrar_feedback, args=(p_tarjan, 'Método Tarjan'))
        feedback_tarjan.start()

        p_tarjan.join(timeout_seconds)
        if p_tarjan.is_alive():
            p_tarjan.terminate()
            p_tarjan.join()
        feedback_tarjan.join()

        fim_tarjan = time.perf_counter()
        tempo_tarjan = fim_tarjan - inicio_tarjan
        memoria_tarjan = tracemalloc.get_traced_memory()[1] / (1024 * 1024)  # Em MB

        if p_tarjan.exitcode != 0:
            print(f"Método Tarjan: Não conseguiu completar em {tempo_tarjan:.4f} segundos.")
            print(f"Uso de memória (Tarjan): {memoria_tarjan:.2f} MB")
            pontes_tarjan = []
        else:
            pontes_tarjan = queue_tarjan.get()
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
