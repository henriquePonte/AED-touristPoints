class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.map = {}

    def is_empty(self) -> bool:
        """

        :return: Verifica se esta vazia
        """
        return len(self.vertices) == 0

    def __len__(self) -> int:
        """

        :return: Retorna o tamanho do grafo
        """
        return len(self.vertices)

    def __str__(self) -> str:
        """

        :return: Retorna os dados do grafo
        """
        output = ""
        for vertex, edges in self.vertices.items():
            output += f"Vertex: {vertex}\n"
            output += f"Edges: {', '.join(edges)}\n\n"
        return output

    def clear(self) -> None:
        """
        Limpa o grafo
        :return: None
        """
        self.vertices = {}
        self.edges = {}
        self.map = {}

    def get_vertices(self) -> set:
        """

        :return: Retorna os vertices
        """
        return set(self.vertices.keys())

    def get_edges(self) -> list:
        """

        :return: Retorna as arestas
        """
        return list(self.edges.keys())

    def size_vertices(self) -> int:
        """

        :return: Retorna o numero de vertices
        """
        return len(self.vertices)

    def size_edges(self) -> int:
        """

        :return: Numero das arestas
        """
        return len(self.edges)

    def add_vertex(self, vertex) -> None:
        """
        Adicionar um vértice
        :param vertex: Nome do vértice
        :return: None
        """
        if vertex not in self.vertices:
            self.vertices[vertex] = []
            self.map[vertex] = {}

    def add_edge(self, from_vertex: str, to_vertex: str, distance: float, min_speed: int,
                 max_speed: int, orientation: int) -> str:
        """
        Adiciona uma aresta ao grafo.
        :param from_vertex: Ponto de Origem
        :param to_vertex:  Ponto de destino
        :param distance: Distância entre os 2 pontos
        :param min_speed: Velocidade mínima da via
        :param max_speed: Velocidade máxima da via
        :param orientation: Sentido da via
        :return: Retorna uma mensagem de status indicando sucesso ou fracasso
        """
        if from_vertex in self.vertices and to_vertex in self.vertices:
            if (from_vertex, to_vertex) not in self.edges:
                self.vertices[from_vertex].append(to_vertex)
                pedestrian_speed = 5
                car_speed = (min_speed + max_speed) / 2
                pedestrian_time = distance / pedestrian_speed
                car_time = distance / car_speed
                edge_data = {
                    'distance': distance,
                    'min_speed': min_speed,
                    'max_speed': max_speed,
                    'orientation': orientation,
                    'pedestrian_time': pedestrian_time,
                    'car_time': car_time
                }
                self.edges[(from_vertex, to_vertex)] = edge_data
                self.map[from_vertex][to_vertex] = edge_data
                if orientation == 2:
                    self.vertices[to_vertex].append(from_vertex)
                    self.edges[(to_vertex, from_vertex)] = edge_data
                    self.map[to_vertex][from_vertex] = edge_data
            return "Aresta criada"
        return "Erro ao criar aresta"

    def remove_vertex(self, vertex) -> str:
        """
        Remover um vértice do grafo
        :param vertex: Nome do vértice
        :return: Retorna uma mensagem de status indicando sucesso ou fracasso
        """
        if vertex in self.vertices:
            for neighbor in self.vertices[vertex]:
                if vertex in self.vertices[neighbor]:
                    self.vertices[neighbor].remove(vertex)

            del self.vertices[vertex]
            self.edges = {key: value for key, value in self.edges.items() if vertex not in key}
            self.map = {key: value for key, value in self.map.items() if vertex not in value}
            return "Vértice removido com sucesso."
        else:
            return "Vértice não encontrado."

    def remove_edge(self, from_vertex: str, to_vertex: str) -> str:
        """
        Remover uma aresta do grafo
        :param from_vertex: Vértice de Origem
        :param to_vertex: Vértice de Destino
        :return: Retorna uma mensagem de status indicando sucesso ou fracasso
        """
        if (from_vertex, to_vertex) in self.edges:
            self.vertices[from_vertex].remove(to_vertex)
            del self.edges[(from_vertex, to_vertex)]
            del self.map[from_vertex][to_vertex]
            if (to_vertex, from_vertex) in self.edges:
                del self.edges[(to_vertex, from_vertex)]
                del self.map[to_vertex][from_vertex]
            return "Aresta removida com sucesso."
        else:
            return "Aresta não encontrada."

    def from_result_to_shortest_path(self, from_vertex, to_vertex):
        """

        :param from_vertex: Vértice de Origem
        :param to_vertex: Vértice de Destino
        :return: Retorna uma mensagem de status indicando fracasso ou a lista do caminho mais curto
        """
        reversed_path = []
        current_vertex = to_vertex
        while current_vertex in from_vertex and from_vertex[current_vertex][1] is not None:
            reversed_path.append(current_vertex)
            current_vertex = from_vertex[current_vertex][1]
        if current_vertex not in from_vertex:
            return "Caminho não encontrado"
        path = []
        while reversed_path:
            path.append(reversed_path.pop())
        return path

    def internal_degree_centrality(self):
        degree_centrality = {}
        num_vertices = len(self.vertices)
        for vertex in self.vertices:
            degree_centrality[vertex] = len(self.vertices[vertex]) / (num_vertices - 1)
        return degree_centrality

    def external_degree_centrality(self):
        external_degree = {}
        for vertex in self.vertices:
            external_degree[vertex] = 0
            for edge in self.edges:
                from_vertex, to_vertex = edge
                if from_vertex == vertex and to_vertex not in self.vertices:
                    external_degree[vertex] += 1
        return external_degree

    def closeness_centrality(self):
        closeness_centrality = {}
        for vertex in self.vertices:
            total_distance = 0
            for target in self.vertices:
                if target != vertex:
                    shortest_path = self.shortest_path(vertex, target)
                    total_distance += len(shortest_path) - 1 if shortest_path else 0
            if total_distance > 0:
                closeness_centrality[vertex] = (len(self.vertices) - 1) / total_distance
            else:
                closeness_centrality[vertex] = 0.0
        return closeness_centrality

    def shortest_path(self, source, target):
        queue = [(source, [source])]
        while queue:
            vertex, path = queue.pop(0)
            if vertex == target:
                return path
            for neighbor in self.vertices[vertex]:
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))