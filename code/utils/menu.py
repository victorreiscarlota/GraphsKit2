from grafo import Grafo
from utils.gerar_grafos import GeradorGrafos
from tests.teste_desempenho import teste_desempenho
from enum import Enum


class MainMenuOption(Enum):
    ANALISAR_GRAFOS = 1
    CRIAR_GRAFO = 2
    TESTE_DESEMPENHO = 3
    SAIR = 4


class SubMenuOption(Enum):
    ADICIONAR_ARESTA = 1
    REMOVER_ARESTA = 2
    CHECAR_ADJACENCIA = 3
    EXIBIR_LISTA_ADJ = 4
    EXIBIR_MATRIZ_ADJ = 5
    EXIBIR_MATRIZ_INC = 6
    VERIFICAR_CONECTIVIDADE = 7
    IDENTIFICAR_PONTES = 8
    IDENTIFICAR_ARTICULACOES = 9
    EXPORTAR_GRAFO = 10
    EXPORTAR_PPM = 11
    NOVO_METODO_PONTES = 12
    VOLTAR = 13


class Menu:
    @staticmethod
    def iniciar():
        main_menu_actions = {
            MainMenuOption.ANALISAR_GRAFOS: Menu.analisar_grafos,
            MainMenuOption.CRIAR_GRAFO: Menu.criar_grafo,
            MainMenuOption.TESTE_DESEMPENHO: Menu.teste_desempenho,
            MainMenuOption.SAIR: Menu.sair_programa
        }

        while True:
            Menu.exibir_menu_principal()
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
    def exibir_menu_principal():
        print("\nEscolha uma das opções abaixo:")
        print("1. Analisar Grafos Prontos")
        print("2. Criar Grafo Manualmente")
        print("3. Realizar Teste de Desempenho")
        print("4. Sair")

    @staticmethod
    def analisar_grafos():
        grafos_prontos = GeradorGrafos.gerar_grafos_prontos()
        for grafo in grafos_prontos:
            print(f"\n{grafo.nome}:")
            print(f"O grafo é {'direcionado' if grafo.dirigido else 'não direcionado'}.")
            print(f"Vértices: {grafo.num_vertices}")
            print(f"Arestas: {grafo.contar_vertices_arestas()[1]}")
            pontes_naive = grafo.identificar_pontes_naive()
            pontes_tarjan = grafo.identificar_pontes_tarjan()
            print("Pontes (Método Simples):", [(u + 1, v + 1) for u, v in pontes_naive])
            print("Pontes (Método Tarjan):", [(u + 1, v + 1) for u, v in pontes_tarjan])
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
    def criar_grafo():
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
            SubMenuOption.ADICIONAR_ARESTA: Menu.adicionar_aresta,
            SubMenuOption.REMOVER_ARESTA: Menu.remover_aresta,
            SubMenuOption.CHECAR_ADJACENCIA: Menu.checar_adjacencia,
            SubMenuOption.EXIBIR_LISTA_ADJ: Menu.exibir_lista_adj,
            SubMenuOption.EXIBIR_MATRIZ_ADJ: Menu.exibir_matriz_adj,
            SubMenuOption.EXIBIR_MATRIZ_INC: Menu.exibir_matriz_inc,
            SubMenuOption.VERIFICAR_CONECTIVIDADE: Menu.verificar_conectividade,
            SubMenuOption.IDENTIFICAR_PONTES: Menu.identificar_pontes,
            SubMenuOption.IDENTIFICAR_ARTICULACOES: Menu.identificar_articulacoes,
            SubMenuOption.EXPORTAR_GRAFO: Menu.exportar_grafo,
            SubMenuOption.EXPORTAR_PPM: Menu.exportar_ppm,
            SubMenuOption.NOVO_METODO_PONTES: Menu.novo_metodo_pontes,
            SubMenuOption.VOLTAR: Menu.voltar_menu_principal
        }

        while True:
            Menu.exibir_menu_secundario()
            try:
                escolha = int(input("Escolha uma opção: "))
                option = SubMenuOption(escolha)
                action = sub_menu_actions.get(option)
                if action:
                    result = action(grafo)
                    if result == 'voltar':
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
    def exibir_menu_secundario():
        print("\nSubmenu:")
        print("1. Adicionar Aresta")
        print("2. Remover Aresta")
        print("3. Verificar Adjacência")
        print("4. Exibir Lista de Adjacência")
        print("5. Exibir Matriz de Adjacência")
        print("6. Exibir Matriz de Incidência")
        print("7. Verificar Conectividade")
        print("8. Identificar Pontes")
        print("9. Identificar Articulações")
        print("10. Exportar Grafo")
        print("11. Exportar Grafo como PPM")
        print("12. Identificar Pontes (Método Alternativo)")
        print("13. Voltar ao Menu Principal")

    @staticmethod
    def teste_desempenho():
        teste_desempenho()

    @staticmethod
    def sair_programa():
        print("Saindo do programa. Até logo!")
        exit()

    @staticmethod
    def adicionar_aresta(grafo):
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
    def remover_aresta(grafo):
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
    def checar_adjacencia(grafo):
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
    def exibir_lista_adj(grafo):
        grafo.exibir_lista_adjacencia()

    @staticmethod
    def exibir_matriz_adj(grafo):
        grafo.exibir_matriz_adjacencia()

    @staticmethod
    def exibir_matriz_inc(grafo):
        grafo.exibir_matriz_incidencia()

    @staticmethod
    def verificar_conectividade(grafo):
        if grafo.dirigido:
            print("Fortemente Conexo:", grafo.grafo_fortemente_conexo())
            print("Conexo Fraco:", grafo.grafo_conexo_fraco())
            print("Semi-fortemente Conexo:", grafo.grafo_semi_fortemente_conexo())
        else:
            print("Conexo:", grafo.grafo_conexo())

    @staticmethod
    def identificar_pontes(grafo):
        pontes_naive = grafo.identificar_pontes_naive()
        pontes_tarjan = grafo.identificar_pontes_tarjan()
        pontes_naive_exib = [(u + 1, v + 1) for u, v in pontes_naive]
        pontes_tarjan_exib = [(u + 1, v + 1) for u, v in pontes_tarjan]
        print("Pontes (Método Simples):", pontes_naive_exib)
        print("Pontes (Método Tarjan):", pontes_tarjan_exib)

    @staticmethod
    def identificar_articulacoes(grafo):
        articulacoes = [v + 1 for v in grafo.identificar_articulacoes()]
        print("Articulações:", articulacoes)

    @staticmethod
    def exportar_grafo(grafo):
        nome = input("Digite o nome base dos arquivos (sem extensão): ").strip()
        if not nome:
            nome = grafo.nome.replace(" ", "_")
        grafo.exportar(nome)
        print("Exportação concluída.")

    @staticmethod
    def exportar_ppm(grafo):
        nome_ppm = input("Digite o nome do arquivo PPM (com extensão .ppm): ").strip()
        if not nome_ppm.endswith('.ppm'):
            print("Erro: O nome do arquivo deve terminar com '.ppm'.")
            return
        grafo.exportar(nome_ppm[:-4], ["ppm"])
        print(f"Grafo exportado como {nome_ppm}.")

    @staticmethod
    def novo_metodo_pontes(grafo):
        pontes_naive = grafo.identificar_pontes_naive_novo()
        pontes_naive_exib = [(u + 1, v + 1) for u, v in pontes_naive]
        print("Pontes (Método Alternativo):", pontes_naive_exib)

    @staticmethod
    def voltar_menu_principal(grafo):
        return 'voltar'
