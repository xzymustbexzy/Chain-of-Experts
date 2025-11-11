# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
An individual consumes vegetables and fruits. A serving of vegetables contains
VegetableVitamins units of vitamins and VegetableMinerals units of minerals. A
serving of fruits contains FruitVitamins units of vitamins and FruitMinerals
units of minerals. The individual requires at least MinimumVitamins units of
vitamins and MinimumMinerals units of minerals. Vegetables cost VegetableCost
per serving and fruits cost FruitCost per serving. Determine the number of
servings of each to minimize total cost.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/36/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VegetableVitamins @Def: Amount of vitamins in one serving of vegetables @Shape: [] 
VegetableVitamins = data['VegetableVitamins']
# @Parameter VegetableMinerals @Def: Amount of minerals in one serving of vegetables @Shape: [] 
VegetableMinerals = data['VegetableMinerals']
# @Parameter FruitVitamins @Def: Amount of vitamins in one serving of fruits @Shape: [] 
FruitVitamins = data['FruitVitamins']
# @Parameter FruitMinerals @Def: Amount of minerals in one serving of fruits @Shape: [] 
FruitMinerals = data['FruitMinerals']
# @Parameter MinimumVitamins @Def: Minimum required units of vitamins @Shape: [] 
MinimumVitamins = data['MinimumVitamins']
# @Parameter MinimumMinerals @Def: Minimum required units of minerals @Shape: [] 
MinimumMinerals = data['MinimumMinerals']
# @Parameter VegetableCost @Def: Cost per serving of vegetables @Shape: [] 
VegetableCost = data['VegetableCost']
# @Parameter FruitCost @Def: Cost per serving of fruits @Shape: [] 
FruitCost = data['FruitCost']

# Variables 
# @Variable VegetableServings @Def: The number of servings of vegetables @Shape: [] 
VegetableServings = model.addVar(vtype=GRB.CONTINUOUS, name="VegetableServings")
# @Variable FruitServings @Def: The number of servings of fruits @Shape: [] 
FruitServings = model.addVar(vtype=GRB.CONTINUOUS, name="FruitServings")

# Constraints 
# @Constraint Constr_1 @Def: A serving of vegetables contains VegetableVitamins units of vitamins and a serving of fruits contains FruitVitamins units of vitamins. The individual requires at least MinimumVitamins units of vitamins.
model.addConstr(VegetableVitamins * VegetableServings + FruitVitamins * FruitServings >= MinimumVitamins)
# @Constraint Constr_2 @Def: A serving of vegetables contains VegetableMinerals units of minerals and a serving of fruits contains FruitMinerals units of minerals. The individual requires at least MinimumMinerals units of minerals.
model.addConstr(VegetableMinerals * VegetableServings + FruitMinerals * FruitServings >= MinimumMinerals)

# Objective 
# @Objective Objective @Def: Total cost is the sum of VegetableCost per serving of vegetables and FruitCost per serving of fruits. The objective is to minimize the total cost while meeting the minimum nutrient requirements.
model.setObjective(VegetableCost * VegetableServings + FruitCost * FruitServings, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['VegetableServings'] = VegetableServings.x
variables['FruitServings'] = FruitServings.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
