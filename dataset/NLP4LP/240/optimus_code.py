# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A candle-making company can transport candles using freight and air. Freight can
transport FreightCapacityPerTrip tons per trip, while air can transport
AirCapacityPerTrip tons per trip. Each freight trip costs FreightCostPerTrip
dollars, and each air trip costs AirCostPerTrip dollars. The company needs to
transport at least MinimumTotalTons of candles and has a transportation budget
of Budget dollars. Additionally, at least MinimumAirProportion proportion of the
total tons must be transported via air. There must also be at least
MinimumFreightTrips freight trips. The objective is to determine the number of
freight and air trips to minimize the total number of trips.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/241/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter FreightCapacityPerTrip @Def: Amount of tons freight can transport per trip @Shape: [] 
FreightCapacityPerTrip = data['FreightCapacityPerTrip']
# @Parameter AirCapacityPerTrip @Def: Amount of tons air can transport per trip @Shape: [] 
AirCapacityPerTrip = data['AirCapacityPerTrip']
# @Parameter FreightCostPerTrip @Def: Cost per freight trip in dollars @Shape: [] 
FreightCostPerTrip = data['FreightCostPerTrip']
# @Parameter AirCostPerTrip @Def: Cost per air trip in dollars @Shape: [] 
AirCostPerTrip = data['AirCostPerTrip']
# @Parameter MinimumTotalTons @Def: Minimum total tons to transport @Shape: [] 
MinimumTotalTons = data['MinimumTotalTons']
# @Parameter Budget @Def: Budget for transportation in dollars @Shape: [] 
Budget = data['Budget']
# @Parameter MinimumAirProportion @Def: Minimum proportion of tons to transport via air @Shape: [] 
MinimumAirProportion = data['MinimumAirProportion']
# @Parameter MinimumFreightTrips @Def: Minimum number of freight trips @Shape: [] 
MinimumFreightTrips = data['MinimumFreightTrips']

# Variables 
# @Variable FreightTrips @Def: The number of freight trips @Shape: [] 
FreightTrips = model.addVar(vtype=GRB.INTEGER, name="FreightTrips")
# @Variable AirTrips @Def: The number of air trips @Shape: [] 
AirTrips = model.addVar(vtype=GRB.INTEGER, name="AirTrips")

# Constraints 
# @Constraint Constr_1 @Def: The company needs to transport at least MinimumTotalTons of candles.
model.addConstr(FreightTrips * FreightCapacityPerTrip + AirTrips * AirCapacityPerTrip >= MinimumTotalTons)
# @Constraint Constr_2 @Def: The transportation budget is limited to Budget dollars.
model.addConstr(FreightTrips * FreightCostPerTrip + AirTrips * AirCostPerTrip <= Budget)
# @Constraint Constr_3 @Def: At least MinimumAirProportion proportion of the total tons must be transported via air.
model.addConstr(AirTrips * AirCapacityPerTrip >= MinimumAirProportion * (FreightTrips * FreightCapacityPerTrip + AirTrips * AirCapacityPerTrip))
# @Constraint Constr_4 @Def: There must be at least MinimumFreightTrips freight trips.
model.addConstr(FreightTrips >= MinimumFreightTrips)

# Objective 
# @Objective Objective @Def: Determine the number of freight and air trips to minimize the total number of trips.
model.setObjective(FreightTrips + AirTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['FreightTrips'] = FreightTrips.x
variables['AirTrips'] = AirTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
