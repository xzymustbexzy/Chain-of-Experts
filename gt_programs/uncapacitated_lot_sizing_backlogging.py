from pulp import *

def uncapacitated_lot_sizing_backlogging(periods, demand, cost_fixed, cost_unit_order, cost_unit_hold, penalty):
    # Define the problem
    prob = LpProblem("Uncapacitated_Lot_Sizing_Backlogging", LpMinimize)

    # Variables
    OrderedAmount = LpVariable.dicts("OrderedAmount", periods, 0, None, LpContinuous)
    EndingInventory = LpVariable.dicts("EndingInventory", periods, 0, None, LpContinuous)
    OrderIsPlaced = LpVariable.dicts("OrderIsPlaced", periods, 0, 1, LpInteger)
    BackloggedAmount = LpVariable.dicts("BackloggedAmount", periods, 0, None, LpContinuous)

    # Objective function
    prob += lpSum([cost_fixed[t] * OrderIsPlaced[t] + cost_unit_order[t] * OrderedAmount[t] + cost_unit_hold[t] * EndingInventory[t] + penalty[t] * BackloggedAmount[t] for t in periods])

    # Constraints
    for t in periods:
        if t == 0:
            prob += EndingInventory[t-1] + OrderedAmount[t] - BackloggedAmount[t-1] == demand[t] - BackloggedAmount[t]
            prob += OrderedAmount[t] <= OrderIsPlaced[t] * lpSum(demand)
            prob += EndingInventory[t] == 0
            prob += BackloggedAmount[t] == 0
        else:
            prob += EndingInventory[t-1] + OrderedAmount[t] - BackloggedAmount[t-1] == demand[t] + EndingInventory[t] - BackloggedAmount[t]
            prob += OrderedAmount[t] <= OrderIsPlaced[t] * lpSum(demand)
            prob += EndingInventory[t] == 0
            prob += BackloggedAmount[t] == 0
            
    # Solve the problem
    prob.solve()
    total_cost = value(prob.objective)
    
    return total_cost