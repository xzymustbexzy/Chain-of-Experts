from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def vrptw(customers, demand, lower_time_window, upper_time_window, distance, service_time, vehicle_capacity, M):
    num_vehicles = len(customers)
    depot = 0
    
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(distance), num_vehicles, depot)
    
    # Create Routing Model.
    routing_model = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance[from_node][to_node]
    
    transit_callback_index = routing_model.RegisterTransitCallback(distance_callback)
    
    # Set the cost of travel.
    routing_model.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demand[from_node]
    demand_callback_index = routing_model.RegisterUnaryTransitCallback(demand_callback)
    routing_model.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        [vehicle_capacity] * num_vehicles,  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Add Time Window constraint.
    time = 'Time'
    routing_model.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        30,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing_model.GetDimensionOrDie(time)
    for customer_id in range(1, len(customers)):
        start = lower_time_window[customer_id]
        end = upper_time_window[customer_id]
        index = manager.NodeToIndex(customer_id)
        time_dimension.CumulVar(index).SetRange(start, end)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)
    
    # Solve the problem.
    solution = routing_model.SolveWithParameters(search_parameters)
    if solution:
        print_solution(manager, routing_model, solution)
    
    # Return the minimum total distance.
    min_total_distance = solution.ObjectiveValue()
    return min_total_distance

