import pulp

def nltrans(supply, demand, rate, limit):
    """
    Args:
        supply: a list of integers, each indicates the amount of goods available at an origin
        demand: a list of integers, each indicates the amount of goods required at a destination
        rate: a 2D list of integers, the shipment costs per unit from each origin to each destination
        limit: a 2D list of integers, the limit on units shipped from each origin to each destination

    Returns:
        total_cost: an integer, denotes the minimum total cost of shipping goods
    """
    
    # Initiate the model
    model = pulp.LpProblem("Minimize_Shipping_Cost", pulp.LpMinimize)

    # Origins and destinations
    Origins = range(len(supply))
    Destinations = range(len(demand))

    # Decision variable
    Shipping = {(i, j): pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, name="Shipping_{0}_{1}".format(i, j)) for i in Origins for j in Destinations}

    # Objective
    model += pulp.lpSum([Shipping[(i, j)] * rate[i][j] for i in Origins for j in Destinations])

    # Each origin supply constraint
    for i in Origins:
        model += pulp.lpSum([Shipping[(i, j)] for j in Destinations]) <= supply[i]

    # Each destination demand constraint
    for j in Destinations:
        model += pulp.lpSum([Shipping[(i, j)] for i in Origins]) >= demand[j]

    # Shipping limit constraint
    for i in Origins:
        for j in Destinations:
            model += Shipping[(i, j)] <= limit[i][j]

    model.solve()

    total_cost = pulp.value(model.objective)
    return total_cost