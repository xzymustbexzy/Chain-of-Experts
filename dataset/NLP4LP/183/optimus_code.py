# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Maximize the total snow transported by small and large trucks, where each small
truck has a snow carrying capacity of SnowCapacitySmallTruck and each large
truck has a snow carrying capacity of SnowCapacityLargeTruck. This is subject to
the constraint that the total number of people required, calculated as
PeoplePerSmallTruck multiplied by the number of small trucks plus
PeoplePerLargeTruck multiplied by the number of large trucks, does not exceed
TotalPeople. Additionally, the number of small trucks must be at least
MinSmallTrucks, the number of large trucks must be at least MinLargeTrucks, and
the number of small trucks must be SmallTrucksPerLargeTruck times the number of
large trucks.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/184/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PeoplePerSmallTruck @Def: Number of people required to shovel snow per small truck @Shape: [] 
PeoplePerSmallTruck = data['PeoplePerSmallTruck']
# @Parameter PeoplePerLargeTruck @Def: Number of people required to shovel snow per large truck @Shape: [] 
PeoplePerLargeTruck = data['PeoplePerLargeTruck']
# @Parameter SnowCapacitySmallTruck @Def: Snow carrying capacity of a small truck (in units) @Shape: [] 
SnowCapacitySmallTruck = data['SnowCapacitySmallTruck']
# @Parameter SnowCapacityLargeTruck @Def: Snow carrying capacity of a large truck (in units) @Shape: [] 
SnowCapacityLargeTruck = data['SnowCapacityLargeTruck']
# @Parameter TotalPeople @Def: Total number of people available for snow shoveling @Shape: [] 
TotalPeople = data['TotalPeople']
# @Parameter MinSmallTrucks @Def: Minimum number of small trucks required @Shape: [] 
MinSmallTrucks = data['MinSmallTrucks']
# @Parameter MinLargeTrucks @Def: Minimum number of large trucks required @Shape: [] 
MinLargeTrucks = data['MinLargeTrucks']
# @Parameter SmallTrucksPerLargeTruck @Def: Number of small trucks per large truck @Shape: [] 
SmallTrucksPerLargeTruck = data['SmallTrucksPerLargeTruck']

# Variables 
# @Variable NumberSmallTrucks @Def: The number of small trucks @Shape: [] 
NumberSmallTrucks = model.addVar(vtype=GRB.INTEGER, name="NumberSmallTrucks")
# @Variable NumberLargeTrucks @Def: The number of large trucks @Shape: [] 
NumberLargeTrucks = model.addVar(vtype=GRB.INTEGER, lb=MinLargeTrucks, name="NumberLargeTrucks")

# Constraints 
# @Constraint Constr_1 @Def: The total number of people required, calculated as PeoplePerSmallTruck multiplied by the number of small trucks plus PeoplePerLargeTruck multiplied by the number of large trucks, does not exceed TotalPeople.
model.addConstr(PeoplePerSmallTruck * NumberSmallTrucks + PeoplePerLargeTruck * NumberLargeTrucks <= TotalPeople)
# @Constraint Constr_2 @Def: The number of small trucks must be at least MinSmallTrucks.
model.addConstr(NumberSmallTrucks >= MinSmallTrucks)
# @Constraint Constr_3 @Def: The number of large trucks must be at least MinLargeTrucks.
model.addConstr(NumberLargeTrucks >= MinLargeTrucks)
# @Constraint Constr_4 @Def: The number of small trucks must be SmallTrucksPerLargeTruck times the number of large trucks.
model.addConstr(NumberSmallTrucks == SmallTrucksPerLargeTruck * NumberLargeTrucks)

# Objective 
# @Objective Objective @Def: Maximize the total snow transported by small and large trucks, where each small truck has a snow carrying capacity of SnowCapacitySmallTruck and each large truck has a snow carrying capacity of SnowCapacityLargeTruck.
model.setObjective(NumberSmallTrucks * SnowCapacitySmallTruck + NumberLargeTrucks * SnowCapacityLargeTruck, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberSmallTrucks'] = NumberSmallTrucks.x
variables['NumberLargeTrucks'] = NumberLargeTrucks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
