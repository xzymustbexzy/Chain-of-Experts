# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A fishing boat transports fish to shore using canoes and diesel boats. Each
canoe can carry CanoeCapacity fish, and each diesel boat can carry
DieselBoatCapacity fish. The number of canoes used must be at least
CanoeToBoatRatio times the number of diesel boats used. To transport at least
MinFish fish, minimize the total number of canoes and diesel boats required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/187/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CanoeCapacity @Def: Number of fish that a canoe can carry @Shape: [] 
CanoeCapacity = data['CanoeCapacity']
# @Parameter DieselBoatCapacity @Def: Number of fish that a small diesel boat can carry @Shape: [] 
DieselBoatCapacity = data['DieselBoatCapacity']
# @Parameter CanoeToBoatRatio @Def: Minimum ratio of canoes to diesel boats @Shape: [] 
CanoeToBoatRatio = data['CanoeToBoatRatio']
# @Parameter MinFish @Def: Minimum number of fish to be transported to shore @Shape: [] 
MinFish = data['MinFish']

# Variables 
# @Variable NumberOfCanoes @Def: The number of canoes used @Shape: ['integer'] 
NumberOfCanoes = model.addVar(vtype=GRB.INTEGER, name="NumberOfCanoes")
# @Variable NumberOfDieselBoats @Def: The number of diesel boats used @Shape: ['integer'] 
NumberOfDieselBoats = model.addVar(vtype=GRB.INTEGER, name="NumberOfDieselBoats")

# Constraints 
# @Constraint Constr_1 @Def: Each canoe can carry CanoeCapacity fish and each diesel boat can carry DieselBoatCapacity fish. The total number of fish transported must be at least MinFish.
model.addConstr(CanoeCapacity * NumberOfCanoes + DieselBoatCapacity * NumberOfDieselBoats >= MinFish)
# @Constraint Constr_2 @Def: The number of canoes used must be at least CanoeToBoatRatio times the number of diesel boats used.
model.addConstr(NumberOfCanoes >= CanoeToBoatRatio * NumberOfDieselBoats)

# Objective 
# @Objective Objective @Def: Minimize the total number of canoes and diesel boats required.
model.setObjective(NumberOfCanoes + NumberOfDieselBoats, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfCanoes'] = NumberOfCanoes.x
variables['NumberOfDieselBoats'] = NumberOfDieselBoats.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
