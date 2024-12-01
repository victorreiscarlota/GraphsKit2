import os

class GraphMLExporter:
    @staticmethod
    def exportar(grafo, nome_arquivo="grafo.graphml"):
        dados_dir = "dados"
        if not os.path.exists(dados_dir):
            os.makedirs(dados_dir)
        with open(os.path.join(dados_dir, nome_arquivo), "w", encoding="utf-8") as arquivo:
            arquivo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            arquivo.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"\n')
            arquivo.write('         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
            arquivo.write('         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns\n')
            arquivo.write('         http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
            

            arquivo.write('    <key id="d0" for="node" attr.name="label" attr.type="string"/>\n')
            arquivo.write('    <key id="d1" for="edge" attr.name="weight" attr.type="double"/>\n')
            arquivo.write('    <key id="d2" for="edge" attr.name="label" attr.type="string"/>\n')
            
            arquivo.write('  <graph id="G" edgedefault="{}">\n'.format("directed" if grafo.dirigido else "undirected"))

            for vertice in range(grafo.num_vertices):
                label = grafo.vertex_labels.get(vertice, f"V{vertice + 1}")
                arquivo.write(f'    <node id="{vertice}">\n')
                arquivo.write(f'      <data key="d0">{label}</data>\n')
                arquivo.write('    </node>\n')
            

            for i, edge in enumerate(grafo.edge_list):
                u = edge['u']
                v = edge['v']
                peso = edge['peso']
                label = edge['label'] if edge['label'] else ""
                arquivo.write(f'    <edge id="{i}" source="{u}" target="{v}">\n')
                arquivo.write(f'      <data key="d1">{peso}</data>\n')
                arquivo.write(f'      <data key="d2">{label}</data>\n')
                arquivo.write('    </edge>\n')
            
            arquivo.write('  </graph>\n')
            arquivo.write('</graphml>\n')

