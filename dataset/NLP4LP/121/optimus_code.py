# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
In a science club, there are NumTables different tables for making slime. At
each table i, PowderUsed[i] units of powder and GlueUsed[i] units of glue are
used to produce SlimeProduced[i] units of slime. Each table i also generates
MessProduced[i] units of mess. The club has AvailablePowder units of powder and
AvailableGlue units of glue available. Additionally, no more than MaxMess units
of mess can be created. The objective is to determine the number of each table
to set up to maximize the total amount of slime produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/122/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumTables @Def: Number of different tables for making slime @Shape: [] 
NumTables = data['NumTables']
# @Parameter PowderUsed @Def: Amount of powder used by table i @Shape: ['NumTables'] 
PowderUsed = data['PowderUsed']
# @Parameter GlueUsed @Def: Amount of glue used by table i @Shape: ['NumTables'] 
GlueUsed = data['GlueUsed']
# @Parameter SlimeProduced @Def: Amount of slime produced by table i @Shape: ['NumTables'] 
SlimeProduced = data['SlimeProduced']
# @Parameter MessProduced @Def: Amount of mess produced by table i @Shape: ['NumTables'] 
MessProduced = data['MessProduced']
# @Parameter AvailablePowder @Def: Total available units of powder @Shape: [] 
AvailablePowder = data['AvailablePowder']
# @Parameter AvailableGlue @Def: Total available units of glue @Shape: [] 
AvailableGlue = data['AvailableGlue']
# @Parameter MaxMess @Def: Maximum allowable units of mess @Shape: [] 
MaxMess = data['MaxMess']

# Variables 
# @Variable Production @Def: The amount produced at table i @Shape: ['NumTables'] 
Production = model.addVars(NumTables, vtype=GRB.CONTINUOUS, name="Production")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of powder used by all tables cannot exceed AvailablePowder.
model.addConstr(quicksum(PowderUsed[i] * Production[i] for i in range(NumTables)) <= AvailablePowder)
# @Constraint Constr_2 @Def: The total amount of glue used by all tables cannot exceed AvailableGlue.
model.addConstr(quicksum(GlueUsed[i] * Production[i] for i in range(NumTables)) <= AvailableGlue)
# @Constraint Constr_3 @Def: The total amount of mess produced by all tables cannot exceed MaxMess.
model.addConstr(quicksum(Production[i] * MessProduced[i] for i in range(NumTables)) <= MaxMess)

# Objective 
# @Objective Objective @Def: The total amount of slime produced is the sum of SlimeProduced[i] multiplied by the number of each table set up. The objective is to maximize the total amount of slime produced.
model.setObjective(quicksum(SlimeProduced[i] * Production[i] for i in range(NumTables)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Production'] = {i: Production[i].X for i in range(NumTables)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
