class Desenhador:
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
