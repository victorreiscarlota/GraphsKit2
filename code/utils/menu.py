from grafo import Grafo
from utils.gerar_grafos import GeradorGrafos
from tests.teste_desempenho import teste_desempenho
from enum import Enum

class MainMenuOption(Enum):
    ANALYZE_GRAPHS = 1
    CREATE_GRAPH = 2
    PERFORMANCE_TEST = 3
    EXIT = 4

class SubMenuOption(Enum):
    ADD_EDGE = 1
    REMOVE_EDGE = 2
    CHECK_ADJACENCY = 3
    SHOW_ADJ_LIST = 4
    SHOW_ADJ_MATRIX = 5
    SHOW_INC_MATRIX = 6
    CHECK_CONNECTIVITY = 7
    IDENTIFY_BRIDGES = 8
    IDENTIFY_ARTICULATIONS = 9
    EXPORT_GRAPH = 10
    EXPORT_PPM = 11
    NEW_NAIVE_BRIDGES = 12
    BACK = 13


class Menu:
    @staticmethod
    def iniciar():
        main_menu_actions = {
            MainMenuOption.ANALYZE_GRAPHS: Menu.analyze_graphs,
            MainMenuOption.CREATE_GRAPH: Menu.create_graph,
            MainMenuOption.PERFORMANCE_TEST: Menu.performance_test,
            MainMenuOption.EXIT: Menu.exit_program
        }

        while True:
            Menu.display_main_menu()
            try:
                opcao = int(input("Escolha uma opção: "))
                option = MainMenuOption(opcao)
                action = main_menu_actions.get(option)
                if action:
                    action()
                else:
                    print("Opção inválida, tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
            except KeyError:
                print("Opção inválida, tente novamente.")

    @staticmethod
    def display_main_menu():
        print("\nEscolha as opções abaixo:")
        print("1. Analisar Grafos Prontos")
        print("2. Criar Grafo Manualmente")
        print("3. Realizar Teste de Desempenho")
        print("4. Sair")
        # for option in MainMenuOption:
        #     print(f"{option.value}. {option.name.replace('_', ' ').title()}")

    @staticmethod
    def analyze_graphs():
        grafos_prontos = GeradorGrafos.gerar_grafos_prontos()
        for grafo in grafos_prontos:
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
            if grafo.dirigido:
                print("Fortemente Conexo:", grafo.grafo_fortemente_conexo())
                print("Conexo Fraco:", grafo.grafo_conexo_fraco())
                print("Semi-fortemente Conexo:", grafo.grafo_semi_fortemente_conexo())
            else:
                print("Conexo:", grafo.grafo_conexo())
            grafo.exportar(f"{grafo.nome.replace(' ', '_')}")
            print(f"Grafo '{grafo.nome}' exportado para os formatos GRAPHML, PPM e TXT no diretório 'dados'.")

    @staticmethod
    def create_graph():
        try:
            num_vertices = int(input("Digite o número de vértices: "))
            if num_vertices <= 0:
                print("O número de vértices deve ser positivo.")
                return
            dirigido = input("O grafo é direcionado? (s/n): ").lower() == 's'
            nome_grafo = input("Digite o nome do grafo: ").strip()
            if not nome_grafo:
                nome_grafo = "Grafo Manual"
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
            return

        grafo = Grafo(num_vertices, dirigido, nome=nome_grafo)

        sub_menu_actions = {
            SubMenuOption.ADD_EDGE: Menu.add_edge,
            SubMenuOption.REMOVE_EDGE: Menu.remove_edge,
            SubMenuOption.CHECK_ADJACENCY: Menu.check_adjacency,
            SubMenuOption.SHOW_ADJ_LIST: Menu.show_adj_list,
            SubMenuOption.SHOW_ADJ_MATRIX: Menu.show_adj_matrix,
            SubMenuOption.SHOW_INC_MATRIX: Menu.show_inc_matrix,
            SubMenuOption.CHECK_CONNECTIVITY: Menu.check_connectivity,
            SubMenuOption.IDENTIFY_BRIDGES: Menu.identify_bridges,
            SubMenuOption.IDENTIFY_ARTICULATIONS: Menu.identify_articulations,
            SubMenuOption.EXPORT_GRAPH: Menu.export_graph,
            SubMenuOption.EXPORT_PPM: Menu.export_ppm,
            SubMenuOption.NEW_NAIVE_BRIDGES: Menu.new_naive_bridges,
            SubMenuOption.BACK: Menu.back_to_main_menu
        }

        while True:
            Menu.display_sub_menu()
            try:
                escolha = int(input("Escolha uma opção: "))
                option = SubMenuOption(escolha)
                action = sub_menu_actions.get(option)
                if action:
                    result = action(grafo)
                    if result == 'back':
                        export_nome = grafo.nome.replace(" ", "_")
                        grafo.exportar(export_nome)
                        print(f"Grafo '{grafo.nome}' exportado automaticamente após a criação.")
                        break
                else:
                    print("Opção inválida, tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, digite números inteiros.")
            except KeyError:
                print("Opção inválida, tente novamente.")

    @staticmethod
    def display_sub_menu():
        print("\nSubmenu:")
        for option in SubMenuOption:
            print(f"{option.value}. {option.name.replace('_', ' ').title()}")

    @staticmethod
    def performance_test():
        teste_desempenho()

    @staticmethod
    def exit_program():
        print("Saindo do programa. Até logo!")
        exit()

    @staticmethod
    def add_edge(grafo):
        try:
            u = int(input(f"Digite o vértice u (1 a {grafo.num_vertices}): ")) - 1
            v = int(input(f"Digite o vértice v (1 a {grafo.num_vertices}): ")) - 1
            if u < 0 or u >= grafo.num_vertices or v < 0 or v >= grafo.num_vertices:
                print(f"Erro: Vértices válidos estão entre 1 e {grafo.num_vertices}.")
                return
            peso_input = input("Digite o peso da aresta (padrão 1): ")
            peso = int(peso_input) if peso_input else 1
            label = input("Digite o rótulo da aresta (opcional): ")
            grafo.adicionar_aresta(u, v, peso, label)
            print(f"Aresta ({u + 1}, {v + 1}) adicionada!")
        except ValueError:
            print("Entrada inválida. Por favor, digite números inteiros.")

    @staticmethod
    def remove_edge(grafo):
        try:
            u = int(input(f"Digite o vértice u (1 a {grafo.num_vertices}): ")) - 1
            v = int(input(f"Digite o vértice v (1 a {grafo.num_vertices}): ")) - 1
            if u < 0 or u >= grafo.num_vertices or v < 0 or v >= grafo.num_vertices:
                print(f"Erro: Vértices válidos estão entre 1 e {grafo.num_vertices}.")
                return
            grafo.remover_aresta(u, v)
            print(f"Aresta ({u + 1}, {v + 1}) removida!")
        except ValueError:
            print("Entrada inválida. Por favor, digite números inteiros.")

    @staticmethod
    def check_adjacency(grafo):
        try:
            u = int(input(f"Digite o vértice u (1 a {grafo.num_vertices}): ")) - 1
            v = int(input(f"Digite o vértice v (1 a {grafo.num_vertices}): ")) - 1
            if u < 0 or u >= grafo.num_vertices or v < 0 or v >= grafo.num_vertices:
                print(f"Erro: Vértices válidos estão entre 1 e {grafo.num_vertices}.")
                return
            if grafo.checar_adjacencia_vertices(u, v):
                print(f"Aresta ({u + 1}, {v + 1}) existe!")
            else:
                print(f"Aresta ({u + 1}, {v + 1}) não existe.")
        except ValueError:
            print("Entrada inválida. Por favor, digite números inteiros.")

    @staticmethod
    def show_adj_list(grafo):
        grafo.exibir_lista_adjacencia()

    @staticmethod
    def show_adj_matrix(grafo):
        grafo.exibir_matriz_adjacencia()

    @staticmethod
    def show_inc_matrix(grafo):
        grafo.exibir_matriz_incidencia()

    @staticmethod
    def check_connectivity(grafo):
        if grafo.dirigido:
            print("Fortemente Conexo:", grafo.grafo_fortemente_conexo())
            print("Conexo Fraco:", grafo.grafo_conexo_fraco())
            print("Semi-fortemente Conexo:", grafo.grafo_semi_fortemente_conexo())
        else:
            print("Conexo:", grafo.grafo_conexo())

    @staticmethod
    def identify_bridges(grafo):
        pontes_naive = grafo.identificar_pontes_naive()
        pontes_tarjan = grafo.identificar_pontes_tarjan()
        pontes_naive_exib = [(u + 1, v + 1) for u, v in pontes_naive]
        pontes_tarjan_exib = [(u + 1, v + 1) for u, v in pontes_tarjan]
        print("Pontes (Naive):", pontes_naive_exib)
        print("Pontes (Tarjan):", pontes_tarjan_exib)

    @staticmethod
    def identify_articulations(grafo):
        articulacoes = [v + 1 for v in grafo.identificar_articulacoes()]
        print("Articulações:", articulacoes)

    @staticmethod
    def export_graph(grafo):
        nome = input("Digite o nome base dos arquivos (sem extensão): ").strip()
        if not nome:
            nome = grafo.nome.replace(" ", "_")
        grafo.exportar(nome)
        print("Exportação concluída.")

    @staticmethod
    def export_ppm(grafo):
        nome_ppm = input("Digite o nome do arquivo PPM (com extensão .ppm): ").strip()
        if not nome_ppm.endswith('.ppm'):
            print("Erro: O nome do arquivo deve terminar com '.ppm'.")
            return
        grafo.exportar(nome_ppm[:-4], ["ppm"])
        print(f"Grafo exportado como {nome_ppm}.")

    @staticmethod
    def new_naive_bridges(grafo):
        pontes_naive = grafo.identificar_pontes_naive_novo()
        pontes_naive_exib = [(u + 1, v + 1) for u, v in pontes_naive]
        print("Pontes (Naive):", pontes_naive_exib)

    @staticmethod
    def back_to_main_menu(grafo):
        return 'back'
