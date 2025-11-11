# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A farmer sends boxes of corn via ferry and light rail. Each ferry trip
transports FerryTripCapacity boxes, and each light rail trip transports
LightRailTripCapacity boxes. The number of light rail trips must be at least
MinLightRailMultiplier times the number of ferry trips. The farmer aims to send
at least MinBoxesToSend boxes of corn. The objective is to minimize the total
number of ferry and light rail trips.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/177/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter FerryTripCapacity @Def: Number of boxes of corn that can be sent per ferry trip @Shape: [] 
FerryTripCapacity = data['FerryTripCapacity']
# @Parameter LightRailTripCapacity @Def: Number of boxes of corn that can be sent per light rail trip @Shape: [] 
LightRailTripCapacity = data['LightRailTripCapacity']
# @Parameter MinLightRailMultiplier @Def: Minimum multiple that the number of light rail trips must be compared to ferry trips @Shape: [] 
MinLightRailMultiplier = data['MinLightRailMultiplier']
# @Parameter MinBoxesToSend @Def: Minimum number of boxes of corn that the farmer wants to send @Shape: [] 
MinBoxesToSend = data['MinBoxesToSend']

# Variables 
# @Variable FerryTrips @Def: The number of ferry trips @Shape: [] 
FerryTrips = model.addVar(vtype=GRB.INTEGER, name="FerryTrips")
# @Variable LightRailTrips @Def: The number of light rail trips @Shape: [] 
LightRailTrips = model.addVar(vtype=GRB.INTEGER, name="LightRailTrips")

# Constraints 
# @Constraint Constr_1 @Def: The number of light rail trips must be at least MinLightRailMultiplier times the number of ferry trips.
model.addConstr(LightRailTrips >= MinLightRailMultiplier * FerryTrips)
# @Constraint Constr_2 @Def: FerryTripCapacity multiplied by the number of ferry trips plus LightRailTripCapacity multiplied by the number of light rail trips must be at least MinBoxesToSend.
model.addConstr(FerryTripCapacity * FerryTrips + LightRailTripCapacity * LightRailTrips >= MinBoxesToSend)

# Objective 
# @Objective Objective @Def: Minimize the total number of ferry and light rail trips.
model.setObjective(quicksum([FerryTrips, LightRailTrips]), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['FerryTrips'] = FerryTrips.x
variables['LightRailTrips'] = LightRailTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
