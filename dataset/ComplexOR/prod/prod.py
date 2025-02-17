def prod(a, c, u, b):
    """
    Args:
        a: a list of integers, parameter for each element in set P
        c: a list of integers, profit coefficient for each element in set P
        u: a list of integers, upper limit for each element in set P
        b: an integer, the global constraint parameter

    Returns:
        total_profit: an integer, denotes the maximum total profit after calculation
    """
    # Import gurobipy
    from gurobipy import Model, GRB

    # Check that a, c, and u have the same length
    if not (len(a) == len(c) == len(u)):
        raise ValueError("Input lists a, c, and u must have the same length")

    # Check that a[j] != 0 and u[j] >= 0
    for idx in range(len(a)):
        if a[idx] == 0:
            raise ValueError("Parameter a[{}] is zero, division by zero not allowed.".format(idx))
        if u[idx] < 0:
            raise ValueError("Upper limit u[{}] cannot be negative.".format(idx))

    # Create the model
    m = Model("profit_maximization")
    m.setParam('OutputFlag', 0)  # Suppress Gurobi output

    # Number of elements in P
    n = len(a)
    P = range(n)

    # Add variables X[j] for j in P
    X = {}
    for j in P:
        X[j] = m.addVar(lb=0, ub=u[j], name="X_{}".format(j))

    # Set the objective function: maximize sum of c[j] * X[j]
    m.setObjective(sum(c[j] * X[j] for j in P), GRB.MAXIMIZE)

    # Add the constraint: sum over j of (1/a[j]) * X[j] <= b
    m.addConstr(sum((1.0 / a[j]) * X[j] for j in P) <= b, "constraint")

    # Optimize the model
    m.optimize()

    # Retrieve the total profit
    if m.status == GRB.OPTIMAL:
        total_profit = int(round(m.objVal))
    else:
        total_profit = 0  # You may handle infeasibility differently if needed

    return total_profit
