import os
from utils.desenhador import Desenhador

class PPMExporter:
    @staticmethod
    def exportar(grafo, nome_arquivo="grafo.ppm"):
        dados_dir = "dados"
        if not os.path.exists(dados_dir):
            os.makedirs(dados_dir)
        largura = 800
        altura = 800
        raio_vertice = 20
        num_cols = int(grafo.num_vertices ** 0.5) + 1
        num_rows = (grafo.num_vertices // num_cols) + 1
        espacamento_x = largura // (num_cols + 1)
        espacamento_y = altura // (num_rows + 1)
        posicoes = {}
        idx = 0
        for row in range(1, num_rows + 1):
            for col in range(1, num_cols + 1):
                if idx < grafo.num_vertices:
                    x = col * espacamento_x
                    y = row * espacamento_y
                    posicoes[idx] = (x, y)
                    idx += 1
        caminho_frames = os.path.join(dados_dir, "imagens_ppm")
        if not os.path.exists(caminho_frames):
            os.makedirs(caminho_frames)
        imagem_base = [[(255, 255, 255) for _ in range(largura)] for _ in range(altura)]
        for i in range(grafo.num_vertices):
            x, y = posicoes[i]
            Desenhador.desenhar_circulo(imagem_base, x, y, raio_vertice, (0, 0, 255))
        for idx in range(len(grafo.edge_list)):
            imagem = [row.copy() for row in imagem_base]
            for edge in grafo.edge_list[:idx+1]:
                u = edge['u']
                v = edge['v']
                x1, y1 = posicoes[u]
                x2, y2 = posicoes[v]
                if grafo.dirigido:
                    Desenhador.desenhar_seta(imagem, x1, y1, x2, y2, (0, 0, 0))
                else:
                    Desenhador.desenhar_linha_basica(imagem, x1, y1, x2, y2, (0, 0, 0))
            frame_nome = f"frame_{grafo.frame_count}.ppm"
            PPMExporter.salvar_imagem_ppm(imagem, os.path.join(caminho_frames, frame_nome))
            grafo.frame_count += 1
        imagem_final = [row.copy() for row in imagem_base]
        for edge in grafo.edge_list:
            u = edge['u']
            v = edge['v']
            x1, y1 = posicoes[u]
            x2, y2 = posicoes[v]
            if grafo.dirigido:
                Desenhador.desenhar_seta(imagem_final, x1, y1, x2, y2, (0, 0, 0))
            else:
                Desenhador.desenhar_linha_basica(imagem_final, x1, y1, x2, y2, (0, 0, 0))
        PPMExporter.salvar_imagem_ppm(imagem_final, os.path.join(dados_dir, nome_arquivo))
        print(f"Imagem PPM exportada como {os.path.join(dados_dir, nome_arquivo)}")

    @staticmethod
    def salvar_imagem_ppm(imagem, nome_arquivo):
        with open(nome_arquivo, "wb") as f:
            f.write(b"P6\n")
            f.write(f"{len(imagem[0])} {len(imagem)}\n".encode())
            f.write(b"255\n")
            for row in imagem:
                for pixel in row:
                    f.write(bytes(pixel))
