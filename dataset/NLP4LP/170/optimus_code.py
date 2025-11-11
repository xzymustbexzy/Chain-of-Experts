# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A tropical city sends mail using submarines and boats. Each submarine can carry
SubmarineCapacity pieces of mail per trip and consumes SubmarineGasUsage liters
of gas per trip. Each boat can carry BoatCapacity pieces of mail per trip and
consumes BoatGasUsage liters of gas per trip. The number of submarine trips is
limited to MaxSubmarineTrips. At least MinBoatTripPercentage of all trips must
be by boat. The city needs to transport at least MailRequired pieces of mail.
The objective is to minimize the total gas usage.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/171/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SubmarineCapacity @Def: Number of pieces of mail a submarine can carry per trip @Shape: [] 
SubmarineCapacity = data['SubmarineCapacity']
# @Parameter SubmarineGasUsage @Def: Amount of gas a submarine uses per trip in liters @Shape: [] 
SubmarineGasUsage = data['SubmarineGasUsage']
# @Parameter BoatCapacity @Def: Number of pieces of mail a boat can carry per trip @Shape: [] 
BoatCapacity = data['BoatCapacity']
# @Parameter BoatGasUsage @Def: Amount of gas a boat uses per trip in liters @Shape: [] 
BoatGasUsage = data['BoatGasUsage']
# @Parameter MaxSubmarineTrips @Def: Maximum number of submarine trips allowed @Shape: [] 
MaxSubmarineTrips = data['MaxSubmarineTrips']
# @Parameter MinBoatTripPercentage @Def: Minimum percentage of trips that must be by boat @Shape: [] 
MinBoatTripPercentage = data['MinBoatTripPercentage']
# @Parameter MailRequired @Def: Minimum number of pieces of mail to transport @Shape: [] 
MailRequired = data['MailRequired']

# Variables 
# @Variable SubmarineTrips @Def: The number of submarine trips @Shape: [] 
SubmarineTrips = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxSubmarineTrips, name="SubmarineTrips")
# @Variable BoatTrips @Def: The number of boat trips @Shape: [] 
BoatTrips = model.addVar(vtype=GRB.INTEGER, name='BoatTrips')

# Constraints 
# @Constraint Constr_1 @Def: The number of submarine trips cannot exceed MaxSubmarineTrips.
model.addConstr(SubmarineTrips <= MaxSubmarineTrips)
# @Constraint Constr_2 @Def: At least MinBoatTripPercentage of all trips must be by boat.
model.addConstr(BoatTrips >= MinBoatTripPercentage * (BoatTrips + SubmarineTrips))
# @Constraint Constr_3 @Def: The total number of pieces of mail transported must be at least MailRequired.
model.addConstr(SubmarineTrips * SubmarineCapacity + BoatTrips * BoatCapacity >= MailRequired)

# Objective 
# @Objective Objective @Def: Minimize the total gas usage, calculated as the sum of gas consumed by all submarine and boat trips.
model.setObjective(SubmarineGasUsage * SubmarineTrips + BoatGasUsage * BoatTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SubmarineTrips'] = SubmarineTrips.x
variables['BoatTrips'] = BoatTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
