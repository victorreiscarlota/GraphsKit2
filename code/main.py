from grafo import Grafo
from tests.teste_desempenho import teste_desempenho

def menu():
    grafos_prontos = {
        "1": {
            'arestas': [(0, 1), (1, 2), (2, 3), (3, 0)],
            'dirigido': False
        },
        "2": {
            'arestas': [(0, 1), (1, 2), (2, 3), (3, 0), (3, 1)],
            'dirigido': False
        },
        "3": {
            'arestas': [(0, 1), (1, 2), (2, 0)],
            'dirigido': True
        },
        "4": {
            'arestas': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
            'dirigido': False
        },
        "5": {
            'arestas': [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)],
            'dirigido': True
        },
        "6": {
            'arestas': [(0, 1), (1, 2), (2, 3)],
            'dirigido': False
        },
        "7": {
            'arestas': [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 3)],
            'dirigido': True
        },
    }
    while True:
        print("\nEscolha as opções abaixo:")
        print("1. Analisar Grafos Prontos")
        print("2. Criar Grafo Manualmente")
        print("3. Realizar Teste de Desempenho (Parte 2)")
        print("4. Sair")
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
            continue
        if opcao == 1:
            for nome, info in grafos_prontos.items():
                arestas = info['arestas']
                dirigido = info['dirigido']
                num_vertices = max(max(u, v) for u, v in arestas) + 1
                grafo_nome = f"Grafo_{nome}"
                grafo = Grafo(num_vertices, dirigido, nome=grafo_nome)
                for u, v in arestas:
                    grafo.adicionar_aresta(u, v)
                print(f"\n{grafo.nome}:")
                print(f"O grafo é {'direcionado' if grafo.dirigido else 'não direcionado'}.")
                print(f"Vértices: {grafo.num_vertices}")
                print(f"Arestas: {grafo.contar_vertices_arestas()[1]}")
                pontes_naive = grafo.identificar_pontes_naive()
                pontes_tarjan = grafo.identificar_pontes_tarjan()
                print("Pontes (Naive):", [(u + 1, v + 1) for u, v in pontes_naive])
                print("Pontes (Tarjan):", [(u + 1, v + 1) for u, v in pontes_tarjan])
                articulacoes = grafo.identificar_articulacoes()
                print("Articulações:", [v + 1 for v in articulacoes])
                if dirigido:
                    print("Fortemente Conexo:", grafo.grafo_fortemente_conexo())
                    print("Conexo Fraco:", grafo.grafo_conexo_fraco())
                    print("Semi-fortemente Conexo:", grafo.grafo_semi_fortemente_conexo())
                else:
                    print("Conexo:", grafo.grafo_conexo())
                grafo.exportar_para_gexf(f"{grafo.nome}.gexf")
                grafo.exportar_para_ppm(f"{grafo.nome}.ppm")
                grafo.exportar_para_txt(f"{grafo.nome}.txt")
                print(f"Grafo '{grafo.nome}' exportado para os formatos GEXF, PPM e TXT no diretório 'dados'.")
        elif opcao == 2:
            try:
                num_vertices = int(input("Digite o número de vértices: "))
                if num_vertices <= 0:
                    print("O número de vértices deve ser positivo.")
                    continue
                dirigido = input("O grafo é direcionado? (s/n): ").lower() == 's'
                nome_grafo = input("Digite o nome do grafo: ").strip()
                if not nome_grafo:
                    nome_grafo = "Grafo_Manual"
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
                continue
            grafo = Grafo(num_vertices, dirigido, nome=nome_grafo)
            while True:
                print("\n1. Adicionar Aresta")
                print("2. Remover Aresta")
                print("3. Verificar Adjacência")
                print("4. Exibir Lista de Adjacência")
                print("5. Exibir Matriz de Adjacência")
                print("6. Exibir Matriz de Incidência")
                print("7. Verificar Conectividade")
                print("8. Identificar Pontes")
                print("9. Identificar Articulações")
                print("10. Exportar Grafo")
                print("11. Exportar para PPM")
                print("12. Voltar")
                try:
                    escolha = int(input("Escolha uma opção: "))
                except ValueError:
                    print("Entrada inválida. Por favor, digite números inteiros.")
                    continue
                if escolha == 1:
                    try:
                        u = int(input(f"Digite o vértice u (1 a {grafo.num_vertices}): ")) - 1
                        v = int(input(f"Digite o vértice v (1 a {grafo.num_vertices}): ")) - 1
                        if u < 0 or u >= grafo.num_vertices or v < 0 or v >= grafo.num_vertices:
                            print(f"Erro: Vértices válidos estão entre 1 e {grafo.num_vertices}.")
                            continue
                        peso_input = input("Digite o peso da aresta (padrão 1): ")
                        peso = int(peso_input) if peso_input else 1
                        label = input("Digite o rótulo da aresta (opcional): ")
                        grafo.adicionar_aresta(u, v, peso, label)
                        print(f"Aresta ({u + 1}, {v + 1}) adicionada!")
                    except ValueError:
                        print("Entrada inválida. Por favor, digite números inteiros.")
                elif escolha == 2:
                    try:
                        u = int(input(f"Digite o vértice u (1 a {grafo.num_vertices}): ")) - 1
                        v = int(input(f"Digite o vértice v (1 a {grafo.num_vertices}): ")) - 1
                        if u < 0 or u >= grafo.num_vertices or v < 0 or v >= grafo.num_vertices:
                            print(f"Erro: Vértices válidos estão entre 1 e {grafo.num_vertices}.")
                            continue
                        grafo.remover_aresta(u, v)
                        print(f"Aresta ({u + 1}, {v + 1}) removida!")
                    except ValueError:
                        print("Entrada inválida. Por favor, digite números inteiros.")
                elif escolha == 3:
                    try:
                        u = int(input(f"Digite o vértice u (1 a {grafo.num_vertices}): ")) - 1
                        v = int(input(f"Digite o vértice v (1 a {grafo.num_vertices}): ")) - 1
                        if u < 0 or u >= grafo.num_vertices or v < 0 or v >= grafo.num_vertices:
                            print(f"Erro: Vértices válidos estão entre 1 e {grafo.num_vertices}.")
                            continue
                        if grafo.checar_adjacencia_vertices(u, v):
                            print(f"Aresta ({u + 1}, {v + 1}) existe!")
                        else:
                            print(f"Aresta ({u + 1}, {v + 1}) não existe.")
                    except ValueError:
                        print("Entrada inválida. Por favor, digite números inteiros.")
                elif escolha == 4:
                    grafo.exibir_lista_adjacencia()
                elif escolha == 5:
                    grafo.exibir_matriz_adjacencia()
                elif escolha == 6:
                    grafo.exibir_matriz_incidencia()
                elif escolha == 7:
                    if grafo.dirigido:
                        print("Fortemente Conexo:", grafo.grafo_fortemente_conexo())
                        print("Conexo Fraco:", grafo.grafo_conexo_fraco())
                        print("Semi-fortemente Conexo:", grafo.grafo_semi_fortemente_conexo())
                    else:
                        print("Conexo:", grafo.grafo_conexo())
                elif escolha == 8:
                    pontes_naive = grafo.identificar_pontes_naive()
                    pontes_tarjan = grafo.identificar_pontes_tarjan()
                    pontes_naive_exib = [(u + 1, v + 1) for u, v in pontes_naive]
                    pontes_tarjan_exib = [(u + 1, v + 1) for u, v in pontes_tarjan]
                    print("Pontes (Naive):", pontes_naive_exib)
                    print("Pontes (Tarjan):", pontes_tarjan_exib)
                elif escolha == 9:
                    articulacoes = [v + 1 for v in grafo.identificar_articulacoes()]
                    print("Articulações:", articulacoes)
                elif escolha == 10:
                    nome = input("Digite o nome base dos arquivos (sem extensão): ").strip()
                    if not nome:
                        nome = grafo.nome.replace(" ", "_")
                    grafo.exportar_para_gexf(f"{nome}.gexf")
                    grafo.exportar_para_ppm(f"{nome}.ppm")
                    grafo.exportar_para_txt(f"{nome}.txt")
                    print("Exportação concluída.")
                elif escolha == 11:
                    nome_ppm = input("Digite o nome do arquivo PPM (com extensão .ppm): ").strip()
                    if not nome_ppm.endswith('.ppm'):
                        print("Erro: O nome do arquivo deve terminar com '.ppm'.")
                        continue
                    grafo.exportar_para_ppm(nome_ppm)
                elif escolha == 12:
                    export_nome = grafo.nome.replace(" ", "_")
                    grafo.exportar_para_gexf(f"{export_nome}.gexf")
                    grafo.exportar_para_ppm(f"{export_nome}.ppm")
                    grafo.exportar_para_txt(f"{export_nome}.txt")
                    print(f"Grafo '{grafo.nome}' exportado automaticamente após a criação.")
                    break
                else:
                    print("Opção inválida, tente novamente.")
        elif opcao == 3:
            teste_desempenho()
        elif opcao == 4:
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()
