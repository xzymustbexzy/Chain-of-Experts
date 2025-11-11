# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company produces NumProducts different products using NumResources different
resources. Each product requires specific amounts of resources as defined by
ResourceRequired. The TotalAvailableResources limit the total usage of each
resource. The production of one product must exceed the production of another
product. Additionally, the production of a specific product is limited by
MaxLiquidSanitizers. Each product can clean a certain number of hands as
specified by CleaningPerUnit. The company aims to determine the number of each
product to produce in order to maximize the total number of hands cleaned.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/118/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProducts @Def: Number of different products @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter NumResources @Def: Number of different resources @Shape: [] 
NumResources = data['NumResources']
# @Parameter ResourceRequired @Def: Amount of each resource required to produce one unit of each product @Shape: ['NumResources', 'NumProducts'] 
ResourceRequired = data['ResourceRequired']
# @Parameter TotalAvailableResources @Def: Total available units of each resource @Shape: ['NumResources'] 
TotalAvailableResources = data['TotalAvailableResources']
# @Parameter MaxLiquidSanitizers @Def: Maximum number of liquid hand sanitizers that can be produced @Shape: [] 
MaxLiquidSanitizers = data['MaxLiquidSanitizers']
# @Parameter CleaningPerUnit @Def: Number of hands cleaned by each unit of each product @Shape: ['NumProducts'] 
CleaningPerUnit = data['CleaningPerUnit']

# Variables 
# @Variable Production @Def: The number of units produced for each product @Shape: ['NumProducts'] 
Production = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="Production")

# Constraints 
# @Constraint Constr_1 @Def: Each product requires specific amounts of resources, and the total usage of each resource cannot exceed the TotalAvailableResources.
model.addConstrs((quicksum(ResourceRequired[r][p] * Production[p] for p in range(NumProducts)) <= TotalAvailableResources[r] for r in range(NumResources)), name="ResourceUsage")

# Define indices for Constr_2 and Constr_3
i = 0  # Index of the first product
j = 1  # Index of the second product

# @Constraint Constr_2 @Def: The production of one product must exceed the production of another product.
model.addConstr(Production[i] >= Production[j], "Production_geq_{}_{}".format(i, j))
# @Constraint Constr_3 @Def: The production of a specific product cannot exceed MaxLiquidSanitizers.
model.addConstr(Production[j] <= MaxLiquidSanitizers, "MaxLiquidSanitizers_constr")

# Objective 
# @Objective Objective @Def: Maximize the total number of hands cleaned, calculated as the sum of the number of each product produced multiplied by CleaningPerUnit.
model.setObjective(quicksum(Production[p] * CleaningPerUnit[p] for p in range(NumProducts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Production'] = [Production[p].x for p in range(NumProducts)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
