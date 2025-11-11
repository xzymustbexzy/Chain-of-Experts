import pulp

def media_selection(target_audiences, advertising_media, incidence_matrix, media_costs):
    model = pulp.LpProblem("MediaSelection", pulp.LpMinimize)

    advertising_vars = pulp.LpVariable.dicts("IsSelectedMIP", 
                                               (i for i in advertising_media), 
                                               cat="Binary")

    # Objective Function: Minimize total cost
    model += pulp.lpSum([advertising_vars[i]*media_costs[i] for i in advertising_media])

    # Constraints: At least one media should cover each target audience
    for t in target_audiences:
        model += pulp.lpSum([advertising_vars[i]*incidence_matrix[t][i] for i in advertising_media]) >= 1

    # Solve Model
    model.solve()

    status = pulp.LpStatus[model.status]
    
    if status != "Optimal":
        return "The problem does not have an optimal solution."
    else:
        min_total_cost = pulp.value(model.objective)

    return min_total_cost