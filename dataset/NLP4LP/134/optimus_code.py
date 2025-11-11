# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A company utilizes NumProcesses different production processes to manufacture
NumProducts types of products. Each process has a ProductionRate for each
product, requires a certain amount of PreliminaryMaterialRequired per hour, and
the company has a total of TotalPreliminaryMaterialAvailable units of
preliminary material available. The company must produce at least
MinProductRequired units of each product. The objective is to determine the
number of each process to run in order to minimize the total time needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/135/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProcesses @Def: Number of production processes @Shape: [] 
NumProcesses = data['NumProcesses']
# @Parameter NumProducts @Def: Number of product types @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter ProductionRate @Def: Production rate of each product per process (units per hour) @Shape: ['NumProcesses', 'NumProducts'] 
ProductionRate = data['ProductionRate']
# @Parameter PreliminaryMaterialRequired @Def: Preliminary material required per process (units per hour) @Shape: ['NumProcesses'] 
PreliminaryMaterialRequired = data['PreliminaryMaterialRequired']
# @Parameter TotalPreliminaryMaterialAvailable @Def: Total units of preliminary material available @Shape: [] 
TotalPreliminaryMaterialAvailable = data['TotalPreliminaryMaterialAvailable']
# @Parameter MinProductRequired @Def: Minimum units of each product to be produced @Shape: ['NumProducts'] 
MinProductRequired = data['MinProductRequired']

# Variables 
# @Variable NumberOfProcesses @Def: The number of each production process @Shape: ['NumProcesses'] 
NumberOfProcesses = model.addVars(NumProcesses, vtype=GRB.CONTINUOUS, name="NumberOfProcesses")
# @Variable Time @Def: The total production time @Shape: [] 
Time = model.addVar(vtype=GRB.CONTINUOUS, name="Time")

# Constraints 
# @Constraint Constr_1 @Def: The total preliminary material used by all processes cannot exceed TotalPreliminaryMaterialAvailable units. This is calculated as the sum of (PreliminaryMaterialRequired[i] * NumberOfProcesses[i] * Time) for all processes i.
model.addConstr(quicksum(PreliminaryMaterialRequired[i] * NumberOfProcesses[i] * Time for i in range(NumProcesses)) <= TotalPreliminaryMaterialAvailable)
# @Constraint Constr_2 @Def: For each product, the total production across all processes must be at least MinProductRequired units. This is calculated as the sum of (ProductionRate[i][j] * NumberOfProcesses[i] * Time) for all processes i and each product j.
model.addConstrs((quicksum(ProductionRate[i][j] * NumberOfProcesses[i] * Time for i in range(NumProcesses)) >= MinProductRequired[j] for j in range(NumProducts)), name="MinProductRequired")
# @Constraint Constr_3 @Def: Number of each process to run must be a non-negative value.
model.addConstrs((NumberOfProcesses[p] >= 0 for p in range(NumProcesses)), name="NumberOfProcesses_nonnegative")
# @Constraint Constr_4 @Def: Time must be a non-negative value.
model.addConstr(Time >= 0)

# Objective 
# @Objective Objective @Def: Minimize the total time needed by determining the number of each process to run.
model.setObjective(Time, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfProcesses'] = NumberOfProcesses.x
variables['Time'] = Time.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
