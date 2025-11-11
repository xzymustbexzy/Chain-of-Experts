# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A shipping company transports packages using trucks and cars. Each truck
transports TruckCapacity packages per trip and uses TruckGas liters of gas per
trip. Each car transports CarCapacity packages per trip and uses CarGas liters
of gas per trip. The number of truck trips is limited by MaxTruckTrips. At least
MinCarTripPercentage of all trips must be made by car. The company needs to
transport at least MinTotalPackages packages. The objective is to minimize the
total gas consumed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/181/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TruckCapacity @Def: Number of packages a truck can transport per trip @Shape: [] 
TruckCapacity = data['TruckCapacity']
# @Parameter CarCapacity @Def: Number of packages a car can transport per trip @Shape: [] 
CarCapacity = data['CarCapacity']
# @Parameter TruckGas @Def: Liters of gas a truck uses per trip @Shape: [] 
TruckGas = data['TruckGas']
# @Parameter CarGas @Def: Liters of gas a car uses per trip @Shape: [] 
CarGas = data['CarGas']
# @Parameter MaxTruckTrips @Def: Maximum number of truck trips allowed @Shape: [] 
MaxTruckTrips = data['MaxTruckTrips']
# @Parameter MinCarTripPercentage @Def: Minimum percentage of trips that must be made by car @Shape: [] 
MinCarTripPercentage = data['MinCarTripPercentage']
# @Parameter MinTotalPackages @Def: Minimum number of packages to transport @Shape: [] 
MinTotalPackages = data['MinTotalPackages']

# Variables 
# @Variable TruckTrips @Def: The number of truck trips @Shape: ['Integer'] 
TruckTrips = model.addVar(vtype=GRB.INTEGER, name="TruckTrips", ub=MaxTruckTrips)
# @Variable CarTrips @Def: The number of car trips @Shape: ['Integer'] 
CarTrips = model.addVar(vtype=GRB.INTEGER, name="CarTrips")

# Constraints 
# @Constraint Constr_1 @Def: The number of truck trips cannot exceed MaxTruckTrips.
model.addConstr(TruckTrips <= MaxTruckTrips)
# @Constraint Constr_2 @Def: At least MinCarTripPercentage of all trips must be made by car.
model.addConstr((1 - MinCarTripPercentage) * CarTrips >= MinCarTripPercentage * TruckTrips)
# @Constraint Constr_3 @Def: At least MinTotalPackages packages must be transported.
model.addConstr(TruckTrips * TruckCapacity + CarTrips * CarCapacity >= MinTotalPackages, "MinTotalPackagesConstr")

# Objective 
# @Objective Objective @Def: Total gas consumed is the sum of gas used by trucks and cars per trip. The objective is to minimize the total gas consumed.
model.setObjective(TruckGas * TruckTrips + CarGas * CarTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['TruckTrips'] = TruckTrips.x
variables['CarTrips'] = CarTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
