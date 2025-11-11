# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A theme park transports its visitors using scooters and rickshaws. Each scooter
can carry ScooterCapacity people while each rickshaw can carry RickshawCapacity
people. At most MaxRickshawPercentage of the vehicles used can be rickshaws. The
park needs to transport at least NumVisitors visitors, and the objective is to
minimize the total number of scooters used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/158/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ScooterCapacity @Def: Capacity of a scooter in number of people @Shape: [] 
ScooterCapacity = data['ScooterCapacity']
# @Parameter RickshawCapacity @Def: Capacity of a rickshaw in number of people @Shape: [] 
RickshawCapacity = data['RickshawCapacity']
# @Parameter MaxRickshawPercentage @Def: Maximum percentage of vehicles that can be rickshaws @Shape: [] 
MaxRickshawPercentage = data['MaxRickshawPercentage']
# @Parameter NumVisitors @Def: Number of visitors to transport @Shape: [] 
NumVisitors = data['NumVisitors']

# Variables 
# @Variable NumScooters @Def: The number of scooters used to transport visitors @Shape: ['Integer'] 
NumScooters = model.addVar(vtype=GRB.INTEGER, name="NumScooters", lb=0)
# @Variable NumRickshaws @Def: The number of rickshaws used to transport visitors @Shape: ['Integer'] 
NumRickshaws = model.addVar(vtype=GRB.INTEGER, name="NumRickshaws")

# Constraints 
# @Constraint Constr_1 @Def: Each scooter can carry ScooterCapacity people and each rickshaw can carry RickshawCapacity people. The total number of people transported must be at least NumVisitors.
model.addConstr(ScooterCapacity * NumScooters + RickshawCapacity * NumRickshaws >= NumVisitors)
# @Constraint Constr_2 @Def: The number of rickshaws used must not exceed MaxRickshawPercentage of the total number of vehicles used.
model.addConstr((1 - MaxRickshawPercentage) * NumRickshaws <= MaxRickshawPercentage * NumScooters)

# Objective 
# @Objective Objective @Def: Minimize the total number of scooters used.
model.setObjective(NumScooters, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumScooters'] = NumScooters.x
variables['NumRickshaws'] = NumRickshaws.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
