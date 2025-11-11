# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A mining company allocates TotalLand square miles between NumTechniques mining
techniques to maximize the total daily production of rare earth oxide. Each
mining technique i has a ProductionRate[i] per square mile, generates
WastewaterRate[i] tons of polluted wastewater per square mile daily, and
requires MachinesRequired[i] extraction machines per square mile. The total
number of extraction machines used must not exceed TotalMachines, and the total
polluted wastewater produced must not exceed MaxWastewater tons daily.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/85/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalLand @Def: Total land available for mining in square miles @Shape: [] 
TotalLand = data['TotalLand']
# @Parameter TotalMachines @Def: Total number of extraction machines available @Shape: [] 
TotalMachines = data['TotalMachines']
# @Parameter MaxWastewater @Def: Maximum allowed polluted wastewater per day in tons @Shape: [] 
MaxWastewater = data['MaxWastewater']
# @Parameter NumTechniques @Def: Number of mining techniques @Shape: [] 
NumTechniques = data['NumTechniques']
# @Parameter ProductionRate @Def: Daily production of rare earth oxide per square mile for each mining technique @Shape: ['NumTechniques'] 
ProductionRate = data['ProductionRate']
# @Parameter WastewaterRate @Def: Daily polluted wastewater created per square mile for each mining technique @Shape: ['NumTechniques'] 
WastewaterRate = data['WastewaterRate']
# @Parameter MachinesRequired @Def: Number of extraction machines required per square mile for each mining technique @Shape: ['NumTechniques'] 
MachinesRequired = data['MachinesRequired']

# Variables 
# @Variable LandAllocated @Def: The amount of land allocated to each mining technique @Shape: ['NumTechniques'] 
LandAllocated = model.addVars(NumTechniques, vtype=GRB.CONTINUOUS, name="LandAllocated")

# Constraints 
# @Constraint Constr_1 @Def: The total land allocated to all mining techniques cannot exceed TotalLand square miles.
model.addConstr(quicksum(LandAllocated[i] for i in range(NumTechniques)) <= TotalLand)
# @Constraint Constr_2 @Def: The total number of extraction machines required for all mining techniques cannot exceed TotalMachines.
model.addConstr(quicksum(MachinesRequired[i] * LandAllocated[i] for i in range(NumTechniques)) <= TotalMachines)
# @Constraint Constr_3 @Def: The total polluted wastewater produced by all mining techniques cannot exceed MaxWastewater tons daily.
model.addConstr(quicksum(WastewaterRate[i] * LandAllocated[i] for i in range(NumTechniques)) <= MaxWastewater)

# Objective 
# @Objective Objective @Def: Maximize the total daily production of rare earth oxide.
model.setObjective(quicksum(ProductionRate[i] * LandAllocated[i] for i in range(NumTechniques)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['LandAllocated'] = model.getAttr("X", LandAllocated)
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
