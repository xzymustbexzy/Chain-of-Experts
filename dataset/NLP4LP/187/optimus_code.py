# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A volunteer organization transports voters to the polls using vans and cars,
where each van can carry VoterCapacityVan voters and each car can carry
VoterCapacityCar voters. They need to transport at least MinVoters voters, and
no more than MaxVanPercentage of the vehicles can be vans. The objective is to
minimize the number of cars used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/188/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VoterCapacityVan @Def: Number of voters a van can carry @Shape: [] 
VoterCapacityVan = data['VoterCapacityVan']
# @Parameter VoterCapacityCar @Def: Number of voters a car can carry @Shape: [] 
VoterCapacityCar = data['VoterCapacityCar']
# @Parameter MinVoters @Def: Minimum number of voters to transport @Shape: [] 
MinVoters = data['MinVoters']
# @Parameter MaxVanPercentage @Def: Maximum percentage of vehicles that can be vans @Shape: [] 
MaxVanPercentage = data['MaxVanPercentage']

# Variables 
# @Variable NumberOfVans @Def: The number of vans used @Shape: [] 
NumberOfVans = model.addVar(vtype=GRB.INTEGER, name="NumberOfVans")
# @Variable NumberOfCars @Def: The number of cars used @Shape: [] 
NumberOfCars = model.addVar(vtype=GRB.INTEGER, name="NumberOfCars")

# Constraints 
# @Constraint Constr_1 @Def: Each van can carry VoterCapacityVan voters and each car can carry VoterCapacityCar voters. The organization needs to transport at least 200 voters.
model.addConstr(VoterCapacityVan * NumberOfVans + VoterCapacityCar * NumberOfCars >= MinVoters)
# @Constraint Constr_2 @Def: No more than 30% of the vehicles can be vans.
model.addConstr(NumberOfVans <= MaxVanPercentage * (NumberOfVans + NumberOfCars))

# Objective 
# @Objective Objective @Def: Minimize the number of cars used.
model.setObjective(NumberOfCars, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfVans'] = NumberOfVans.x
variables['NumberOfCars'] = NumberOfCars.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
