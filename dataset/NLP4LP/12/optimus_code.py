# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A souvenir shop produces NumProducts different products using NumResources
different resources. Each product has a profit defined by Profit and requires
specific amounts of resources as specified by ResourceRequirement. The
ResourceAvailability defines the total amount of each resource available. The
objective is to determine the number of each product to produce to maximize
total Profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/13/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProducts @Def: Number of different products produced @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter NumResources @Def: Number of different resources used @Shape: [] 
NumResources = data['NumResources']
# @Parameter Profit @Def: Profit per unit of each product @Shape: ['NumProducts'] 
Profit = data['Profit']
# @Parameter ResourceRequirement @Def: Amount of each resource required to produce one unit of each product @Shape: ['NumResources', 'NumProducts'] 
ResourceRequirement = data['ResourceRequirement']
# @Parameter ResourceAvailability @Def: Amount of each resource available per week @Shape: ['NumResources'] 
ResourceAvailability = data['ResourceAvailability']
    
# Variables 
# @Variable Production @Def: The quantity produced for each product @Shape: ['NumProducts'] 
Production = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="Production")
    
# Constraints 
# @Constraint Constr_1 @Def: The total amount of wood required to produce all products does not exceed the available wood.
model.addConstr(quicksum(ResourceRequirement[0][j] * Production[j] for j in range(NumProducts)) <= ResourceAvailability[0], name="Constr_1")
# @Constraint Constr_2 @Def: The total amount of plastic required to produce all products does not exceed the available plastic.
model.addConstr(quicksum(ResourceRequirement[1][j] * Production[j] for j in range(NumProducts)) <= ResourceAvailability[1], name="Constr_2")
    
# Objective 
# @Objective Objective @Def: Total Profit is the sum of the profit per unit of each product multiplied by the number of each product produced. The objective is to maximize the total Profit.
model.setObjective(quicksum(Profit[i] * Production[i] for i in range(NumProducts)), GRB.MAXIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['Production'] = {j: Production[j].x for j in range(NumProducts)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
