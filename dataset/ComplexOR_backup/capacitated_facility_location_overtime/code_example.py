def capacitated_facility_location_overtime(periods, resources, products, products_per_resource, successors, 
           required_units, capacity, big_number, overtime_cost, holding_cost, 
           setup_cost, production_time_per_unit, setup_time, initial_inventory, demand):
    """
    Args:
        periods: list of integers, representing time periods [1, 2, 3, ..., P]
        resources: list of integers, representing resources
        products: list of integers, representing products
        products_per_resource: dictionary, mapping each resource to the list of products it can produce
        successors: dictionary, mapping each product to the list of its immediate successors
        required_units: 2D list, number of units of product k required to produce one unit of product i
        capacity: 2D list, available capacity of resource j in each period
        big_number: an integer, a big number for setting constraints
        overtime_cost: list of integers, overtime cost per unit of overtime at each resource
        holding_cost: list of integers, holding cost of each product per unit and period
        setup_cost: list of integers, setup cost of each product
        production_time_per_unit: list of integers, production time per unit of each product
        setup_time: list of integers, setup time of each product
        initial_inventory: list of integers, initial inventory for each product
        demand: 2D list, external demand for each product in each period

    Returns:
        least_cost: an integer, the minimum cost calculated based on the model
    """
    least_cost = 0
    return least_cost