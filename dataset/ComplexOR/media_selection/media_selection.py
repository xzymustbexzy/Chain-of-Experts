def media_selection(target_audiences, advertising_media, incidence_matrix, media_costs):
    """
    Args:
        target_audiences: List of target audiences (typically a list of integers)
        advertising_media: List of advertising media (typically a list of integers)
        incidence_matrix: 2D list where incidence_matrix[t][m] indicates if audience t is covered by media m
        media_costs: List of costs associated with each advertising media

    Returns:
        min_total_cost: Minimum total cost of selected media that covers all audiences
    """
    import gurobipy as gp
    from gurobipy import GRB

    # Initialize the model
    model = gp.Model("Media Selection")
    model.setParam('OutputFlag', 0)  # Suppress Gurobi output

    num_media = len(advertising_media)
    num_audiences = len(target_audiences)

    # Decision variables: x[m] indicates whether media m is selected (1) or not (0)
    x = model.addVars(num_media, vtype=GRB.BINARY, name="x")

    # Objective: Minimize total cost of selected media
    model.setObjective(gp.quicksum(media_costs[m] * x[m] for m in range(num_media)), GRB.MINIMIZE)

    # Constraints: Each audience must be covered by at least one selected media
    for t in range(num_audiences):
        model.addConstr(
            gp.quicksum(incidence_matrix[t][m] * x[m] for m in range(num_media)) >= 1,
            name=f"CoverAudience_{t}"
        )

    # Optimize the model
    model.optimize()

    # Retrieve the minimum total cost
    min_total_cost = model.objVal

    return min_total_cost
