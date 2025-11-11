# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
You are designing an office space with NumDeskTypes different desk types. Each
desk type has a Price, Space, and Seats. The total cost of the desks must not
exceed MaxBudget, and the total space occupied by the desks must not exceed
MaxSpace. The goal is to determine the number of each desk type to maximize the
total seating availability.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/23/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumDeskTypes @Def: Number of desk types @Shape: [] 
NumDeskTypes = data['NumDeskTypes']
# @Parameter Price @Def: Cost of each desk type @Shape: ['NumDeskTypes'] 
Price = data['Price']
# @Parameter Space @Def: Space occupied by each desk type @Shape: ['NumDeskTypes'] 
Space = data['Space']
# @Parameter Seats @Def: Seating capacity of each desk type @Shape: ['NumDeskTypes'] 
Seats = data['Seats']
# @Parameter MaxBudget @Def: Maximum budget available @Shape: [] 
MaxBudget = data['MaxBudget']
# @Parameter MaxSpace @Def: Maximum office space for desks @Shape: [] 
MaxSpace = data['MaxSpace']

# Variables 
# @Variable NumDesks @Def: The number of desks of each type @Shape: ['NumDeskTypes'] 
NumDesks = model.addVars(NumDeskTypes, vtype=GRB.INTEGER, name="NumDesks")

# Constraints 
# @Constraint Constr_1 @Def: The total cost of the desks must not exceed MaxBudget.
model.addConstr(quicksum(Price[i] * NumDesks[i] for i in range(NumDeskTypes)) <= MaxBudget)
# @Constraint Constr_2 @Def: The total space occupied by the desks must not exceed MaxSpace.
model.addConstr(quicksum(Space[i] * NumDesks[i] for i in range(NumDeskTypes)) <= MaxSpace)

# Objective 
# @Objective Objective @Def: The total seating availability is the sum of the seating capacity of each desk type multiplied by the number of that desk type. The objective is to maximize the total seating availability.
model.setObjective(quicksum(Seats[i] * NumDesks[i] for i in range(NumDeskTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumDesks'] = {i: var.x for i, var in NumDesks.items()}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)