# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A zoo needs to transport TotalMonkeys monkeys to the vet using buses and cars.
Each bus can carry BusCapacity monkeys per trip and takes BusTripTime minutes
per trip. Each car can carry CarCapacity monkeys per trip and takes CarTripTime
minutes per trip. The number of bus trips cannot exceed MaxBusTrips.
Additionally, at least MinCarTripFraction of all trips must be by car. The
objective is to determine the number of bus and car trips that minimize the
total transportation time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/152/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalMonkeys @Def: Number of monkeys to transport @Shape: [] 
TotalMonkeys = data['TotalMonkeys']
# @Parameter BusCapacity @Def: Number of monkeys a bus can transport per trip @Shape: [] 
BusCapacity = data['BusCapacity']
# @Parameter BusTripTime @Def: Time in minutes a bus takes per trip @Shape: [] 
BusTripTime = data['BusTripTime']
# @Parameter CarCapacity @Def: Number of monkeys a car can transport per trip @Shape: [] 
CarCapacity = data['CarCapacity']
# @Parameter CarTripTime @Def: Time in minutes a car takes per trip @Shape: [] 
CarTripTime = data['CarTripTime']
# @Parameter MaxBusTrips @Def: Maximum number of bus trips allowed @Shape: [] 
MaxBusTrips = data['MaxBusTrips']
# @Parameter MinCarTripFraction @Def: Minimum fraction of trips that must be by car @Shape: [] 
MinCarTripFraction = data['MinCarTripFraction']

# Variables 
# @Variable BusTrips @Def: The number of bus trips @Shape: [] 
BusTrips = model.addVar(vtype=GRB.INTEGER, name="BusTrips")
# @Variable CarTrips @Def: The number of car trips @Shape: [] 
CarTrips = model.addVar(vtype=GRB.INTEGER, name="CarTrips")

# Constraints 
# @Constraint Constr_1 @Def: The number of bus trips cannot exceed MaxBusTrips.
model.addConstr(BusTrips <= MaxBusTrips)
# @Constraint Constr_2 @Def: At least MinCarTripFraction of all trips must be by car.
model.addConstr(CarTrips >= MinCarTripFraction * (CarTrips + BusTrips))
# @Constraint Constr_3 @Def: The total number of monkeys transported by buses and cars must equal TotalMonkeys.
model.addConstr(BusTrips * BusCapacity + CarTrips * CarCapacity == TotalMonkeys)

# Objective 
# @Objective Objective @Def: The total transportation time is the sum of the time taken by all bus trips and car trips. The objective is to minimize the total transportation time.
model.setObjective(BusTrips * BusTripTime + CarTrips * CarTripTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['BusTrips'] = BusTrips.x
variables['CarTrips'] = CarTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
