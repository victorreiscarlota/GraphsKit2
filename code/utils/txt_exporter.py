import os

class TXTExporter:
    @staticmethod
    def exportar(grafo, nome_arquivo="grafo.txt"):
        dados_dir = "dados"
        if not os.path.exists(dados_dir):
            os.makedirs(dados_dir)
        with open(os.path.join(dados_dir, nome_arquivo), 'w', encoding='utf-8') as f:
            f.write(f"Grafo: {grafo.nome}\n")
            f.write(f"Direcionado: {'Sim' if grafo.dirigido else 'Não'}\n")
            f.write(f"Vértices: {grafo.num_vertices}\n")
            f.write(f"Arestas: {len(grafo.edge_list)}\n\n")

            f.write("Lista de Adjacência:\n")
            for vertice, adj in grafo.lista_adj.adjacencias.items():
                vertice_exibicao = vertice + 1
                adj_exibicao = ", ".join([f"{v + 1}({peso})" for v, peso in adj])
                f.write(f"{vertice_exibicao}: {adj_exibicao}\n")

            f.write("\nMatriz de Adjacência:\n")
            header = "   " + " ".join([f"{i+1:3}" for i in range(grafo.num_vertices)])
            f.write(header + "\n")
            for i, row in enumerate(grafo.matriz_adj.adj_matrix):
                linha = f"{i+1:3} " + " ".join([f"{val:3}" for val in row])
                f.write(linha + "\n")

            f.write("\nMatriz de Incidência:\n")
            if grafo.edge_list:
                header = "   " + " ".join([f"{i+1:3}" for i in range(len(grafo.edge_list))])
                f.write(header + "\n")
                for i, row in enumerate(grafo.matriz_inc.inc_matrix):
                    linha = f"{i+1:3} " + " ".join([f"{val:3}" for val in row])
                    f.write(linha + "\n")
            else:
                f.write("Sem arestas.\n")
