from pulp import *

def cutting_stock(roll_width, widths, orders, num_patterns, num_rolls_width):
    """
    Solves the Cutting Stock Problem to minimize the number of raw rolls cut.
    
    Args:
    - roll_width: An integer, the width of the raw rolls.
    - widths: A list of integers, the set of widths to be cut.
    - orders: A list of integers, the number of orders for each width.
    - num_patterns: An integer, the number of different patterns.
    - num_rolls_width: A list of lists, where each inner list contains the number of rolls of a 
                       particular width in a given pattern.
    
    Returns:
    - min_rolls_cut: An integer, the minimum number of raw rolls cut.
    """
    
    # Create problem instance
    prob = LpProblem("Cutting_Stock_Problem", LpMinimize)
    
    # Decision variables
    Cut = [LpVariable('Cut_%d' % j, lowBound=0, cat='Integer') for j in range(num_patterns)]

    # Objective function - Minimize the total number of raw rolls cut
    prob += lpSum(Cut), "Total number of rolls cut"
    
    # Constraints
    # Each width i must meet its orders
    for i in range(len(widths)):
        prob += lpSum(num_rolls_width[j][i] * Cut[j] for j in range(num_patterns)) >= orders[i], \
                "Meet_orders_for_width_%d" % widths[i]
    
    # Width of rolls in each pattern j should not exceed the width of raw roll
    for j in range(num_patterns):
        prob += lpSum(widths[i] * num_rolls_width[j][i] for i in range(len(widths))) <= roll_width, \
                "Max_roll_width_for_pattern_%d" % j
            
    # Solve the problem
    prob.solve()
    
    # The status of the solution
    print("Status:", LpStatus[prob.status])
    
    # The optimized variable values
    min_rolls_cut = value(prob.objective)
    cutting_plan = [(j, Cut[j].varValue) for j in range(num_patterns)]

    # Return the minimum number of raw rolls required
    return min_rolls_cut, cutting_plan
