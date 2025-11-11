# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company can transport boxes using vans or trucks. Each van trip has a capacity
of VanCapacity boxes and costs VanCost dollars, while each truck trip has a
capacity of TruckCapacity boxes and costs TruckCost dollars. The company needs
to transport at least MinBoxes boxes with a total cost not exceeding Budget
dollars. Additionally, the number of van trips must be greater than the number
of truck trips. The objective is to minimize the total number of trips.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/139/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VanCapacity @Def: Capacity of a van in boxes per trip @Shape: [] 
VanCapacity = data['VanCapacity']
# @Parameter TruckCapacity @Def: Capacity of a truck in boxes per trip @Shape: [] 
TruckCapacity = data['TruckCapacity']
# @Parameter VanCost @Def: Cost per van trip in dollars @Shape: [] 
VanCost = data['VanCost']
# @Parameter TruckCost @Def: Cost per truck trip in dollars @Shape: [] 
TruckCost = data['TruckCost']
# @Parameter MinBoxes @Def: Minimum number of boxes to transport @Shape: [] 
MinBoxes = data['MinBoxes']
# @Parameter Budget @Def: Budget available in dollars @Shape: [] 
Budget = data['Budget']

# Variables 
# @Variable VanTrips @Def: The number of van trips @Shape: [] 
VanTrips = model.addVar(vtype=GRB.INTEGER, name="VanTrips")
# @Variable TruckTrips @Def: The number of truck trips @Shape: [] 
TruckTrips = model.addVar(vtype=GRB.INTEGER, name="TruckTrips")

# Constraints 
# @Constraint Constr_1 @Def: The total number of boxes transported using vans and trucks must be at least MinBoxes, where each van trip transports VanCapacity boxes and each truck trip transports TruckCapacity boxes.
model.addConstr(VanTrips * VanCapacity + TruckTrips * TruckCapacity >= MinBoxes)
# @Constraint Constr_2 @Def: The total transportation cost must not exceed Budget dollars, where each van trip costs VanCost dollars and each truck trip costs TruckCost dollars.
model.addConstr(VanCost * VanTrips + TruckCost * TruckTrips <= Budget)
# @Constraint Constr_3 @Def: The number of van trips must be greater than the number of truck trips.
model.addConstr(VanTrips >= TruckTrips + 1)

# Objective 
# @Objective Objective @Def: Minimize the total number of trips.
model.setObjective(VanTrips + TruckTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['VanTrips'] = VanTrips.x
variables['TruckTrips'] = TruckTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
