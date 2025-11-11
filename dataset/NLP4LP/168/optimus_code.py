# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An industrial tire company transports tires using cargo planes and ultrawide
trucks. Each cargo plane trip transports TiresPerPlaneTrip tires and costs
CostPerPlaneTrip dollars. Each ultrawide truck trip transports TiresPerTruckTrip
tires and costs CostPerTruckTrip dollars. The company needs to transport at
least MinTires tires and has a budget of AvailableBudget dollars. The number of
cargo plane trips cannot exceed the number of ultrawide truck trips. Determine
the number of cargo plane trips and ultrawide truck trips to minimize the total
number of trips.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/169/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TiresPerPlaneTrip @Def: Number of tires that can be transported by one cargo plane per trip @Shape: [] 
TiresPerPlaneTrip = data['TiresPerPlaneTrip']
# @Parameter CostPerPlaneTrip @Def: Cost of one cargo plane trip in dollars @Shape: [] 
CostPerPlaneTrip = data['CostPerPlaneTrip']
# @Parameter TiresPerTruckTrip @Def: Number of tires that can be transported by one ultrawide truck per trip @Shape: [] 
TiresPerTruckTrip = data['TiresPerTruckTrip']
# @Parameter CostPerTruckTrip @Def: Cost of one ultrawide truck trip in dollars @Shape: [] 
CostPerTruckTrip = data['CostPerTruckTrip']
# @Parameter MinTires @Def: Minimum number of tires to be transported @Shape: [] 
MinTires = data['MinTires']
# @Parameter AvailableBudget @Def: Available budget in dollars for transportation @Shape: [] 
AvailableBudget = data['AvailableBudget']

# Variables 
# @Variable PlaneTrips @Def: The number of cargo plane trips @Shape: ['integer'] 
PlaneTrips = model.addVar(vtype=GRB.INTEGER, name="PlaneTrips")
# @Variable TruckTrips @Def: The number of ultrawide truck trips @Shape: ['integer'] 
TruckTrips = model.addVar(vtype=GRB.INTEGER, name="TruckTrips")

# Constraints 
# @Constraint Constr_1 @Def: The total number of tires transported by cargo planes and ultrawide trucks must be at least MinTires.
model.addConstr(PlaneTrips * TiresPerPlaneTrip + TruckTrips * TiresPerTruckTrip >= MinTires)
# @Constraint Constr_2 @Def: The total cost of cargo plane and ultrawide truck trips must not exceed AvailableBudget dollars.
model.addConstr(CostPerPlaneTrip * PlaneTrips + CostPerTruckTrip * TruckTrips <= AvailableBudget)
# @Constraint Constr_3 @Def: The number of cargo plane trips cannot exceed the number of ultrawide truck trips.
model.addConstr(PlaneTrips <= TruckTrips)

# Objective 
# @Objective Objective @Def: Minimize the total number of cargo plane trips and ultrawide truck trips required to transport all tires within the budget and logistical constraints.
model.setObjective(PlaneTrips + TruckTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['PlaneTrips'] = PlaneTrips.x
variables['TruckTrips'] = TruckTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
