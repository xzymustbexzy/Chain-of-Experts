# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An international goods exporter uses ships and planes to transport goods. Each
ship can carry ShipCapacity containers and consumes ShipFuel liters of fuel per
trip. Each plane can carry PlaneCapacity containers and consumes PlaneFuel
liters of fuel per trip. The company needs to transport at least MinContainers
containers. Additionally, no more than MaxPlaneTrips plane trips can be made,
and at least MinShipTripFraction of the total trips must be by ship. The
objective is to minimize the total fuel consumption.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/141/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ShipCapacity @Def: Capacity of a ship in containers @Shape: [] 
ShipCapacity = data['ShipCapacity']
# @Parameter ShipFuel @Def: Fuel usage of a ship per trip in liters @Shape: [] 
ShipFuel = data['ShipFuel']
# @Parameter PlaneCapacity @Def: Capacity of a plane in containers @Shape: [] 
PlaneCapacity = data['PlaneCapacity']
# @Parameter PlaneFuel @Def: Fuel usage of a plane per trip in liters @Shape: [] 
PlaneFuel = data['PlaneFuel']
# @Parameter MinContainers @Def: Minimum number of containers to transport @Shape: [] 
MinContainers = data['MinContainers']
# @Parameter MaxPlaneTrips @Def: Maximum number of plane trips @Shape: [] 
MaxPlaneTrips = data['MaxPlaneTrips']
# @Parameter MinShipTripFraction @Def: Minimum fraction of trips that must be by ship @Shape: [] 
MinShipTripFraction = data['MinShipTripFraction']

# Variables 
# @Variable ShipTrips @Def: The number of ship trips @Shape: [] 
ShipTrips = model.addVar(vtype=GRB.INTEGER, name="ShipTrips")
# @Variable PlaneTrips @Def: The number of plane trips @Shape: [] 
PlaneTrips = model.addVar(vtype=GRB.INTEGER, name="PlaneTrips")

# Constraints 
# @Constraint Constr_1 @Def: The total number of containers transported by ships and planes must be at least MinContainers.
model.addConstr(ShipTrips * ShipCapacity + PlaneTrips * PlaneCapacity >= MinContainers)
# @Constraint Constr_2 @Def: No more than MaxPlaneTrips plane trips can be made.
model.addConstr(PlaneTrips <= MaxPlaneTrips)
# @Constraint Constr_3 @Def: At least MinShipTripFraction of the total trips must be by ship.
model.addConstr(ShipTrips >= MinShipTripFraction * (ShipTrips + PlaneTrips))

# Objective 
# @Objective Objective @Def: Minimize the total fuel consumption, which is the sum of fuel used by ships and planes based on the number of trips made.
model.setObjective(ShipFuel * ShipTrips + PlaneFuel * PlaneTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ShipTrips'] = ShipTrips.x
variables['PlaneTrips'] = PlaneTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
