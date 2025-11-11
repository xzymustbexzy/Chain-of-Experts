# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A manufacturer uses large and small planes to ship their cars. Each large plane
can carry CapacityLarge cars and each small plane can carry CapacitySmall cars.
The number of large planes must be less than the number of small planes. The
manufacturer wants to deliver at least MinCars cars. Find the minimum number of
planes required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/156/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CapacityLarge @Def: Number of cars a large plane can carry @Shape: [] 
CapacityLarge = data['CapacityLarge']
# @Parameter CapacitySmall @Def: Number of cars a small plane can carry @Shape: [] 
CapacitySmall = data['CapacitySmall']
# @Parameter MinCars @Def: Minimum number of cars to deliver @Shape: [] 
MinCars = data['MinCars']

# Variables 
# @Variable NumLargePlanes @Def: The number of large planes used @Shape: [] 
NumLargePlanes = model.addVar(vtype=GRB.INTEGER, name="NumLargePlanes")
# @Variable NumSmallPlanes @Def: The number of small planes used @Shape: [] 
NumSmallPlanes = model.addVar(vtype=GRB.INTEGER, name="NumSmallPlanes")

# Constraints 
# @Constraint Constr_1 @Def: Each large plane can carry CapacityLarge cars and each small plane can carry CapacitySmall cars. The total number of cars shipped must be at least MinCars.
model.addConstr(CapacityLarge * NumLargePlanes + CapacitySmall * NumSmallPlanes >= MinCars)
# @Constraint Constr_2 @Def: The number of large planes must be less than the number of small planes.
model.addConstr(NumLargePlanes <= NumSmallPlanes - 1)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of planes required to deliver at least MinCars cars.
model.setObjective(NumLargePlanes + NumSmallPlanes, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumLargePlanes'] = NumLargePlanes.x
variables['NumSmallPlanes'] = NumSmallPlanes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
