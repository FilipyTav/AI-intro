import heapq

# With weights
graph_cities: dict[str, dict[str, int]] = {
    # Vertex: { edges }
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "D": 5, "E": 10},
    "C": {"A": 2, "F": 3},
    "D": {"B": 5, "G": 8},
    "E": {"B": 10, "H": 9},
    "F": {"C": 3, "H": 6},
    "G": {"D": 8, "I": 7},
    "H": {"E": 9, "F": 6, "I": 1},
    "I": {"G": 7, "H": 1},
}


def create_node(
    name: str, g: float = float("inf"), h: float = 0.0, parent: dict = {}
) -> dict:
    return {"name": name, "g": g, "h": h, "f": g + h, "parent": parent}


def calc_heuristic(start: str, end: str) -> float:
    return 0


def reconstruct_path(goal_node: dict) -> tuple[list[str], float]:
    path: list[str] = []
    current = goal_node
    cost: float = goal_node["g"]

    while current:
        path.append(current["name"])
        current = current["parent"]

    return (path[::-1], cost)


def a_star_search(graph: dict, start: str, end: str) -> tuple[list[str], float]:
    # Initialize start node
    start_node = create_node(name=start, g=0, h=calc_heuristic(start, end))

    # Initialize open and closed sets
    open_list: list[tuple[float, str]] = [(start_node["f"], start)]
    open_dict: dict = {start_node["name"]: start_node}
    closed_set = set()

    while open_list:
        # Get node with lowest f value
        _, curr_nd_name = heapq.heappop(open_list)
        current_node = open_dict[curr_nd_name]

        if curr_nd_name == end:
            return reconstruct_path(current_node)

        closed_set.add(curr_nd_name)

        # Neighbours
        for n in graph[curr_nd_name]:
            if n in closed_set:
                continue

            cost: float = graph[curr_nd_name][n]
            # Total cost to get to this neighbour
            new_g = current_node["g"] + cost

            if n not in open_dict:
                neighbour = create_node(
                    name=n,
                    g=new_g,
                    h=calc_heuristic(n, end),
                    parent=current_node,
                )
                heapq.heappush(open_list, (neighbour["f"], n))
                open_dict[n] = neighbour
            elif new_g < open_dict[n]["g"]:
                # Found a better path to the neighbour
                neighbour = open_dict[n]
                neighbour["g"] = new_g
                neighbour["f"] = new_g + neighbour["h"]
                neighbour["parent"] = current_node

    return ([], 0)  # No path found


start_node: str = "A"
end_node: str = "I"

path, cost = a_star_search(graph_cities, start_node, end_node)
print(f"Shortest path: {path}, cost: {cost}")
