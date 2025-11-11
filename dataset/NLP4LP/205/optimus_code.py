# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A bakery has BatterAvailable grams of batter and MilkAvailable grams of milk to
produce NumProducts different products. Each product requires a specific amount
of batter as defined by BatterPerProduct and a specific amount of milk as
defined by MilkPerProduct. The profit earned from each product is given by
ProfitPerProduct. The bakery aims to determine the number of each product to
produce in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/206/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter BatterAvailable @Def: Total amount of batter available (in grams) @Shape: [] 
BatterAvailable = data['BatterAvailable']
# @Parameter MilkAvailable @Def: Total amount of milk available (in grams) @Shape: [] 
MilkAvailable = data['MilkAvailable']
# @Parameter NumProducts @Def: Number of different products @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter BatterPerProduct @Def: Amount of batter required to produce one unit of each product @Shape: ['NumProducts'] 
BatterPerProduct = data['BatterPerProduct']
# @Parameter MilkPerProduct @Def: Amount of milk required to produce one unit of each product @Shape: ['NumProducts'] 
MilkPerProduct = data['MilkPerProduct']
# @Parameter ProfitPerProduct @Def: Profit per unit of each product @Shape: ['NumProducts'] 
ProfitPerProduct = data['ProfitPerProduct']

# Variables 
# @Variable UnitsToProduce @Def: The number of units to produce for each product @Shape: ['NumProducts'] 
UnitsToProduce = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="UnitsToProduce")

# Constraints 
# @Constraint Constr_1 @Def: The total batter used to produce all products cannot exceed BatterAvailable grams.
model.addConstr(quicksum(BatterPerProduct[i] * UnitsToProduce[i] for i in range(NumProducts)) <= BatterAvailable)
# @Constraint Constr_2 @Def: The total milk used to produce all products cannot exceed MilkAvailable grams.
model.addConstr(quicksum(MilkPerProduct[i] * UnitsToProduce[i] for i in range(NumProducts)) <= MilkAvailable)

# Objective 
# @Objective Objective @Def: Total profit is the sum of the profits from all products produced. The objective is to maximize the total profit.
model.setObjective(quicksum(UnitsToProduce[i] * ProfitPerProduct[i] for i in range(NumProducts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['UnitsToProduce'] = model.getAttr("X", UnitsToProduce)
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
