# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A mine transports TotalOre units of ore to the surface using small wagons with
capacity SmallWagonCapacity and large wagons with capacity LargeWagonCapacity.
The number of small wagons must be at least MinSmallToLargeRatio times the
number of large wagons. Additionally, at least MinLargeWagons large wagons must
be used. The objective is to minimize the total number of wagons required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/157/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallWagonCapacity @Def: Capacity of a small wagon in units of ore @Shape: [] 
SmallWagonCapacity = data['SmallWagonCapacity']
# @Parameter LargeWagonCapacity @Def: Capacity of a large wagon in units of ore @Shape: [] 
LargeWagonCapacity = data['LargeWagonCapacity']
# @Parameter MinSmallToLargeRatio @Def: Minimum ratio of small wagons to large wagons @Shape: [] 
MinSmallToLargeRatio = data['MinSmallToLargeRatio']
# @Parameter MinLargeWagons @Def: Minimum number of large wagons required @Shape: [] 
MinLargeWagons = data['MinLargeWagons']
# @Parameter TotalOre @Def: Total units of ore to be transported @Shape: [] 
TotalOre = data['TotalOre']

# Variables 
# @Variable SmallWagons @Def: The number of small wagons @Shape: [] 
SmallWagons = model.addVar(vtype=GRB.INTEGER, name="SmallWagons")
# @Variable LargeWagons @Def: The number of large wagons @Shape: [] 
LargeWagons = model.addVar(vtype=GRB.INTEGER, lb=MinLargeWagons, name="LargeWagons")

# Constraints 
# @Constraint Constr_1 @Def: The combined capacity of small and large wagons must be at least TotalOre units of ore.
model.addConstr(SmallWagons * SmallWagonCapacity + LargeWagons * LargeWagonCapacity >= TotalOre)
# @Constraint Constr_2 @Def: The number of small wagons must be at least MinSmallToLargeRatio times the number of large wagons.
model.addConstr(SmallWagons >= MinSmallToLargeRatio * LargeWagons)
# @Constraint Constr_3 @Def: At least MinLargeWagons large wagons must be used.
model.addConstr(LargeWagons >= MinLargeWagons)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of wagons required.
model.setObjective(SmallWagons + LargeWagons, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallWagons'] = SmallWagons.x
variables['LargeWagons'] = LargeWagons.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
