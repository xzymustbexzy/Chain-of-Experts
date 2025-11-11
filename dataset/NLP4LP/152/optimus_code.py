# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A farmer needs to transport TotalCows cows using helicopters and trucks. Each
helicopter trip can transport HelicopterCapacity cows and produces
HelicopterPollution units of pollution. Each truck trip can transport
TruckCapacity cows and produces TruckPollution units of pollution. Due to budget
constraints, at most MaxTruckTrips truck trips can be made. The objective is to
minimize the total pollution produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/153/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalCows @Def: The total number of cows that need to be transported @Shape: [] 
TotalCows = data['TotalCows']
# @Parameter HelicopterCapacity @Def: The number of cows that a helicopter can transport per trip @Shape: [] 
HelicopterCapacity = data['HelicopterCapacity']
# @Parameter HelicopterPollution @Def: The amount of pollution created by a helicopter per trip @Shape: [] 
HelicopterPollution = data['HelicopterPollution']
# @Parameter TruckCapacity @Def: The number of cows that a truck can transport per trip @Shape: [] 
TruckCapacity = data['TruckCapacity']
# @Parameter TruckPollution @Def: The amount of pollution created by a truck per trip @Shape: [] 
TruckPollution = data['TruckPollution']
# @Parameter MaxTruckTrips @Def: The maximum number of truck trips that can be made due to budget constraints @Shape: [] 
MaxTruckTrips = data['MaxTruckTrips']

# Variables 
# @Variable NumHelicopterTrips @Def: The number of trips made by helicopters @Shape: [] 
NumHelicopterTrips = model.addVar(vtype=GRB.INTEGER, name="NumHelicopterTrips")
# @Variable NumTruckTrips @Def: The number of trips made by trucks @Shape: [] 
NumTruckTrips = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxTruckTrips, name="NumTruckTrips")

# Constraints 
# @Constraint Constr_1 @Def: The total number of cows transported by helicopters and trucks must equal TotalCows.
model.addConstr(HelicopterCapacity * NumHelicopterTrips + TruckCapacity * NumTruckTrips == TotalCows)
# @Constraint Constr_2 @Def: At most MaxTruckTrips truck trips can be made.
model.addConstr(NumTruckTrips <= MaxTruckTrips)

# Objective 
# @Objective Objective @Def: Total pollution is the sum of the pollution from helicopter trips and truck trips. The objective is to minimize the total pollution produced.
model.setObjective(HelicopterPollution * NumHelicopterTrips + TruckPollution * NumTruckTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumHelicopterTrips'] = NumHelicopterTrips.x
variables['NumTruckTrips'] = NumTruckTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
