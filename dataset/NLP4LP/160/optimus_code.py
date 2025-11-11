# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A mail delivery service uses regular boats and speed boats. Each regular boat
trip can carry RegularBoatCapacity pieces of mail and consumes
RegularBoatGasConsumption liters of gas. Each speed boat trip can carry
SpeedBoatCapacity pieces of mail and consumes SpeedBoatGasConsumption liters of
gas. The number of regular boat trips is limited to MaxRegularBoatTrips. At
least MinFractionSpeedBoatTrips of the total trips must be made by speed boats.
The service needs to deliver TotalMail pieces of mail. Determine the number of
trips of each type to minimize the total gas consumed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/161/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter RegularBoatCapacity @Def: Number of pieces of mail a regular boat can carry per trip @Shape: [] 
RegularBoatCapacity = data['RegularBoatCapacity']
# @Parameter RegularBoatGasConsumption @Def: Amount of gas (liters) used by a regular boat per trip @Shape: [] 
RegularBoatGasConsumption = data['RegularBoatGasConsumption']
# @Parameter SpeedBoatCapacity @Def: Number of pieces of mail a speed boat can carry per trip @Shape: [] 
SpeedBoatCapacity = data['SpeedBoatCapacity']
# @Parameter SpeedBoatGasConsumption @Def: Amount of gas (liters) used by a speed boat per trip @Shape: [] 
SpeedBoatGasConsumption = data['SpeedBoatGasConsumption']
# @Parameter MaxRegularBoatTrips @Def: Maximum number of trips that can be made by regular boats @Shape: [] 
MaxRegularBoatTrips = data['MaxRegularBoatTrips']
# @Parameter MinFractionSpeedBoatTrips @Def: Minimum required fraction of trips to be made by speed boats @Shape: [] 
MinFractionSpeedBoatTrips = data['MinFractionSpeedBoatTrips']
# @Parameter TotalMail @Def: Total number of pieces of mail to be delivered @Shape: [] 
TotalMail = data['TotalMail']

# Variables 
# @Variable RegularBoatTrips @Def: The number of trips made by regular boats @Shape: [] 
RegularBoatTrips = model.addVar(vtype=GRB.INTEGER, ub=MaxRegularBoatTrips, name="RegularBoatTrips")
# @Variable SpeedBoatTrips @Def: The number of trips made by speed boats @Shape: [] 
SpeedBoatTrips = model.addVar(vtype=GRB.INTEGER, name="SpeedBoatTrips")

# Constraints 
# @Constraint Constr_1 @Def: The number of regular boat trips cannot exceed MaxRegularBoatTrips.
model.addConstr(RegularBoatTrips <= MaxRegularBoatTrips)
# @Constraint Constr_2 @Def: At least MinFractionSpeedBoatTrips fraction of the total trips must be made by speed boats.
model.addConstr(SpeedBoatTrips >= MinFractionSpeedBoatTrips * (RegularBoatTrips + SpeedBoatTrips))
# @Constraint Constr_3 @Def: The total number of pieces of mail delivered by regular and speed boats must be equal to TotalMail.
model.addConstr(RegularBoatTrips * RegularBoatCapacity + SpeedBoatTrips * SpeedBoatCapacity == TotalMail)

# Objective 
# @Objective Objective @Def: The total gas consumed is the sum of gas consumed by regular boats and speed boats per trip multiplied by the number of their respective trips. The objective is to minimize the total gas consumed.
model.setObjective(RegularBoatGasConsumption * RegularBoatTrips + SpeedBoatGasConsumption * SpeedBoatTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['RegularBoatTrips'] = RegularBoatTrips.x
variables['SpeedBoatTrips'] = SpeedBoatTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
