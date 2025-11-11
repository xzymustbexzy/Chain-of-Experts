# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A water salesman transports water using small and large kegs. Each small keg has
a capacity of SmallKegCapacity liters, while each large keg has a capacity of
LargeKegCapacity liters. The salesman can use at most MaxSmallKegsAvailable
small kegs and MaxLargeKegsAvailable large kegs. The number of small kegs used
must be at least SmallKegMultiplier times the number of large kegs used. The
total number of kegs transported cannot exceed MaxTotalKegs, and at least
MinLargeKegs large kegs must be used. Determine the number of small and large
kegs to maximize the total amount of water transported.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/170/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallKegCapacity @Def: Capacity of a small keg in liters @Shape: [] 
SmallKegCapacity = data['SmallKegCapacity']
# @Parameter LargeKegCapacity @Def: Capacity of a large keg in liters @Shape: [] 
LargeKegCapacity = data['LargeKegCapacity']
# @Parameter MaxSmallKegsAvailable @Def: Maximum number of small kegs available @Shape: [] 
MaxSmallKegsAvailable = data['MaxSmallKegsAvailable']
# @Parameter MaxLargeKegsAvailable @Def: Maximum number of large kegs available @Shape: [] 
MaxLargeKegsAvailable = data['MaxLargeKegsAvailable']
# @Parameter SmallKegMultiplier @Def: The multiplier for the number of small kegs to be used compared to large kegs @Shape: [] 
SmallKegMultiplier = data['SmallKegMultiplier']
# @Parameter MaxTotalKegs @Def: Maximum total number of kegs that can be transported @Shape: [] 
MaxTotalKegs = data['MaxTotalKegs']
# @Parameter MinLargeKegs @Def: Minimum number of large kegs that must be used @Shape: [] 
MinLargeKegs = data['MinLargeKegs']

# Variables 
# @Variable NumSmallKegsUsed @Def: The number of small kegs used @Shape: [] 
NumSmallKegsUsed = model.addVar(lb=0, ub=MaxSmallKegsAvailable, vtype=GRB.INTEGER, name="NumSmallKegsUsed")
# @Variable NumLargeKegsUsed @Def: The number of large kegs used @Shape: [] 
NumLargeKegsUsed = model.addVar(vtype=GRB.INTEGER, name="NumLargeKegsUsed")

# Constraints 
# @Constraint Constr_1 @Def: The number of small kegs used must not exceed MaxSmallKegsAvailable.
model.addConstr(NumSmallKegsUsed <= MaxSmallKegsAvailable)
# @Constraint Constr_2 @Def: The number of large kegs used must not exceed MaxLargeKegsAvailable.
model.addConstr(NumLargeKegsUsed <= MaxLargeKegsAvailable)
# @Constraint Constr_3 @Def: The number of small kegs used must be at least SmallKegMultiplier times the number of large kegs used.
model.addConstr(NumSmallKegsUsed >= SmallKegMultiplier * NumLargeKegsUsed)
# @Constraint Constr_4 @Def: The total number of kegs transported cannot exceed MaxTotalKegs.
model.addConstr(NumSmallKegsUsed + NumLargeKegsUsed <= MaxTotalKegs)
# @Constraint Constr_5 @Def: At least MinLargeKegs large kegs must be used.
model.addConstr(NumLargeKegsUsed >= MinLargeKegs)

# Objective 
# @Objective Objective @Def: Maximize the total amount of water transported, which is the sum of the capacities of the small and large kegs used.
model.setObjective(NumSmallKegsUsed * SmallKegCapacity + NumLargeKegsUsed * LargeKegCapacity, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumSmallKegsUsed'] = NumSmallKegsUsed.x
variables['NumLargeKegsUsed'] = NumLargeKegsUsed.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
