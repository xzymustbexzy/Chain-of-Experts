# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The company selects the number of large and small cruise ship trips to minimize
(PollutionLarge × LargeTrips + PollutionSmall × SmallTrips) subject to
LargeTrips ≤ MaxLargeTrips, SmallTrips ≥ MinSmallTripsPercentage × (LargeTrips +
SmallTrips), and (CapacityLarge × LargeTrips + CapacitySmall × SmallTrips) ≥
RequiredCustomers.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/235/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CapacityLarge @Def: Capacity of a large cruise ship in number of customers @Shape: [] 
CapacityLarge = data['CapacityLarge']
# @Parameter CapacitySmall @Def: Capacity of a small cruise ship in number of customers @Shape: [] 
CapacitySmall = data['CapacitySmall']
# @Parameter PollutionLarge @Def: Pollution produced by a large cruise ship trip @Shape: [] 
PollutionLarge = data['PollutionLarge']
# @Parameter PollutionSmall @Def: Pollution produced by a small cruise ship trip @Shape: [] 
PollutionSmall = data['PollutionSmall']
# @Parameter MaxLargeTrips @Def: Maximum number of large cruise ship trips @Shape: [] 
MaxLargeTrips = data['MaxLargeTrips']
# @Parameter MinSmallTripsPercentage @Def: Minimum proportion of total trips made by small cruise ships @Shape: [] 
MinSmallTripsPercentage = data['MinSmallTripsPercentage']
# @Parameter RequiredCustomers @Def: Required number of customers to transport @Shape: [] 
RequiredCustomers = data['RequiredCustomers']

# Variables 
# @Variable NumberLargeTrips @Def: The number of large cruise ship trips @Shape: ['Integer'] 
NumberLargeTrips = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxLargeTrips, name="NumberLargeTrips")
# @Variable NumberSmallTrips @Def: The number of small cruise ship trips @Shape: ['Integer'] 
NumberSmallTrips = model.addVar(vtype=GRB.INTEGER, name="NumberSmallTrips")

# Constraints 
# @Constraint Constr_1 @Def: The number of large trips must not exceed MaxLargeTrips.
model.addConstr(NumberLargeTrips <= MaxLargeTrips)
# @Constraint Constr_2 @Def: The number of small trips must be at least MinSmallTripsPercentage times the total number of trips (LargeTrips + SmallTrips).
model.addConstr(NumberSmallTrips >= MinSmallTripsPercentage * (NumberLargeTrips + NumberSmallTrips))
# @Constraint Constr_3 @Def: The combined capacity of large and small trips must be at least RequiredCustomers (CapacityLarge × LargeTrips + CapacitySmall × SmallTrips ≥ RequiredCustomers).
model.addConstr(CapacityLarge * NumberLargeTrips + CapacitySmall * NumberSmallTrips >= RequiredCustomers)

# Objective 
# @Objective Objective @Def: Minimize the total pollution, calculated as PollutionLarge × LargeTrips + PollutionSmall × SmallTrips.
model.setObjective(PollutionLarge * NumberLargeTrips + PollutionSmall * NumberSmallTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberLargeTrips'] = NumberLargeTrips.x
variables['NumberSmallTrips'] = NumberSmallTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
