import pulp

def revenue_maximization(available_seats, demand, revenue, delta):
    prob = pulp.LpProblem("Flight_Revenue_Maximization", pulp.LpMaximize)

    num_flight_legs = len(available_seats)
    num_packages = len(demand)

    Sell = pulp.LpVariable.dicts("Sell", (i for i in range(num_packages)), lowBound=0, cat='Integer')

    revenue_contributions = [revenue[i] * Sell[i] for i in range(num_packages)]
    prob += pulp.lpSum(revenue_contributions)

    for p in range(num_packages):
        prob += Sell[p] <= demand[p], f"Demand_Constraint_{p}"
    
    for r in range(num_flight_legs):
        prob += pulp.lpSum(delta[p][r] * Sell[p] for p in range(num_packages)) <= available_seats[r], f"Seat_Availability_Constraint_{r}"

    prob.solve()

    if pulp.LpStatus[prob.status] == 'Optimal':
        max_revenue = pulp.value(prob.objective)
        sell_counts = [pulp.value(Sell[i]) for i in range(num_packages)]
        return max_revenue, sell_counts
    else:
        raise Exception("No optimal solution found")
