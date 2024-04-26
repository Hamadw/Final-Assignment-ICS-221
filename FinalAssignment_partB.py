import heapq  # Helps with sorting and managing a list like it's a queue.
import math  # Provides access to mathematical functions.


def heuristic(current_vertex, end_vertex):
   current_x, current_y = divmod(int(current_vertex[1:]) - 1, 10)
   end_x, end_y = divmod(int(end_vertex[1:]) - 1, 10)
   return abs(end_x - current_x) + abs(end_y - current_y)


class GraphMatrix:
   def __init__(self, num_vertices):
       if num_vertices > 100:
           raise ValueError("Maximum of 100 vertices are allowed.")
       self.num_vertices = num_vertices
       self.adjacency_matrix = [[math.inf] * num_vertices for _ in range(num_vertices)]
       self.vertices_info = {}
       self.edges_info = {}
       self.houses_info = {}


   def add_vertex(self, vertex_id):
       if vertex_id not in self.vertices_info:
           index = int(vertex_id[1:]) - 1
           if index < self.num_vertices:
               self.vertices_info[vertex_id] = {"ID": vertex_id}
           else:
               print(f"Vertex ID {vertex_id} is out of the allowed range.")
       else:
           print(f"Vertex {vertex_id} already exists.")


   def add_edge(self, from_vertex, to_vertex, edge_id, name, length, weight):
       if from_vertex in self.vertices_info and to_vertex in self.vertices_info:
           from_index = int(from_vertex[1:]) - 1
           to_index = int(to_vertex[1:]) - 1
           if from_index < self.num_vertices and to_index < self.num_vertices:
               self.adjacency_matrix[from_index][to_index] = weight
               self.adjacency_matrix[to_index][from_index] = weight
               self.edges_info[edge_id] = {
                   "ID": edge_id, "name": name, "length": length, "weight": weight,
                   "from": from_vertex, "to": to_vertex
               }
           else:
               print(f"Indices for {from_vertex} or {to_vertex} are out of the allowed range.")
       else:
           print(f"One or both vertices {from_vertex} and {to_vertex} do not exist.")


   def add_house(self, house_id, vertex_id):
       if vertex_id in self.vertices_info:
           self.houses_info[house_id] = vertex_id
           self.add_vertex(house_id)
           self.add_edge(house_id, vertex_id, f"{house_id}-to-{vertex_id}", "Access Road", 1, 1)
       else:
           print(f"Vertex {vertex_id} does not exist to link house {house_id}.")


   def dijkstra(self, start_vertex):
       distances = {vertex: math.inf for vertex in self.vertices_info}
       distances[start_vertex] = 0
       pq = [(0, start_vertex)]
       while pq:
           current_distance, current_vertex = heapq.heappop(pq)
           current_index = int(current_vertex[1:]) - 1
           for neighbor_index, weight in enumerate(self.adjacency_matrix[current_index]):
               if weight != math.inf:
                   neighbor_vertex = f'I{neighbor_index + 1}'
                   distance = current_distance + weight
                   if distance < distances[neighbor_vertex]:
                       distances[neighbor_vertex] = distance
                       heapq.heappush(pq, (distance, neighbor_vertex))
       return distances


   def a_star(self, start_vertex, end_vertex):
       start_index = int(start_vertex[1:]) - 1
       distances = {vertex: math.inf for vertex in self.vertices_info}
       distances[start_vertex] = 0
       open_set = [(0, start_vertex)]
       came_from = {vertex: None for vertex in self.vertices_info}
       while open_set:
           current_distance, current_vertex = heapq.heappop(open_set)
           if current_vertex == end_vertex:
               path = []
               while current_vertex:
                   path.append(current_vertex)
                   current_vertex = came_from[current_vertex]
               return path[::-1]
           current_index = int(current_vertex[1:]) - 1
           for neighbor_index, weight in enumerate(self.adjacency_matrix[current_index]):
               if weight != math.inf:
                   neighbor_vertex = f'I{neighbor_index + 1}'
                   tentative_g_score = distances[current_vertex] + weight
                   if tentative_g_score < distances[neighbor_vertex]:
                       came_from[neighbor_vertex] = current_vertex
                       distances[neighbor_vertex] = tentative_g_score
                       f_score = tentative_g_score + heuristic(neighbor_vertex, end_vertex)
                       heapq.heappush(open_set, (f_score, neighbor_vertex))
       return "No path found"


   def find_shortest_path_to_house(self, house_id, destination_vertex):
       start_vertex = self.houses_info.get(house_id)
       if not start_vertex:
           return f"No starting point found for house {house_id}"
       return self.dijkstra(start_vertex)[destination_vertex]



# Test Cases
# Graph setup
city_graph_matrix = GraphMatrix(100)  # Maximum of 100 vertices
for i in range(1, 101):
   city_graph_matrix.add_vertex(f"I{i}")
city_graph_matrix.add_edge("I1", "I2", "R1", "Main St", 10, 5)
city_graph_matrix.add_edge("I2", "I3", "R2", "2nd St", 10, 5)
city_graph_matrix.add_edge("I3", "I4", "R3", "3rd St", 10, 5)
city_graph_matrix.add_house("H1", "I5")
city_graph_matrix.add_house("H2", "I10")


# Tests
print(city_graph_matrix.dijkstra("I1")["I4"])
print(city_graph_matrix.a_star("I1", "I4"))
print(city_graph_matrix.find_shortest_path_to_house("H1", "I4"))
