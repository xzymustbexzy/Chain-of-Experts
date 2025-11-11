def electrical_power(generator_types, time_periods, generators, demand, on_start, min_output, max_output, base_cost, per_mw_cost, startup_cost):
    """
    Args:
        generator_types: list of integers, distinct generator types
        time_periods: list of integers, set of time periods
        generators: list of integers, number of generators of each type
        demand: list of integers, total power demand for each time period
        on_start: integer, number of generators that are on at the beginning
        min_output: list of integers, minimum output for each generator type
        max_output: list of integers, maximum output for each generator type
        base_cost: list of integers, minimum operating cost per hour for each generator type
        per_mw_cost: list of integers, cost to generate one MW per hour for each generator type
        startup_cost: list of integers, startup cost for each generator type

    Returns:
        total_cost: the cost to satisfy the predicted electricity demand.
    """
    # To be implemented
    total_cost = 0
    return total_cost