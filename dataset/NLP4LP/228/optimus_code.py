# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A party organizer needs to transport at least MinPeople people using limousines
and buses. Each limousine can carry LimousineCapacity people and each bus can
carry BusCapacity people. At least MinLimousineFraction of the vehicles used
must be limousines. The objective is to minimize the total number of limousines
and buses used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/229/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter LimousineCapacity @Def: Number of people a limousine can carry @Shape: [] 
LimousineCapacity = data['LimousineCapacity']
# @Parameter BusCapacity @Def: Number of people a bus can carry @Shape: [] 
BusCapacity = data['BusCapacity']
# @Parameter MinPeople @Def: Minimum number of people to transport @Shape: [] 
MinPeople = data['MinPeople']
# @Parameter MinLimousineFraction @Def: Minimum fraction of vehicles that must be limousines @Shape: [] 
MinLimousineFraction = data['MinLimousineFraction']

# Variables 
# @Variable NumLimousines @Def: The number of limousines used @Shape: ['Integer'] 
NumLimousines = model.addVar(vtype=GRB.INTEGER, name="NumLimousines")
# @Variable PeopleLimousines @Def: The number of people assigned to limousines @Shape: ['Continuous'] 
PeopleLimousines = model.addVar(vtype=GRB.CONTINUOUS, name="PeopleLimousines")
# @Variable NumBuses @Def: The number of buses used @Shape: ['Integer'] 
NumBuses = model.addVar(vtype=GRB.INTEGER, name="NumBuses")
# @Variable PeopleBuses @Def: The number of people assigned to buses @Shape: ['Continuous'] 
PeopleBuses = model.addVar(vtype=GRB.CONTINUOUS, name="PeopleBuses")

# Constraints 
# @Constraint Constr_1 @Def: Each limousine can carry LimousineCapacity people.
model.addConstr(PeopleLimousines <= LimousineCapacity * NumLimousines)
# @Constraint Constr_2 @Def: Each bus can carry BusCapacity people.
model.addConstr(PeopleBuses <= NumBuses * BusCapacity)
# @Constraint Constr_3 @Def: The total number of people transported by limousines and buses must be at least MinPeople.
model.addConstr(PeopleLimousines + PeopleBuses >= MinPeople)
# @Constraint Constr_4 @Def: At least MinLimousineFraction of the vehicles used must be limousines.
model.addConstr(NumLimousines >= MinLimousineFraction * (NumLimousines + NumBuses))

# Objective 
# @Objective Objective @Def: Minimize the total number of limousines and buses used.
model.setObjective(NumLimousines + NumBuses, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumLimousines'] = NumLimousines.x
variables['PeopleLimousines'] = PeopleLimousines.x
variables['NumBuses'] = NumBuses.x
variables['PeopleBuses'] = PeopleBuses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
