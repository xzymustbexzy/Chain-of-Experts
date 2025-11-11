def capacitated_facility_location(FixedCost, TransportCost, Capacity, Demand):
    """
    Solves the Capacitated Facility Location Problem.

    Args:
        FixedCost (list of int): Fixed costs of maintaining/building each facility.
        TransportCost (list of list of int): Transportation costs of allocating customer demand to facilities.
        Capacity (list of int): Capacities of each facility.
        Demand (list of int): Demands of each customer.

    Returns:
        DistributionCost (float): The total minimized distribution cost.
    """
    DistributionCost = 0 
    return DistributionCost