from gurobipy import Model, GRB

def aircraft_landing(EarliestLanding, LatestLanding, TargetLanding, PenaltyAfterTarget, PenaltyBeforeTarget, SeparationTime):
    """
    Args:
        EarliestLanding: list of integers, earliest landing times for each aircraft.
        LatestLanding: list of integers, latest landing times for each aircraft.
        TargetLanding: list of integers, target landing times for each aircraft.
        PenaltyAfterTarget: list of integers, penalties for landing after target times for each aircraft.
        PenaltyBeforeTarget: list of integers, penalties for landing before target times for each aircraft.
        SeparationTime: 2D list of integers, separation times between each pair of aircraft.

    Returns:
        min_total_penalty: an integer, denotes the minimized total penalty after calculation.
    """

    n = len(EarliestLanding)  # Number of aircraft

    # Create a new model
    model = Model()

    # Decision variables:
    # t_i: actual landing time of aircraft i
    t = model.addVars(n, lb=EarliestLanding, ub=LatestLanding, vtype=GRB.CONTINUOUS, name="t")

    # e_i: earliness (time before target landing time)
    e = model.addVars(n, lb=0, vtype=GRB.CONTINUOUS, name="e")

    # l_i: lateness (time after target landing time)
    l = model.addVars(n, lb=0, vtype=GRB.CONTINUOUS, name="l")

    # Constraints:

    # Relationship between landing time, earliness, and lateness
    for i in range(n):
        model.addConstr(t[i] - TargetLanding[i] == l[i] - e[i], name=f"timing_{i}")

    # Order constraints: aircraft must land in a specific order
    for i in range(n - 1):
        model.addConstr(t[i] <= t[i + 1], name=f"order_{i}")

    # Separation constraints: minimum separation time between landings
    for i in range(n):
        for j in range(i + 1, n):
            model.addConstr(t[j] - t[i] >= SeparationTime[i][j], name=f"separation_{i}_{j}")

    # Objective: minimize total penalties for earliness and lateness
    total_penalty = sum(PenaltyBeforeTarget[i]*e[i] + PenaltyAfterTarget[i]*l[i] for i in range(n))
    model.setObjective(total_penalty, GRB.MINIMIZE)

    # Optimize the model
    model.optimize()

    # Retrieve the minimized total penalty
    if model.status == GRB.OPTIMAL:
        min_total_penalty = int(model.objVal)
    else:
        min_total_penalty = None  # If no optimal solution is found

    return min_total_penalty
