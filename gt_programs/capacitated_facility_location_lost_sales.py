from gurobipy import Model, GRB, quicksum

def capacitated_facility_location_lost_sales(demand, production_time, setup_time, capacity, production_cost, setup_cost, inventory_holding_cost, lost_sales_cost, big_number):
    """
    Solve the capacitated lot-sizing problem with setup times and lost sales.
    """
    # Number of items and periods
    num_items = len(demand)
    num_periods = len(demand[0])
    
    # Initialize model
    m = Model('capacitated_lot_sizing')
    
    # Decision variables
    ProductionUnits = {(i, t): m.addVar(vtype=GRB.CONTINUOUS, name=f"prod_units_{i}_{t}") for i in range(num_items) for t in range(num_periods)}
    Inventory = {(i, t): m.addVar(vtype=GRB.CONTINUOUS, name=f"inventory_{i}_{t}") for i in range(num_items) for t in range(num_periods)}
    SetupVariable = {(i, t): m.addVar(vtype=GRB.BINARY, name=f"setup_var_{i}_{t}") for i in range(num_items) for t in range(num_periods)}
    LostSales = {(i, t): m.addVar(vtype=GRB.CONTINUOUS, name=f"lost_sales_{i}_{t}") for i in range(num_items) for t in range(num_periods)}
    
    # Objective function
    m.setObjective(
        quicksum(setup_cost[i][t] * SetupVariable[i, t] +
                 production_cost[i][t] * ProductionUnits[i, t] +
                 inventory_holding_cost[i][t] * Inventory[i, t] +
                 lost_sales_cost[i][t] * LostSales[i, t]
                 for i in range(num_items) for t in range(num_periods)),
        GRB.MINIMIZE
    )
    
    # Constraints
    # Inventory balance
    for i in range(num_items):
        for t in range(num_periods):
            m.addConstr(
                (Inventory[i, t-1] if t > 0 else 0) + ProductionUnits[i, t] - LostSales[i, t] ==
                Demand[i][t] + Inventory[i, t], 
                f"inventory_balance_{i}_{t}"
            )

    # Capacity constraints
    for t in range(num_periods):
        m.addConstr(
            quicksum(setup_time[i][t] * SetupVariable[i, t] + production_time[i][t] * ProductionUnits[i, t] 
                     for i in range(num_items)) <= capacity[t], 
            f"capacity_{t}"
        )

    # Production-Setup linking
    for i in range(num_items):
        for t in range(num_periods):
            m.addConstr(
                ProductionUnits[i, t] <= big_number * SetupVariable[i, t], 
                f"linking_{i}_{t}"
            )

    # Lost sales constraints
    for i in range(num_items):
        for t in range(num_periods):
            m.addConstr(
                LostSales[i, t] <= demand[i][t],
                f"lost_sales_{i}_{t}"
            )
    
    # Solve the model
    m.optimize()
    
    # Collect results if the model is solved to optimality
    if m.status == GRB.OPTIMAL:
        minimize_cost = m.objVal
        return minimize_cost
    else:
        raise Exception("The model did not solve to optimality.")

# Example inputs to run the model are same as provided above
