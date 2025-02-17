def netmcol(Cities, Links, Products, Supply, Demand, ShipmentCost, Capacity, JointCapacity):
    """
    Args:
        Cities: list, a list of cities
        Links: list, a list of links between the cities
        Products: list, a list of products
        Supply: list of lists, the supply of each product at each city
        Demand: list of lists, the demand of each product at each city
        ShipmentCost: list of lists of lists, the cost of shipping each product from each city to each city
        Capacity: list of lists of lists, the capacity of shipping each product from each city to each city
        JointCapacity: list of lists, the joint capacity of each link

    Returns:
        total_cost: float, the minimized total shipping cost after calculation
    """
    from gurobipy import Model, GRB, quicksum

    # Create a new model
    model = Model()

    # Create mapping from city and product names to indices
    city_to_index = {city: idx for idx, city in enumerate(Cities)}
    product_to_index = {product: idx for idx, product in enumerate(Products)}

    # Variables: x[i,j,p] for each link (i,j) and product p
    x = model.addVars(Links, Products, lb=0, name="x")

    # Objective: minimize total shipping cost
    model.setObjective(
        quicksum(
            ShipmentCost[city_to_index[i]][city_to_index[j]][product_to_index[p]] * x[i, j, p]
            for (i, j) in Links for p in Products
        ),
        GRB.MINIMIZE
    )

    # Build dictionaries of incoming and outgoing links for each city
    in_links = {i: [] for i in Cities}
    out_links = {i: [] for i in Cities}
    for (i, j) in Links:
        out_links[i].append(j)
        in_links[j].append(i)

    # Flow conservation constraints for each city and product
    for i in Cities:
        idx_i = city_to_index[i]
        for p in Products:
            idx_p = product_to_index[p]
            net_supply = Supply[idx_i][idx_p] - Demand[idx_i][idx_p]
            inflow = quicksum(x[j, i, p] for j in in_links[i])
            outflow = quicksum(x[i, j, p] for j in out_links[i])
            model.addConstr(net_supply + inflow - outflow == 0, name=f"flow_{i}_{p}")

    # Capacity constraints for each link and product
    for (i, j) in Links:
        idx_i = city_to_index[i]
        idx_j = city_to_index[j]
        for p in Products:
            idx_p = product_to_index[p]
            model.addConstr(
                x[i, j, p] <= Capacity[idx_i][idx_j][idx_p],
                name=f"capacity_{i}_{j}_{p}"
            )

    # Joint capacity constraints for each link
    for (i, j) in Links:
        idx_i = city_to_index[i]
        idx_j = city_to_index[j]
        model.addConstr(
            quicksum(x[i, j, p] for p in Products) <= JointCapacity[idx_i][idx_j],
            name=f"joint_capacity_{i}_{j}"
        )

    # Optimize the model
    model.optimize()

    # Retrieve the minimized total shipping cost
    total_cost = model.objVal

    return total_cost
