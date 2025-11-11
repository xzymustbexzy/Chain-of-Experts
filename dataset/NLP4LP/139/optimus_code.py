# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A bee farmer transports his honey in small and large bottles, where a small
bottle has a capacity of SmallBottleCapacity units of honey and a large bottle
has a capacity of LargeBottleCapacity units of honey. The farmer has available
at most MaxSmallBottles small bottles and at most MaxLargeBottles large bottles.
Additionally, the number of small bottles used must be at least
MinRatioSmallToLarge times the number of large bottles used. The total number of
bottles transported must not exceed MaxTotalBottles, and at least
MinLargeBottles large bottles must be used. The farmer aims to maximize the
total amount of honey transported.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/140/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallBottleCapacity @Def: Capacity of a small bottle in units of honey @Shape: [] 
SmallBottleCapacity = data['SmallBottleCapacity']
# @Parameter LargeBottleCapacity @Def: Capacity of a large bottle in units of honey @Shape: [] 
LargeBottleCapacity = data['LargeBottleCapacity']
# @Parameter MaxSmallBottles @Def: Maximum number of small bottles available @Shape: [] 
MaxSmallBottles = data['MaxSmallBottles']
# @Parameter MaxLargeBottles @Def: Maximum number of large bottles available @Shape: [] 
MaxLargeBottles = data['MaxLargeBottles']
# @Parameter MinRatioSmallToLarge @Def: Minimum ratio of small bottles to large bottles @Shape: [] 
MinRatioSmallToLarge = data['MinRatioSmallToLarge']
# @Parameter MaxTotalBottles @Def: Maximum total number of bottles that can be transported @Shape: [] 
MaxTotalBottles = data['MaxTotalBottles']
# @Parameter MinLargeBottles @Def: Minimum number of large bottles that must be used @Shape: [] 
MinLargeBottles = data['MinLargeBottles']

# Variables 
# @Variable SmallBottlesUsed @Def: The number of small bottles used @Shape: [] 
SmallBottlesUsed = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxSmallBottles, name="SmallBottlesUsed")
# @Variable LargeBottlesUsed @Def: The number of large bottles used @Shape: [] 
LargeBottlesUsed = model.addVar(vtype=GRB.INTEGER, lb=MinLargeBottles, ub=MaxLargeBottles, name="LargeBottlesUsed")

# Constraints 
# @Constraint Constr_1 @Def: The number of small bottles used must be at least MinRatioSmallToLarge times the number of large bottles used.
model.addConstr(SmallBottlesUsed >= MinRatioSmallToLarge * LargeBottlesUsed)
# @Constraint Constr_2 @Def: The total number of bottles transported must not exceed MaxTotalBottles.
model.addConstr(SmallBottlesUsed + LargeBottlesUsed <= MaxTotalBottles)
# @Constraint Constr_3 @Def: At least MinLargeBottles large bottles must be used.
model.addConstr(LargeBottlesUsed >= MinLargeBottles)
# @Constraint Constr_4 @Def: The number of small bottles used must not exceed MaxSmallBottles.
model.addConstr(SmallBottlesUsed <= MaxSmallBottles)
# @Constraint Constr_5 @Def: The number of large bottles used must not exceed MaxLargeBottles.
model.addConstr(LargeBottlesUsed <= MaxLargeBottles)

# Objective 
# @Objective Objective @Def: Maximize the total amount of honey transported, which is the sum of (SmallBottleCapacity × number of small bottles) and (LargeBottleCapacity × number of large bottles).
model.setObjective(SmallBottleCapacity * SmallBottlesUsed + LargeBottleCapacity * LargeBottlesUsed, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallBottlesUsed'] = SmallBottlesUsed.x
variables['LargeBottlesUsed'] = LargeBottlesUsed.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
