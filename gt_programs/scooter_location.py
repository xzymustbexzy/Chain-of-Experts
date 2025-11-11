from pulp import *

def scooter_location(estimated_demand, distance_matrix, num_available_scooters, max_selected_locations, new_max):
    num_demand_points = len(estimated_demand)
    num_candidate_locations = len(distance_matrix[0])

    problem = LpProblem("Scooter Distribution", LpMinimize)

    # Decision Variables
    assign_matrix = [[LpVariable(f'assign_{i}_{j}', 0, 1, LpInteger) for j in range(num_candidate_locations)] for i in range(num_demand_points)]
    selected_location = [LpVariable(f'selected_{j}', 0, 1, LpInteger) for j in range(num_candidate_locations)]
    new_scooters = LpVariable("new_scooters", lowBound=0, upBound=new_max)

    # Objective
    problem += lpSum(estimated_demand[i] * distance_matrix[i][j] * assign_matrix[i][j] for i in range(num_demand_points) for j in range(num_candidate_locations))

    # Constraints
    for i in range(num_demand_points):
        for j in range(num_candidate_locations):
            problem += assign_matrix[i][j] <= selected_location[j]

    for i in range(num_demand_points):
        problem += lpSum(assign_matrix[i][j] for j in range(num_candidate_locations)) <= 1

    problem += lpSum(estimated_demand[i] * assign_matrix[i][j] for i in range(num_demand_points) for j in range(num_candidate_locations)) == num_available_scooters + new_scooters

    problem += lpSum(selected_location[j] for j in range(num_candidate_locations)) <= max_selected_locations

    # Solve
    problem.solve()

    min_total_distance = value(problem.objective)

    return min_total_distance