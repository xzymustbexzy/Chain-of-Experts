def netthru(cities, links, supply, demand, cost, city_capacity, link_capacity):
    """
    Args:
        cities: list of cities
        links: list of tuples representing links between cities (i, j)
        supply: list of integers representing amounts of goods available at each city
        demand: list of integers representing amounts of goods required at each city
        cost: 2D list representing shipment costs per ton over each link (i, j)
        city_capacity: list of integers representing maximum throughput at each city
        link_capacity: 2D list representing maximum shipment over each link (i, j)

    Returns:
        total_cost: a float, denotes the total minimum cost of shipping goods over the network
    """
    total_cost = 0.0
    return total_cost