def capacitated_warehouse_location(Locations, Customers, Demand, AllocationCost, Capacity, LowerLimitOnDemand, LowerLimitOfOpenWarehouses, UpperLimitOfOpenWarehouses, FixedCost):
    """
    Args:
        Locations: list of integers, potential warehouse locations
        Customers: list of integers, list of customers
        Demand: list of integers, demand of each customer
        AllocationCost: 2D list of integers, allocation cost between each location and customer
        Capacity: list of integers, capacity of each warehouse location
        LowerLimitOnDemand: list of integers, lower limit on demand that must be satisfied in each location
        LowerLimitOfOpenWarehouses: integer, minimum number of warehouses that must be opened
        UpperLimitOfOpenWarehouses: integer, maximum number of warehouses that can be opened
        FixedCost: list of integers, fixed cost of opening each warehouse location

    Returns:
        least_cost: integer, the minimized total cost (including shipping and fixed costs)
    """
    # To be implemented
    least_cost = 0
    return least_cost