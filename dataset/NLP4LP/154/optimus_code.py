# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of bikes and scooters to maximize the total number of meals
delivered, where each bike holds BikeCapacity meals and requires BikeCharge
units of charge, and each scooter holds ScooterCapacity meals and requires
ScooterCharge units of charge. Ensure that the proportion of bikes does not
exceed MaxBikeFraction of all electric vehicles, at least MinScooters scooters
are used, and the total charge consumed by all vehicles does not exceed
TotalCharge units.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/155/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter BikeCapacity @Def: Number of meals a bike can hold @Shape: [] 
BikeCapacity = data['BikeCapacity']
# @Parameter BikeCharge @Def: Units of charge a bike requires @Shape: [] 
BikeCharge = data['BikeCharge']
# @Parameter ScooterCapacity @Def: Number of meals a scooter can hold @Shape: [] 
ScooterCapacity = data['ScooterCapacity']
# @Parameter ScooterCharge @Def: Units of charge a scooter requires @Shape: [] 
ScooterCharge = data['ScooterCharge']
# @Parameter MaxBikeFraction @Def: Maximum fraction of electric vehicles that can be bikes @Shape: [] 
MaxBikeFraction = data['MaxBikeFraction']
# @Parameter MinScooters @Def: Minimum number of scooters to be used @Shape: [] 
MinScooters = data['MinScooters']
# @Parameter TotalCharge @Def: Total units of charge available @Shape: [] 
TotalCharge = data['TotalCharge']

# Variables 
# @Variable NumberOfBikes @Def: The number of bikes @Shape: ['integer'] 
NumberOfBikes = model.addVar(vtype=GRB.INTEGER, name="NumberOfBikes")
# @Variable NumberOfScooters @Def: The number of scooters @Shape: ['integer'] 
NumberOfScooters = model.addVar(vtype=GRB.INTEGER, lb=MinScooters, name="NumberOfScooters")

# Constraints 
# @Constraint Constr_1 @Def: The proportion of bikes does not exceed MaxBikeFraction of all electric vehicles.
model.addConstr(NumberOfBikes <= MaxBikeFraction * (NumberOfBikes + NumberOfScooters))
# @Constraint Constr_2 @Def: At least MinScooters scooters must be used.
model.addConstr(NumberOfScooters >= MinScooters)
# @Constraint Constr_3 @Def: The total charge consumed by all vehicles does not exceed TotalCharge units.
model.addConstr(BikeCharge * NumberOfBikes + ScooterCharge * NumberOfScooters <= TotalCharge)

# Objective 
# @Objective Objective @Def: Maximize the total number of meals delivered, calculated as the sum of BikeCapacity multiplied by the number of bikes and ScooterCapacity multiplied by the number of scooters.
model.setObjective(BikeCapacity * NumberOfBikes + ScooterCapacity * NumberOfScooters, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfBikes'] = NumberOfBikes.x
variables['NumberOfScooters'] = NumberOfScooters.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
