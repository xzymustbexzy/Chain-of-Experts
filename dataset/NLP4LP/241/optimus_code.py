# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The production company needs to transport TotalPeople using large mobile
production units and small mobile production units. Each large unit can hold
CapacityLargeUnit people and occupies ParkingLargeUnit parking spots. Each small
unit can hold CapacitySmallUnit people and occupies ParkingSmallUnit parking
spots. At least MinSmallUnits small mobile production units must be used. The
number of large mobile production units must be at least MinLargeUnitProportion
of all mobile production units. The objective is to minimize the total number of
parking spots required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/242/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CapacityLargeUnit @Def: Number of people that one large mobile production unit can hold @Shape: [] 
CapacityLargeUnit = data['CapacityLargeUnit']
# @Parameter ParkingLargeUnit @Def: Number of parking spots occupied by one large mobile production unit @Shape: [] 
ParkingLargeUnit = data['ParkingLargeUnit']
# @Parameter CapacitySmallUnit @Def: Number of people that one small mobile production unit can hold @Shape: [] 
CapacitySmallUnit = data['CapacitySmallUnit']
# @Parameter ParkingSmallUnit @Def: Number of parking spots occupied by one small mobile production unit @Shape: [] 
ParkingSmallUnit = data['ParkingSmallUnit']
# @Parameter MinSmallUnits @Def: Minimum number of small mobile production units required @Shape: [] 
MinSmallUnits = data['MinSmallUnits']
# @Parameter MinLargeUnitProportion @Def: Minimum proportion of large mobile production units relative to total vehicles @Shape: [] 
MinLargeUnitProportion = data['MinLargeUnitProportion']
# @Parameter TotalPeople @Def: Total number of people that need to be transported @Shape: [] 
TotalPeople = data['TotalPeople']

# Variables 
# @Variable NumberLargeUnits @Def: The number of large mobile production units used @Shape: [] 
NumberLargeUnits = model.addVar(vtype=GRB.INTEGER, name="NumberLargeUnits")
# @Variable NumberSmallUnits @Def: The number of small mobile production units used @Shape: [] 
NumberSmallUnits = model.addVar(vtype=GRB.INTEGER, lb=MinSmallUnits, name="NumberSmallUnits")

# Constraints 
# @Constraint Constr_1 @Def: The number of people transported using large and small mobile production units must be at least TotalPeople. Each large unit holds CapacityLargeUnit people and each small unit holds CapacitySmallUnit people.
model.addConstr(CapacityLargeUnit * NumberLargeUnits + CapacitySmallUnit * NumberSmallUnits >= TotalPeople)
# @Constraint Constr_2 @Def: At least MinSmallUnits small mobile production units must be used.
model.addConstr(NumberSmallUnits >= MinSmallUnits)
# @Constraint Constr_3 @Def: The number of large mobile production units must be at least MinLargeUnitProportion of all mobile production units.
model.addConstr(NumberLargeUnits >= MinLargeUnitProportion * (NumberLargeUnits + NumberSmallUnits))

# Objective 
# @Objective Objective @Def: Minimize the total number of parking spots required. The total parking spots are calculated by summing the parking spots occupied by large and small mobile production units, where each large unit occupies ParkingLargeUnit spots and each small unit occupies ParkingSmallUnit spots.
model.setObjective(NumberLargeUnits * ParkingLargeUnit + NumberSmallUnits * ParkingSmallUnit, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberLargeUnits'] = NumberLargeUnits.x
variables['NumberSmallUnits'] = NumberSmallUnits.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
