from Sistema import Grafo
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple
import math


class Sistema:
    def __init__(self):
        self.graph = Grafo.Graph()

    def __str__(self) -> str:
        return str(self.graph)

    def __len__(self) -> int:
        """

        :return: Retorna o numero de vertices do grafo.
        """
        return len(self.graph)

    def add_ponto_interresse(self, vertex: str) -> str:
        """
        Adiciona um vértice ao gráfico.
        :param vertex: Nome do vértice
        :return: Retorna uma mensagem de status indicando sucesso
        """
        self.graph.add_vertex(vertex)
        return "Vértice adicionado com sucesso."

    def add_rua(self, from_vertex: str, to_vertex: str, distance: float, min_speed: int,
                max_speed: int, orientation: int) -> str:
        """
        Adiciona uma aresta ao grafo
        :param from_vertex: Nome do primeiro vértice
        :param to_vertex: Nome do segundo vértice
        :param distance: Distancia entre os dois vertices
        :param min_speed: Velocidade minima da via
        :param max_speed: Velocidade maxima da via
        :param orientation: Se a via é de mão dupla então = 2
        :return: Retorna uma mensagem de status indicando sucesso
        """

        return self.graph.add_edge(from_vertex, to_vertex, distance, min_speed, max_speed, orientation)

    def remove_ponto_interresse(self, vertex: str) -> str:
        """

        :param vertex: Remove um vértice do grafo
        :return: Retorna uma mensagem de status indicando sucesso
        """
        return self.graph.remove_vertex(vertex)

    def remove_rua(self, from_vertex: str, to_vertex: str) -> str:
        """
        Removes an edge from the graph.
        Returns a status message indicating success or failure.
        """
        return self.graph.remove_edge(from_vertex, to_vertex)

    def internal_degree_centrality(self):
        return self.graph.internal_degree_centrality()

    def external_degree_centrality(self):
        return self.graph.external_degree_centrality()

    def closeness_centrality(self):
        return self.graph.closeness_centrality()

    def get_pontos_interresse(self) -> set:
        """

        :return: Os Pontos de interesse do grafo
        """
        return self.graph.get_vertices()

    def get_ruas(self) -> list:
        """

        :return: As arestas de interesse do grafo
        """
        return self.graph.get_edges()

    def save_to_json(self, filename: str) -> None:
        """
        Grava num ficheiro JSON.
        :param filename: Nome do ficheiro
        :return: None
        """
        # Converter as chaves de tuplos para strings
        edges = {str(key): value for key, value in self.graph.edges.items()}
        mapa = {str(key): value for key, value in self.graph.map.items()}

        data = {
            "vertices": list(self.graph.vertices.keys()),
            "edges": edges,
            "mapa": mapa
        }
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_from_json(self, filename: str):
        """
        Carrega um ficheiro JSON.
        :param filename: Nome do ficheiro
        :return: Retorna uma mensagem de status indicando sucesso e um tuplo com os parâmetros
        """
        if os.path.getsize(filename) == 0:
            return "O arquivo JSON está vazio."

        with open(filename, "r") as file:
            try:
                data = json.load(file)
                self.graph.clear()
                for vertex in data["vertices"]:
                    self.graph.add_vertex(vertex)
                for edge_key, edge_value in data["edges"].items():
                    from_vertex, to_vertex = eval(edge_key)
                    distance = edge_value["distance"]
                    min_speed = edge_value["min_speed"]
                    max_speed = edge_value["max_speed"]
                    orientation = edge_value.get(
                        "orientation")
                    self.graph.add_edge(
                        from_vertex, to_vertex, distance, min_speed, max_speed, orientation)
            except json.JSONDecodeError as e:
                return "O arquivo JSON contém dados inválidos:", e

    def mapa_city(self) -> None:
        """
        Desenha o grafo usando o nx
        :return: None
        """
        g = nx.DiGraph()

        for vertex in self.graph.vertices:
            g.add_node(vertex)

        for edge_key, edge_value in self.graph.edges.items():
            from_vertex, to_vertex = eval(str(edge_key))
            distance = edge_value["distance"]
            g.add_edge(from_vertex, to_vertex, distance=distance)

        # Define as posições dos vértices no layout do grafo
        pos = nx.spring_layout(g)

        nx.draw_networkx_nodes(g, pos, node_color="lightblue", node_size=500)

        edge_labels = {
            (u, v): f"{g.edges[u, v]['distance']}" for u, v in g.edges}
        nx.draw_networkx_edges(g, pos, arrowstyle="->", arrowsize=10)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

        # Exibe o nome dos pontos de interesse nos vértices
        labels = {vertex: vertex for vertex in g.nodes}
        nx.draw_networkx_labels(g, pos, labels)

        # Exibe o grafo
        plt.axis("off")
        plt.show()

    def interromper_via(self, via_list: List[List[str]]) -> List[List[str]]:
        """
        Interrompe temporariamente uma ou mais vias de circulação.
        Retorna uma lista de caminhos alternativos entre os pontos,
        ordenados por ordem crescente da distância utilizando o Bubble Sort.
        """
        caminhos_alternativos = []

        for via in via_list:
            if len(via) >= 2:
                from_vertex = via[0]
                to_vertex = via[-1]

                # Verifica se os pontos existem no grafo
                if from_vertex in self.graph.vertices and to_vertex in self.graph.vertices:
                    edge_data = self.graph.edges[(from_vertex, to_vertex)]
                    original_distance = edge_data["distance"]
                    min_speed = edge_data["min_speed"]
                    max_speed = edge_data["max_speed"]
                    orientation = edge_data["orientation"]

                    self.graph.remove_edge(from_vertex, to_vertex)

                    # Encontra caminhos alternativos para a via interrompida
                    queue = [[from_vertex]]

                    while queue:
                        caminho_atual = queue.pop(0)
                        ultimo_vertice = caminho_atual[-1]

                        # Verifica se chegamos ao ponto de destino
                        if ultimo_vertice == to_vertex:
                            caminhos_alternativos.append(caminho_atual)
                            continue

                        # Explora os vizinhos do último vértice do caminho atual
                        vizinhos = self.graph.vertices[ultimo_vertice]
                        for vizinho in vizinhos:
                            if vizinho not in caminho_atual:
                                novo_caminho = caminho_atual + [vizinho]
                                queue.append(novo_caminho)

                    self.graph.add_edge(from_vertex, to_vertex, original_distance,
                                        min_speed, max_speed, orientation)

        # Ordena os caminhos alternativos utilizando Bubble Sort
        n = len(caminhos_alternativos)
        for i in range(n - 1):
            for j in range(n - i - 1):
                distancia_j = self.calcular_distancia(caminhos_alternativos[j])
                distancia_j_plus_1 = self.calcular_distancia(caminhos_alternativos[j + 1])
                if distancia_j > distancia_j_plus_1:
                    caminhos_alternativos[j], caminhos_alternativos[j + 1] = caminhos_alternativos[j + 1], \
                                                                             caminhos_alternativos[j]

        return caminhos_alternativos

    def calcular_distancia(self, caminho: List[str]) -> float:
        """
        Calcula a distância total de um caminho.
        """
        distancia_total = 0.0

        for i in range(len(caminho) - 1):
            edge_data = self.graph.edges[(caminho[i], caminho[i + 1])]
            distancia_total += edge_data["distance"]

        return distancia_total

    def obter_itinerario(self, origem: str, destino: str) -> str:
        """
                Obtém o itinerário entre dois pontos de interesse turístico.

        :param origem: Ponto de origem
        :param destino: Ponte de destino
        :return: Retorna uma string formatada com informações sobre a distância,
        tempo de viagem de carro e tempo de viagem a pé do caminho mais curto.
        """

        if origem not in self.graph.vertices or destino not in self.graph.vertices:
            return ""

        # Caminho mais curto para carro
        distancia_carro, caminho_carro = self.dijkstra(
            origem, destino, mode='car')

        # Caminho mais curto a pé
        distancia_pe, caminho_pe = self.dijkstra(origem, destino, mode='pe')

        # Obtém o tempo total de viagem de carro
        tempo_total_carro = 0.0
        for i in range(len(caminho_carro) - 1):
            from_vertex = caminho_carro[i]
            to_vertex = caminho_carro[i + 1]
            edge_data = self.graph.map[from_vertex][to_vertex]
            tempo_total_carro += edge_data['car_time']

        # Obtém o tempo total de viagem a pé
        tempo_total_pe = 0.0
        for i in range(len(caminho_pe) - 1):
            from_vertex = caminho_pe[i]
            to_vertex = caminho_pe[i + 1]
            edge_data = self.graph.map[from_vertex][to_vertex]
            tempo_total_pe += edge_data['pedestrian_time']

        # Constrói a string formatada com as informações do itinerário
        itinerario = f"Origem: {origem}\n"
        itinerario += f"Destino: {destino}\n"
        itinerario += f"Distância de carro: {distancia_carro} km\n"
        itinerario += f"Tempo total de viagem de carro: {tempo_total_carro:.2f} horas\n"
        itinerario += f"Distância a pé: {distancia_pe} km\n"
        itinerario += f"Tempo total de viagem a pé: {tempo_total_pe:.2f} horas\n"
        itinerario += "Caminho de carro:\n"
        itinerario += "\n".join(caminho_carro) + "\n"
        itinerario += "Caminho a pé:\n"
        itinerario += "\n".join(caminho_pe)

        return itinerario

    def dijkstra(self, origem: str, destino: str, mode: str = 'car') -> Tuple[float, List[str]]:
        """
        Aplica o algoritmo de Dijkstra para encontrar o caminho mais curto entre dois vértices.
        :param origem: Ponto de origem
        :param destino: Ponto de destino
        :param mode: Modo de locomoção
        :return:Retorna um tuplo contendo a distância mais curta e o caminho mais curto como uma lista de vértices
        """

        # Inicializa o dicionário de distâncias com infinito para todos os vértices, exceto a origem
        distances: Dict[str, float] = {
            vertex: math.inf for vertex in self.graph.get_vertices()}
        distances[origem] = 0.0

        # Inicializa o dicionário de vértices anterior
        previous: Dict[str, Optional[str]] = {
            vertex: None for vertex in self.graph.get_vertices()}

        # Crie uma priority queue para armazenar vértices com as  suas distâncias correspondentes
        priority_queue: List[Tuple[str, float]] = [(origem, 0.0)]

        while priority_queue:
            # Obtém o vértice com a distância mínima da priority queue
            current_vertex, current_distance = min(
                priority_queue, key=lambda x: x[1])
            priority_queue.remove((current_vertex, current_distance))

            if current_vertex == destino:
                # Destino alcançado, construa o caminho mais curto
                path = []
                while current_vertex:
                    path.append(current_vertex)
                    current_vertex = previous[current_vertex]
                path.reverse()
                return distances[destino], path

            # Explora os vizinhos do vértice atual
            for neighbor in self.graph.vertices[current_vertex]:
                edge_data = self.graph.map[current_vertex][neighbor]
                if mode == 'car':
                    distance = edge_data['distance']
                    max_speed = edge_data['max_speed']
                    time = distance / max_speed
                else:
                    distance = edge_data['distance']
                    time = edge_data['pedestrian_time']

                # Calcula a nova distância ao vizinho através do vértice atual
                new_distance = current_distance + distance

                if new_distance < distances[neighbor]:
                    # Atualiza a distância e o vértice anterior
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_vertex

                    # Adiciona o vizinho à priority queue com a nova distância
                    priority_queue.append((neighbor, new_distance))

        # Nenhum caminho encontrado da origem ao destino
        return math.inf, []

    def consultar_rotas_carro(self, origens: List[str]) -> str:
        """
        Consulta rotas para viagens de carro e exibe uma árvore de abrangência com os
         pontos de interesse escolhidos como raízes.
        :param origens: Lista de pontos de origem
        :return: Retorna uma mensagem de status indicando sucesso e desenha a árvore
        """
        if not origens:
            return "Nenhum ponto de origem fornecido."

        # Criar um grafo vazio
        spanning_tree = nx.Graph()

        # Realizar a busca em largura para cada ponto de origem
        for origem in origens:
            if origem not in self.graph.vertices:
                continue

            queue = [origem]
            visited = set()

            while queue:
                vertex = queue.pop(0)
                visited.add(vertex)

                neighbors = self.graph.vertices[vertex]

                for neighbor in neighbors:
                    if neighbor not in visited:
                        spanning_tree.add_edge(vertex, neighbor)
                        queue.append(neighbor)

        # Desenhar a árvore de abrangência
        pos = nx.spring_layout(spanning_tree)

        nx.draw_networkx(spanning_tree, pos, with_labels=True, node_color='lightblue',
                         node_size=500, alpha=0.8, font_size=8)

        # Mostrar o gráfico
        plt.axis("off")
        plt.show()

        return "Árvore de abrangência de rotas de carro gerada com sucesso."
