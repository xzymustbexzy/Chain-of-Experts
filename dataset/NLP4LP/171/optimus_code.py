# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of helicopter trips and car trips to transport at least
MinFishToTransport fish. Each helicopter trip carries HelicopterCapacity fish
and takes HelicopterTime minutes, and each car trip carries CarCapacity fish and
takes CarTime minutes. The number of helicopter trips must not exceed
MaxHelicopterTrips, and at least MinPercentageCarTrips of all trips must be by
car. The objective is to minimize the total time required for all trips.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/172/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter HelicopterCapacity @Def: Number of fish a helicopter can transport per trip @Shape: [] 
HelicopterCapacity = data['HelicopterCapacity']
# @Parameter HelicopterTime @Def: Time a helicopter takes per trip in minutes @Shape: [] 
HelicopterTime = data['HelicopterTime']
# @Parameter CarCapacity @Def: Number of fish a car can transport per trip @Shape: [] 
CarCapacity = data['CarCapacity']
# @Parameter CarTime @Def: Time a car takes per trip in minutes @Shape: [] 
CarTime = data['CarTime']
# @Parameter MaxHelicopterTrips @Def: Maximum number of helicopter trips allowed @Shape: [] 
MaxHelicopterTrips = data['MaxHelicopterTrips']
# @Parameter MinPercentageCarTrips @Def: Minimum percentage of trips that must be by car @Shape: [] 
MinPercentageCarTrips = data['MinPercentageCarTrips']
# @Parameter MinFishToTransport @Def: Minimum number of fish to transport @Shape: [] 
MinFishToTransport = data['MinFishToTransport']

# Variables 
# @Variable HelicopterTrips @Def: Number of helicopter trips @Shape: [] 
HelicopterTrips = model.addVar(vtype=GRB.INTEGER, name="HelicopterTrips")
# @Variable CarTrips @Def: Number of car trips @Shape: [] 
CarTrips = model.addVar(vtype=GRB.INTEGER, name="CarTrips")

# Constraints 
# @Constraint Constr_1 @Def: The total number of fish transported by helicopters and cars must be at least MinFishToTransport.
model.addConstr(HelicopterCapacity * HelicopterTrips + CarCapacity * CarTrips >= MinFishToTransport)
# @Constraint Constr_2 @Def: The number of helicopter trips must not exceed MaxHelicopterTrips.
model.addConstr(HelicopterTrips <= MaxHelicopterTrips)
# @Constraint Constr_3 @Def: At least MinPercentageCarTrips of all trips must be by car.
model.addConstr(CarTrips >= MinPercentageCarTrips * (HelicopterTrips + CarTrips))

# Objective 
# @Objective Objective @Def: Minimize the total time required for all trips, calculated as the sum of the time taken by helicopter trips and car trips.
model.setObjective(HelicopterTrips * HelicopterTime + CarTrips * CarTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['HelicopterTrips'] = HelicopterTrips.x
variables['CarTrips'] = CarTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
