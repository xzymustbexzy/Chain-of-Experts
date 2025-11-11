# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An airport buys NumVehicleTypes types of vehicles. Each vehicle type can move
LuggageCapacity luggage per day and produces PollutantPerVehicleType units of
pollutant per day. The airport needs to move at least MinLuggageRequired luggage
per day and can produce at most MaxPollutantAllowed units of pollutant per day.
Determine the number of each vehicle type to minimize the total number of
vehicles needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/73/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumVehicleTypes @Def: Number of vehicle types @Shape: [] 
NumVehicleTypes = data['NumVehicleTypes']
# @Parameter MinLuggageRequired @Def: Minimum number of luggage to move per day @Shape: [] 
MinLuggageRequired = data['MinLuggageRequired']
# @Parameter MaxPollutantAllowed @Def: Maximum pollutant allowed per day @Shape: [] 
MaxPollutantAllowed = data['MaxPollutantAllowed']
# @Parameter LuggageCapacity @Def: Luggage capacity per vehicle type per day @Shape: ['NumVehicleTypes'] 
LuggageCapacity = data['LuggageCapacity']
# @Parameter PollutantPerVehicleType @Def: Pollutant produced per vehicle type per day @Shape: ['NumVehicleTypes'] 
PollutantPerVehicleType = data['PollutantPerVehicleType']

# Variables 
# @Variable NumberOfVehicles @Def: The number of vehicles of each type used per day @Shape: ['NumVehicleTypes'] 
NumberOfVehicles = model.addVars(NumVehicleTypes, vtype=GRB.INTEGER, name="NumberOfVehicles")

# Constraints 
# @Constraint Constr_1 @Def: Each vehicle type can move LuggageCapacity luggage per day. The airport needs to move at least MinLuggageRequired luggage per day.
model.addConstr(quicksum(LuggageCapacity[i] * NumberOfVehicles[i] for i in range(NumVehicleTypes)) >= MinLuggageRequired)
# @Constraint Constr_2 @Def: Each vehicle type produces PollutantPerVehicleType units of pollutant per day. The airport can produce at most MaxPollutantAllowed units of pollutant per day.
model.addConstr(quicksum(PollutantPerVehicleType[t] * NumberOfVehicles[t] for t in range(NumVehicleTypes)) <= MaxPollutantAllowed)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of vehicles needed.
model.setObjective(quicksum(NumberOfVehicles[i] for i in range(NumVehicleTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfVehicles'] = model.getAttr("X", NumberOfVehicles)
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
