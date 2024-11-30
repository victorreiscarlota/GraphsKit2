import os

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
            PPMExporter.desenhar_circulo(imagem_base, x, y, raio_vertice, (0, 0, 255))
        
        for idx in range(len(grafo.edge_list)):
            imagem = [row.copy() for row in imagem_base]
            for edge in grafo.edge_list[:idx+1]:
                u = edge['u']
                v = edge['v']
                x1, y1 = posicoes[u]
                x2, y2 = posicoes[v]
                PPMExporter.desenhar_linha(imagem, x1, y1, x2, y2, (0, 0, 0))
            frame_nome = f"frame_{grafo.frame_count}.ppm"
            PPMExporter.salvar_imagem_ppm(imagem, os.path.join(caminho_frames, frame_nome))
            grafo.frame_count += 1

        imagem_final = [row.copy() for row in imagem_base]
        for edge in grafo.edge_list:
            u = edge['u']
            v = edge['v']
            x1, y1 = posicoes[u]
            x2, y2 = posicoes[v]
            PPMExporter.desenhar_linha(imagem_final, x1, y1, x2, y2, (0, 0, 0))
        PPMExporter.salvar_imagem_ppm(imagem_final, os.path.join(dados_dir, nome_arquivo))
        print(f"Imagem PPM exportada como {os.path.join(dados_dir, nome_arquivo)}")

    @staticmethod
    def desenhar_linha(imagem, x1, y1, x2, y2, cor):
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        if x2 > x1:
            sx = 1
        else:
            sx = -1
        if y2 > y1:
            sy = 1
        else:
            sy = -1
        if dx > dy:
            err = dx // 2
            while x != x2:
                if 0 <= x < len(imagem[0]) and 0 <= y < len(imagem):
                    imagem[y][x] = cor
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy // 2
            while y != y2:
                if 0 <= x < len(imagem[0]) and 0 <= y < len(imagem):
                    imagem[y][x] = cor
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        if 0 <= x2 < len(imagem[0]) and 0 <= y2 < len(imagem):
            imagem[y2][x2] = cor

    @staticmethod
    def desenhar_circulo(imagem, x0, y0, raio, cor):
        x0 = int(x0)
        y0 = int(y0)
        for y in range(y0 - raio, y0 + raio + 1):
            for x in range(x0 - raio, x0 + raio + 1):
                if 0 <= x < len(imagem[0]) and 0 <= y < len(imagem):
                    if (x - x0) ** 2 + (y - y0) ** 2 <= raio ** 2:
                        imagem[y][x] = cor

    @staticmethod
    def salvar_imagem_ppm(imagem, nome_arquivo):
        with open(nome_arquivo, "wb") as f:
            f.write(b"P6\n")
            f.write(f"{len(imagem[0])} {len(imagem)}\n".encode())
            f.write(b"255\n")
            for row in imagem:
                for pixel in row:
                    f.write(bytes(pixel))
