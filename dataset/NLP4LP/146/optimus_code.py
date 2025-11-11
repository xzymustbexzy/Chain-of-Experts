# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An oil and gas company sends oil to the port using containers and trucks. Each
container can hold ContainerCapacity units of oil while each truck can hold
TruckCapacity units of oil. Due to government restrictions, the number of trucks
used must be at most TruckToContainerRatio multiplied by the number of
containers used. If at least MinimumOilSent units of oil need to be sent to the
port and at least MinimumContainers containers must be used, minimize the total
number of containers and trucks needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/147/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ContainerCapacity @Def: Number of units of oil each container can hold @Shape: [] 
ContainerCapacity = data['ContainerCapacity']
# @Parameter TruckCapacity @Def: Number of units of oil each truck can hold @Shape: [] 
TruckCapacity = data['TruckCapacity']
# @Parameter TruckToContainerRatio @Def: Maximum allowed ratio of number of trucks to number of containers @Shape: [] 
TruckToContainerRatio = data['TruckToContainerRatio']
# @Parameter MinimumOilSent @Def: Minimum number of units of oil that need to be sent to the port @Shape: [] 
MinimumOilSent = data['MinimumOilSent']
# @Parameter MinimumContainers @Def: Minimum number of containers that need to be used @Shape: [] 
MinimumContainers = data['MinimumContainers']

# Variables 
# @Variable NumContainers @Def: The number of containers used @Shape: [] 
NumContainers = model.addVar(vtype=GRB.INTEGER, name="NumContainers", lb=MinimumContainers)
# @Variable NumTrucks @Def: The number of trucks used @Shape: [] 
NumTrucks = model.addVar(vtype=GRB.INTEGER, name="NumTrucks")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of oil sent to the port must be at least 2000 units, calculated as 30 units per container plus 40 units per truck.
model.addConstr(ContainerCapacity * NumContainers + TruckCapacity * NumTrucks >= MinimumOilSent)
# @Constraint Constr_2 @Def: The number of trucks used must be at most half the number of containers used.
model.addConstr(NumTrucks <= TruckToContainerRatio * NumContainers)
# @Constraint Constr_3 @Def: At least 15 containers must be used.
model.addConstr(NumContainers >= MinimumContainers)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of containers and trucks needed.
model.setObjective(NumContainers + NumTrucks, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumContainers'] = NumContainers.x
variables['NumTrucks'] = NumTrucks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
