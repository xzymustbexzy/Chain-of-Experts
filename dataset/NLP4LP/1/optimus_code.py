# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A breakfast joint produces NumSandwichTypes different types of sandwiches using
NumIngredients different ingredients. The amount of each ingredient required for
each sandwich type is specified by Required. The total availability of each
ingredient is given by TotalAvailable. The profit earned per unit of each
sandwich type is defined by ProfitPerSandwich. The objective is to determine the
number of each sandwich type to produce in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/2/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumSandwichTypes @Def: Number of different sandwich types @Shape: [] 
NumSandwichTypes = data['NumSandwichTypes']
# @Parameter NumIngredients @Def: Number of different ingredients @Shape: [] 
NumIngredients = data['NumIngredients']
# @Parameter Required @Def: Amount of ingredient j required to produce one unit of sandwich i @Shape: ['NumIngredients', 'NumSandwichTypes'] 
Required = data['Required']
# @Parameter TotalAvailable @Def: Total availability of ingredient j @Shape: ['NumIngredients'] 
TotalAvailable = data['TotalAvailable']
# @Parameter ProfitPerSandwich @Def: Profit per unit of sandwich i @Shape: ['NumSandwichTypes'] 
ProfitPerSandwich = data['ProfitPerSandwich']

# Variables 
# @Variable NumSandwiches @Def: The number of sandwiches to produce for each sandwich type @Shape: ['NumSandwichTypes'] 
NumSandwiches = model.addVars(NumSandwichTypes, vtype=GRB.CONTINUOUS, name="NumSandwiches")

# Constraints 
# @Constraint Constr_1 @Def: The total usage of eggs for producing regular and special sandwiches does not exceed the total available eggs.
model.addConstr(quicksum(Required[0][i] * NumSandwiches[i] for i in range(NumSandwichTypes)) <= TotalAvailable[0], "Constr_1")
# @Constraint Constr_2 @Def: The total usage of bacon for producing regular and special sandwiches does not exceed the total available bacon.
model.addConstr(quicksum(Required[1][i] * NumSandwiches[i] for i in range(NumSandwichTypes)) <= TotalAvailable[1], "Constr_2")
# @Constraint Constr_3 @Def: The number of regular and special sandwiches produced is non-negative.
model.addConstrs((NumSandwiches[i] >= 0 for i in range(NumSandwichTypes)), 'NumSandwichesNonNegative')

# Objective 
# @Objective Objective @Def: The total profit is the sum of the profit per sandwich type multiplied by the number of sandwiches produced. The objective is to maximize the total profit.
model.setObjective(quicksum(NumSandwiches[i] * ProfitPerSandwich[i] for i in range(NumSandwichTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumSandwiches'] = {i: NumSandwiches[i].X for i in range(NumSandwichTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
