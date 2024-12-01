import os

class GEXFExporter:
    @staticmethod
    def exportar(grafo, nome_arquivo="grafo.gexf"):
        dados_dir = "dados"
        if not os.path.exists(dados_dir):
            os.makedirs(dados_dir)
        with open(os.path.join(dados_dir, nome_arquivo), "w", encoding="utf-8") as arquivo:
            arquivo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            arquivo.write('<gexf xmlns="http://www.gexf.net/1.3draft" xmlns:viz="http://www.gephi.org/gexf/viz/0.1" version="1.3">\n')
            arquivo.write('  <graph mode="static" defaultedgetype="{}">\n'.format("directed" if grafo.dirigido else "undirected"))
            arquivo.write("    <nodes>\n")
            for vertice in range(grafo.num_vertices):
                label = grafo.vertex_labels.get(vertice, f"V{vertice + 1}")
                # Adicionando atributos de posição (opcional)
                arquivo.write(f'      <node id="{vertice}" label="{label}">\n')
                arquivo.write('        <viz:position x="0" y="0" z="0" />\n')  # Posições default, pode ser ajustado
                arquivo.write('      </node>\n')
            arquivo.write("    </nodes>\n")
            arquivo.write("    <edges>\n")
            for i, edge in enumerate(grafo.edge_list):
                u = edge['u']
                v = edge['v']
                peso = edge['peso']
                label = edge['label'] if edge['label'] else ""
                arquivo.write(f'      <edge id="{i}" source="{u}" target="{v}" weight="{peso}" label="{label}" />\n')
            arquivo.write("    </edges>\n")
            arquivo.write("  </graph>\n")
            arquivo.write("</gexf>\n")
