from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution

class BellmanFordSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points
            callback (Optional[Visualiser], optional): Callback for 
            visualisation. Defaults to None.

        Returns:
            Solution: Solution found
        """

        # Create Node for the source cell
        node = grid.get_node(pos=grid.start)

        # Instantiate PriorityQueue frontier and add node into it
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        # Keep track of G scores
        distance = {grid.start: 0}

        explored = []

        while True:
            # Return empty Solution object for no solution
            if frontier.is_empty():
                return NoSolution([], explored)

            # Remove node from the frontier
            node = frontier.pop()
            if node.state not in explored:
                explored.append(node.state)

            # If reached destination point
            if node.state == grid.end:

                # Generate path and return a Solution object
                cells = []

                path_cost = 0

                temp = node
                while temp.parent != None:
                    cells.append(temp.state)
                    path_cost += temp.cost
                    temp = temp.parent

                cells.append(grid.start)
                cells.reverse()

                return Solution(cells, explored, path_cost=path_cost)

            # Determine possible actions
            for action, state in grid.get_neighbours(node.state).items():
                cost = distance[node.state] + grid.get_cost(state)

                if state not in distance or cost < distance[state]:
                    distance[state] = cost

                    n = grid.get_node(pos=state)
                    n.parent = node

                    if not n.action:
                        n.action = action

                    frontier.add(
                        node=n,
                        priority=cost
                    )

# class BellmanFordSearch:
#     @staticmethod
#     def search(grid: Grid) -> Solution:
#         """Find path between two points in a grid using Bellman-Ford Algorithm

#         Args:
#             grid (Grid): Grid of points

#         Returns:
#             Solution: Solution found
#         """
#         # Initialize distances
#         distance = {(i, j): float('infinity') 
#                    for i in range(len(grid.grid)) 
#                    for j in range(len(grid.grid[0]))}
#         distance[grid.start] = 0
        
#         # Keep track of parent nodes
#         parent = {}
        
#         explored = []
        
#         # Relax edges |V|-1 times
#         num_vertices = len(grid.grid) * len(grid.grid[0])
        
#         for _ in range(num_vertices - 1):
#             for i in range(len(grid.grid)):
#                 for j in range(len(grid.grid[0])):
#                     pos = (i, j)
#                     if pos not in explored:
#                         explored.append(pos)
                    
#                     for neighbor in grid.get_neighbours(pos).values():
#                         if grid.grid[neighbor[0]][neighbor[1]].value != "#":
#                             cost = grid.grid[neighbor[0]][neighbor[1]].cost
#                             if distance[pos] != float('infinity') and distance[pos] + cost < distance[neighbor]:
#                                 distance[neighbor] = distance[pos] + cost
#                                 parent[neighbor] = pos

#         # Check for negative weight cycles
#         for i in range(len(grid.grid)):
#             for j in range(len(grid.grid[0])):
#                 pos = (i, j)
#                 for neighbor in grid.get_neighbours(pos).values():
#                     cost = grid.get_cost(neighbor)
#                     if distance[pos] != float('infinity') and distance[pos] + cost < distance[neighbor]:
#                         return NoSolution([], explored)  # Negative cycle exists

#         # If end is not reachable
#         if distance[grid.end] == float('infinity'):
#             return NoSolution([], explored)

#         # Reconstruct path
#         cells = []
#         current = grid.end
#         path_cost = distance[grid.end]
#         while current is not None:
#             cells.append(current)
#             if current == grid.start:
#                 break
#             current = parent[current] if parent[current] else None

#         cells.reverse()
        
#         return Solution(cells, explored, path_cost=path_cost)

# def BellmanFordSearch(graph, start):
#     # عدد العقد في الرسم البياني
#     distances = {node: float('inf') for node in graph}
#     distances[start] = 0

#     # التكرار عبر جميع الحواف لتحديث المسافات
#     for _ in range(len(graph) - 1):
#         for node in graph:
#             for neighbor, weight in graph[node].items():
#                 if distances[node] + weight < distances[neighbor]:
#                     distances[neighbor] = distances[node] + weight

#     # التحقق من الحواف السلبية
#     for node in graph:
#         for neighbor, weight in graph[node].items():
#             if distances[node] + weight < distances[neighbor]:
#                 print("Graph contains negative weight cycle")
#                 return None

#     return distances
