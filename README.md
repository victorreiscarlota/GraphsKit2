# GraphsKit - Manipulação de grafos

> Trabalho prático da disciplina Teoria dos Grafos e Computabilidade, PUC Minas, 2024.

GraphsKit é uma biblioteca em Python desenvolvida para facilitar a criação, manipulação e visualização de grafos. Ela foi implementada sem o uso de bibliotecas externas e oferece funcionalidades como:

- **Criação de grafos** dirigidos e não dirigidos.
- **Adição e remoção de vértices e arestas**.
- **Visualização de diferentes representações** de grafos (lista de adjacência, matriz de adjacência e matriz de incidência).
- **Exportação de grafos** nos formatos GRAPHML, PPM e TXT.
- **Análise de propriedades** do grafo, como conectividade, existência de pontes e articulações, e verificação de caminhos Eulerianos.

## 👨‍🏫 Professor

- Leonardo Vilela Cardoso

## 🧑‍🎓 Integrantes

- Gustavo Pereira de Oliveira
- Luís Felipe Teixeira Dias Brescia
- Luiz Felipe Campos de Morais
- Marcus Vinícius Carvalho de Oliveira
- Victor Reis Carlota

## 📂 Estrutura de diretórios

- `dados/`: Contém os arquivos de dados utilizados no trabalho.
- `models/`: Contém os arquivos de modelos utilizados no trabalho.
- `tests/`: Contém os arquivos de testes utilizados no trabalho.
- `utils/`: Contém os arquivos de utilidades utilizados no trabalho.

<!-- ## 📽️ Demonstração

![DESC](docs/grafo.gif) -->

## ⌨️ Guia de uso

1. Navegue até o diretório `code`.
2. Execute o arquivo principal:

```bash python
python main.py
```

ou

```bash
python3 main.py
```

3. Para poder importar a nossa biblioteca

```bash
pip install -e GraphsKit/
```

## 📚 Documentação

A classe `Grafo` é a classe principal da biblioteca e encapsula as diversas representações e operações sobre grafos.

### **Atributos**

- `num_vertices` (_int_): Número de vértices no grafo.
- `dirigido` (_bool_): Indica se o grafo é dirigido (`True`) ou não dirigido (`False`).
- `nome` (_str_): Nome do grafo.
- `lista_adj` (_ListaAdjacencia_): Representação do grafo como lista de adjacência.
- `matriz_adj` (_MatrizAdjacencia_): Representação do grafo como matriz de adjacência.
- `matriz_inc` (_MatrizIncidencia_): Representação do grafo como matriz de incidência.
- `edge_list` (_list_): Lista de arestas, onde cada aresta é um dicionário com os vértices e peso.
- `vertex_labels` (_dict_): Dicionário que mapeia cada vértice ao seu rótulo.
- `desenhador` (_Desenhador_): Instância usada para desenhar o grafo.

### **Métodos**

**Inicialização**

```python
grafo = Grafo(dirigido=False, nome='Grafo')
```

- `dirigido` (_bool_, opcional): Indica se o grafo é dirigido ou não dirigido. Padrão: `False`.
- `nome` (_str_, opcional): Nome do grafo. Padrão: `'Grafo'`.

**Adição e Remoção de Vértices e Arestas**

```python
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_aresta(1, 2, peso=3)
grafo.remover_vertice(1)
grafo.remover_aresta(2, 1)
```

- `adicionar_vertice(v: int, label: str = None)`: Adiciona um vértice ao grafo.
- `adicionar_aresta(u: int, v: int, peso: float = 1.0)`: Adiciona uma aresta ao grafo.
- `remover_vertice(v: int)`: Remove um vértice do grafo.
- `remover_aresta(u: int, v: int)`: Remove uma aresta do grafo.

**Visualização**

```python
grafo.visualizar_lista_adjacencia()
grafo.visualizar_matriz_adjacencia()
grafo.visualizar_matriz_incidencia()
```

- `visualizar_lista_adjacencia()`: Exibe a lista de adjacência do grafo.
- `visualizar_matriz_adjacencia()`: Exibe a matriz de adjacência do grafo.
- `visualizar_matriz_incidencia()`: Exibe a matriz de incidência do grafo.

**Exportação**

```python
grafo.exportar_graphml('grafo', ["graphml", "txt"])
```

- `exportar_graphml(nome_base: str = 'grafo', tipos: List[str] = ['graphml', 'ppm', 'txt'])`: Exporta o grafo para os formatos especificados.

- `nome_base` (_string, opcional_): Nome base do arquivo de saída. Padrão: `'grafo'`.
- `tipos` (_list, opcional_): Lista de tipos de arquivo para exportar. Padrão: `['graphml', 'ppm', 'txt']`.

## 📌 Conclusão

A biblioteca GraphsKit oferece uma base sólida para a manipulação de grafos em Python, especialmente para fins educacionais. Com as melhorias sugeridas e uma documentação completa, ela pode se tornar uma ferramenta ainda mais poderosa e útil para estudantes e entusiastas de teoria dos grafos.

Se tiver mais dúvidas ou precisar de assistência adicional, estou à disposição para ajudar!
