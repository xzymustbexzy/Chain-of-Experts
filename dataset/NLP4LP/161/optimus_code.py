# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A farmer needs to transport TotalChickens chickens using buses and cars. Each
bus trip can carry BusCapacity chickens and takes BusTripTime hours. Each car
trip can carry CarCapacity chickens and takes CarTripTime hours. The number of
bus trips cannot exceed MaxBusTrips. At least MinCarTripPercentage of the total
trips must be by car. The objective is to minimize the total transportation
time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/162/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter BusCapacity @Def: Number of chickens that a bus can carry per trip @Shape: [] 
BusCapacity = data['BusCapacity']
# @Parameter BusTripTime @Def: Time taken by a bus per trip in hours @Shape: [] 
BusTripTime = data['BusTripTime']
# @Parameter CarCapacity @Def: Number of chickens that a car can carry per trip @Shape: [] 
CarCapacity = data['CarCapacity']
# @Parameter CarTripTime @Def: Time taken by a car per trip in hours @Shape: [] 
CarTripTime = data['CarTripTime']
# @Parameter MaxBusTrips @Def: Maximum allowed number of bus trips @Shape: [] 
MaxBusTrips = data['MaxBusTrips']
# @Parameter MinCarTripPercentage @Def: Minimum required percentage of total trips that must be by car @Shape: [] 
MinCarTripPercentage = data['MinCarTripPercentage']
# @Parameter TotalChickens @Def: Total number of chickens that need to be transported @Shape: [] 
TotalChickens = data['TotalChickens']

# Variables 
# @Variable NumberOfBusTrips @Def: The number of bus trips @Shape: [] 
NumberOfBusTrips = model.addVar(vtype=GRB.INTEGER, name="NumberOfBusTrips")
# @Variable NumberOfCarTrips @Def: The number of car trips @Shape: [] 
NumberOfCarTrips = model.addVar(vtype=GRB.INTEGER, name="NumberOfCarTrips")

# Constraints 
# @Constraint Constr_1 @Def: The number of bus trips cannot exceed MaxBusTrips.
model.addConstr(NumberOfBusTrips <= MaxBusTrips)
# @Constraint Constr_2 @Def: At least MinCarTripPercentage of the total trips must be by car.
model.addConstr(NumberOfCarTrips >= MinCarTripPercentage * (NumberOfCarTrips + NumberOfBusTrips))
# @Constraint Constr_3 @Def: The total number of chickens transported by buses and cars must be at least TotalChickens.
model.addConstr(NumberOfBusTrips * BusCapacity + NumberOfCarTrips * CarCapacity >= TotalChickens)

# Objective 
# @Objective Objective @Def: The total transportation time is the sum of the times of all bus and car trips. The objective is to minimize the total transportation time.
model.setObjective(NumberOfBusTrips * BusTripTime + NumberOfCarTrips * CarTripTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfBusTrips'] = NumberOfBusTrips.x
variables['NumberOfCarTrips'] = NumberOfCarTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
