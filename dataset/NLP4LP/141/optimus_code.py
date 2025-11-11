# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of boat trips and canoe trips to minimize the total
transportation time, where each boat trip carries BoatCapacity ducks and takes
BoatTripTime minutes, and each canoe trip carries CanoeCapacity ducks and takes
CanoeTripTime minutes. The number of boat trips must not exceed MaxBoatTrips, at
least MinCanoeTripFraction of all trips must be canoe trips, and the total
number of ducks transported must be at least MinDucks.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/142/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter BoatCapacity @Def: Number of ducks a boat can carry per trip @Shape: [] 
BoatCapacity = data['BoatCapacity']
# @Parameter CanoeCapacity @Def: Number of ducks a canoe can carry per trip @Shape: [] 
CanoeCapacity = data['CanoeCapacity']
# @Parameter BoatTripTime @Def: Time in minutes per boat trip @Shape: [] 
BoatTripTime = data['BoatTripTime']
# @Parameter CanoeTripTime @Def: Time in minutes per canoe trip @Shape: [] 
CanoeTripTime = data['CanoeTripTime']
# @Parameter MaxBoatTrips @Def: Maximum number of boat trips allowed @Shape: [] 
MaxBoatTrips = data['MaxBoatTrips']
# @Parameter MinCanoeTripFraction @Def: Minimum fraction of trips that must be by canoe @Shape: [] 
MinCanoeTripFraction = data['MinCanoeTripFraction']
# @Parameter MinDucks @Def: Minimum number of ducks to be transported to shore @Shape: [] 
MinDucks = data['MinDucks']

# Variables 
# @Variable BoatTrips @Def: The number of boat trips @Shape: ['NonNegative', 'Integer'] 
BoatTrips = model.addVar(vtype=GRB.INTEGER, name="BoatTrips", lb=0)
# @Variable CanoeTrips @Def: The number of canoe trips @Shape: ['NonNegative', 'Integer'] 
CanoeTrips = model.addVar(vtype=GRB.INTEGER, name="CanoeTrips")

# Constraints 
# @Constraint Constr_1 @Def: The number of boat trips must not exceed MaxBoatTrips.
model.addConstr(BoatTrips <= MaxBoatTrips)
# @Constraint Constr_2 @Def: At least MinCanoeTripFraction of all trips must be canoe trips.
model.addConstr(CanoeTrips >= MinCanoeTripFraction * (BoatTrips + CanoeTrips))
# @Constraint Constr_3 @Def: The total number of ducks transported must be at least MinDucks.
model.addConstr(BoatTrips * BoatCapacity + CanoeTrips * CanoeCapacity >= MinDucks)

# Objective 
# @Objective Objective @Def: Minimize the total transportation time, which is calculated as (Number of boat trips × BoatTripTime) + (Number of canoe trips × CanoeTripTime).
model.setObjective(BoatTrips * BoatTripTime + CanoeTrips * CanoeTripTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['BoatTrips'] = BoatTrips.x
variables['CanoeTrips'] = CanoeTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
