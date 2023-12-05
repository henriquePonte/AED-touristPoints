from Sistema.Grafo import Graph

graph = Graph()

graph.add_vertex("A")
graph.add_vertex("B")
graph.add_vertex("C")

graph.add_edge("A", "B", 5.0, 30, 60, 1)
graph.add_edge("B", "C", 7.0, 40, 70, 1)
graph.add_edge("A", "C", 10.0, 30, 60, 1)

vertices = graph.get_vertices()
print("Vertices:", vertices)

edges = graph.get_edges()
print("Edges:", edges)

result = graph.remove_vertex("B")
print("Remove Vertex:", result)

#result = graph.remove_edge("A", "C")
#print("Remove Edge:", result)

path = graph.from_result_to_shortest_path({"A": (0, None), "B": (5, "A"), "C": (15, "B")}, "C")
print("Shortest Path:", path)

is_empty = graph.is_empty()
print("Is Empty:", is_empty)

graph.add_vertex("D")
graph.add_vertex("E")
print("Length:", len(graph))

print(graph)
