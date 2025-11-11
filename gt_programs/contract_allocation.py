from pulp import LpProblem, LpVariable, LpMinimize, LpStatus, lpSum, value

def contract_allocation(producers, contracts, available_capacity, production_cost, minimal_delivery, contract_size, minimal_number_of_contributors):
    model = LpProblem("Minimize contract allocation costs", LpMinimize)

    generation = LpVariable.dicts("generation", (producers, contracts), lowBound=0)
    generation_incidence = LpVariable.dicts("generation_incidence", (producers, contracts), cat='Binary')

    model += lpSum(production_cost[p][c] * generation[p][c] for p in producers for c in contracts)

    for p in producers:
        model += lpSum(generation[p][c] for c in contracts) <= available_capacity[p]
        for c in contracts:
            model += generation[p][c] >= minimal_delivery[p] * generation_incidence[p][c]

    for c in contracts:
        model += lpSum(generation[p][c] for p in producers) >= contract_size[c]
        model += lpSum(generation_incidence[p][c] for p in producers) >= minimal_number_of_contributors[c]

    model.solve()

    if LpStatus[model.status] == 'Optimal':
        total_cost = value(model.objective)
        return total_cost
    else:
        return None