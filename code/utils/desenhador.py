import math

class Desenhador:
    @staticmethod
    def desenhar_linha_basica(imagem, x1, y1, x2, y2, cor):
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        sx = 1 if x2 > x1 else -1
        sy = 1 if y2 > y1 else -1
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
    def desenhar_seta(imagem, x1, y1, x2, y2, cor):
        Desenhador.desenhar_linha_basica(imagem, x1, y1, x2, y2, cor)
        Desenhador.desenhar_cabeca_seta(imagem, x1, y1, x2, y2, cor)

    @staticmethod
    def desenhar_cabeca_seta(imagem, x1, y1, x2, y2, cor):
        angulo = math.atan2(y2 - y1, x2 - x1)
        tamanho_seta = 10
        angulo1 = angulo + math.pi / 6
        angulo2 = angulo - math.pi / 6
        x3 = int(x2 - tamanho_seta * math.cos(angulo1))
        y3 = int(y2 - tamanho_seta * math.sin(angulo1))
        x4 = int(x2 - tamanho_seta * math.cos(angulo2))
        y4 = int(y2 - tamanho_seta * math.sin(angulo2))
        Desenhador.desenhar_linha_basica(imagem, x2, y2, x3, y3, cor)
        Desenhador.desenhar_linha_basica(imagem, x2, y2, x4, y4, cor)

    @staticmethod
    def desenhar_circulo(imagem, x0, y0, raio, cor):
        x0 = int(x0)
        y0 = int(y0)
        for y in range(y0 - raio, y0 + raio + 1):
            for x in range(x0 - raio, x0 + raio + 1):
                if 0 <= x < len(imagem[0]) and 0 <= y < len(imagem):
                    if (x - x0) ** 2 + (y - y0) ** 2 <= raio ** 2:
                        imagem[y][x] = cor
