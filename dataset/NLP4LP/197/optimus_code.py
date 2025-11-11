# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A patient consumes NumSupplements different health supplements, each providing
various amounts of NumNutrients nutrients per serving. Each supplement has a
CostPerServing. The patient must consume enough supplements to meet the
MinimumRequirement for each nutrient. The objective is to determine the number
of servings of each supplement to minimize the total daily cost.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/198/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumSupplements @Def: Number of health supplements @Shape: [] 
NumSupplements = data['NumSupplements']
# @Parameter NumNutrients @Def: Number of nutrients @Shape: [] 
NumNutrients = data['NumNutrients']
# @Parameter AmountPerServing @Def: Amount of nutrient i per serving of supplement j @Shape: ['NumNutrients', 'NumSupplements'] 
AmountPerServing = data['AmountPerServing']
# @Parameter CostPerServing @Def: Cost per serving of supplement j @Shape: ['NumSupplements'] 
CostPerServing = data['CostPerServing']
# @Parameter MinimumRequirement @Def: Minimum required amount of nutrient i @Shape: ['NumNutrients'] 
MinimumRequirement = data['MinimumRequirement']

# Variables 
# @Variable Servings @Def: The number of servings for each supplement @Shape: ['NumSupplements'] 
Servings = model.addVars(NumSupplements, vtype=GRB.CONTINUOUS, name="Servings")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of Calcium obtained from the supplements must meet or exceed the minimum required.
model.addConstr(quicksum(AmountPerServing[0][j] * Servings[j] for j in range(NumSupplements)) >= MinimumRequirement[0])
# @Constraint Constr_2 @Def: The total amount of Magnesium obtained from the supplements must meet or exceed the minimum required.
model.addConstr(quicksum(AmountPerServing[1][j] * Servings[j] for j in range(NumSupplements)) >= MinimumRequirement[1])

# Objective 
# @Objective Objective @Def: Minimize the total daily cost of supplements while meeting the minimum requirements for Calcium and Magnesium.
model.setObjective(quicksum(CostPerServing[j] * Servings[j] for j in range(NumSupplements)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Servings'] = {j: Servings[j].X for j in range(NumSupplements)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)