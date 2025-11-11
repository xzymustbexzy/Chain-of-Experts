import cvxpy as cp
import numpy as np

def blend_problem(alloys_on_market, required_elements, composition_data, desired_blend_percentage, alloy_price):
    """
    Solve the alloy blending problem to achieve the desired blend at minimum cost.

    Args:
        alloys_on_market: list of integers, IDs of available alloys on the market
        required_elements: list of strings, IDs of required elements
        composition_data: 2D list of floats, percentage of each required element in each alloy
        desired_blend_percentage: list of floats, desired blend percentage for each element
        alloy_price: list of floats, price of each alloy

    Returns:
        min_cost: a float, minimum total cost to achieve the desired blend
        alloy_purchased: np.array, the amount of each alloy to purchase
    """
    # Number of alloys and required elements
    num_alloys = len(alloys_on_market)
    num_elements = len(required_elements)
    
    # Convert lists to numpy arrays for matrix operations
    composition_data = np.array(composition_data)
    desired_blend_percentage = np.array(desired_blend_percentage)
    alloy_price = np.array(alloy_price)
    
    # Define the decision variable (amount of each alloy to purchase)
    AlloyPurchased = cp.Variable(num_alloys)
    
    # The objective is to minimize the total cost of the purchased alloys
    cost = alloy_price @ AlloyPurchased  # @ operator is used for matrix multiplication in numpy
    objective = cp.Minimize(cost)
    
    # Constraints
    constraints = []

    # Constraint to ensure that the desired blend percentage of each required element is met
    for e in range(num_elements):
        constraints.append(composition_data[e, :] @ AlloyPurchased == desired_blend_percentage[e])
    
    # Constraint to ensure that the total amount of alloys purchased is equal to 1
    constraints.append(cp.sum(AlloyPurchased) == 1)

    # The AlloyPurchased should be non-negative
    constraints += [AlloyPurchased >= 0]
    
    # Solve the problem
    prob = cp.Problem(objective, constraints)
    prob.solve()
    
    # Check if the problem is feasible and has an optimal solution
    if prob.status not in ["infeasible", "unbounded"]:
        # Optimal solution found
        min_cost = prob.value
        alloy_purchased = AlloyPurchased.value
        print("The minimum cost is: ", min_cost)
        print("Amount of each alloy to purchase: ", alloy_purchased)
        return min_cost, alloy_purchased
    else:
        # Problem has no solution
        print("No solution exists for the blending problem with the provided data.")
        return None, None
