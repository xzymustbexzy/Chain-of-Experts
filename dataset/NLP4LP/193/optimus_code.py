# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A young boy aims to meet at least MinCalcium units of calcium and MinIron units
of iron per day by consuming milk and vegetables. Each serving of milk costs
MilkCost and contains MilkCalcium units of calcium and MilkIron units of iron.
Each serving of vegetables costs VegetableCost and contains VegetableCalcium
units of calcium and VegetableIron units of iron. The objective is to determine
the number of milk and vegetable servings to minimize the total cost.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/194/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinCalcium @Def: Minimum required units of calcium per day @Shape: [] 
MinCalcium = data['MinCalcium']
# @Parameter MinIron @Def: Minimum required units of iron per day @Shape: [] 
MinIron = data['MinIron']
# @Parameter MilkCost @Def: Cost of a glass of milk @Shape: [] 
MilkCost = data['MilkCost']
# @Parameter MilkCalcium @Def: Units of calcium in a glass of milk @Shape: [] 
MilkCalcium = data['MilkCalcium']
# @Parameter MilkIron @Def: Units of iron in a glass of milk @Shape: [] 
MilkIron = data['MilkIron']
# @Parameter VegetableCost @Def: Cost of a plate of vegetables @Shape: [] 
VegetableCost = data['VegetableCost']
# @Parameter VegetableCalcium @Def: Units of calcium in a plate of vegetables @Shape: [] 
VegetableCalcium = data['VegetableCalcium']
# @Parameter VegetableIron @Def: Units of iron in a plate of vegetables @Shape: [] 
VegetableIron = data['VegetableIron']

# Variables 
# @Variable MilkAmount @Def: The number of glasses of milk consumed per day @Shape: [] 
MilkAmount = model.addVar(vtype=GRB.CONTINUOUS, name="MilkAmount")
# @Variable VegetablesAmount @Def: The number of plates of vegetables consumed per day @Shape: [] 
VegetablesAmount = model.addVar(vtype=GRB.CONTINUOUS, name="VegetablesAmount")

# Constraints 
# @Constraint Constr_1 @Def: The total calcium obtained from milk and vegetables must be at least MinCalcium units per day.
model.addConstr(MilkCalcium * MilkAmount + VegetableCalcium * VegetablesAmount >= MinCalcium)
# @Constraint Constr_2 @Def: The total iron obtained from milk and vegetables must be at least MinIron units per day.
model.addConstr(MilkIron * MilkAmount + VegetableIron * VegetablesAmount >= MinIron, 'IronRequirement')
# @Constraint Constr_3 @Def: The number of milk servings and vegetable servings must be non-negative.
model.addConstr(MilkAmount >= 0, "MilkAmount_nonnegative")
model.addConstr(VegetablesAmount >= 0, "VegetablesAmount_nonnegative")

# Objective 
# @Objective Objective @Def: Minimize the total cost, which is the sum of the costs of milk servings and vegetable servings.
model.setObjective(MilkCost * MilkAmount + VegetableCost * VegetablesAmount, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['MilkAmount'] = MilkAmount.x
variables['VegetablesAmount'] = VegetablesAmount.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
