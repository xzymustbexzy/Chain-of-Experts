# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A bakery manufactures NumProducts distinct products, each yielding a specific
Profit per batch. Each product requires a certain amount of time from each of
the NumResources resource types for production. The bakery has a limited amount
of time available for each resource, defined by ResourceAvailability. The goal
is to maximize the total Profit by fully utilizing the available Resource
capacities.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/37/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumProducts @Def: Number of products baked @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter NumResources @Def: Number of resource types @Shape: [] 
NumResources = data['NumResources']
# @Parameter Profit @Def: Profit per batch of each product @Shape: ['NumProducts'] 
Profit = data['Profit']
# @Parameter ResourceTime @Def: Time required per batch of each product for each resource @Shape: ['NumResources', 'NumProducts'] 
ResourceTime = data['ResourceTime']
# @Parameter ResourceAvailability @Def: Total available time per resource @Shape: ['NumResources'] 
ResourceAvailability = data['ResourceAvailability']

# Variables 
# @Variable Batch @Def: The number of batches for each product @Shape: ['NumProducts'] 
Batch = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="Batch")

# Constraints 
# @Constraint Constr_1 @Def: For each resource type, the total time required by all product batches does not exceed the ResourceAvailability.
model.addConstrs((quicksum(ResourceTime[r][p] * Batch[p] for p in range(NumProducts)) <= ResourceAvailability[r] for r in range(NumResources)), name="ResourceLimit")

# Objective 
# @Objective Objective @Def: Total Profit is the sum of the profit per batch of each product multiplied by the number of batches produced. The objective is to maximize the total Profit.
model.setObjective(quicksum(Profit[i] * Batch[i] for i in range(NumProducts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Batch'] = {p: Batch[p].x for p in Batch}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
