def knapsack_optimization(item_values, item_weights, max_weight_knapsack):
    """
    Args:
        item_values: a list of integers, indicating the value of each item
        item_weights: a list of integers, indicating the weight of each item
        max_weight_knapsack: an integer, denotes the maximum weight capacity of the knapsack

    Returns:
        max_total_value: an integer, denotes the maximum total value of the items in the knapsack
    """
    num_items = len(item_values)
    dp = [[0] * (max_weight_knapsack + 1) for _ in range(num_items + 1)]

    for i in range(1, num_items + 1):
        for w in range(1, max_weight_knapsack + 1):
            if item_weights[i - 1] <= w:
                dp[i][w] = max(item_values[i - 1] + dp[i - 1][w - item_weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    max_total_value = dp[num_items][max_weight_knapsack]
    return max_total_value