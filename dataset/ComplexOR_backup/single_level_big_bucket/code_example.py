def single_level_big_bucket(demand, total_capacity, capacity, 
                       holding_cost, backlog_cost, fixed_cost, initial_stock):
    """
    Solve the Lot Sizing Problem with Single Level Big Bucket.

    Args:
        demand: 2D list of integers, demand of item `i` in period `t`
        total_capacity: list of integers, total capacity in period `t`
        capacity: 2D list of integers, production capacity of item `i` in period `t`
        holding_cost: list of integers, holding cost of item `i`
        backlog_cost: list of integers, backlog cost of item `i`
        fixed_cost: list of integers, fixed cost of producing item `i`
        initial_stock: list of integers, initial stock of item `i`

    Returns:
        min_cost: float, the minimized total cost
    """
    min_cost = 1e9
    return min_cost