# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A post office is purchasing dual and single model stamping machines. A dual
model stamping machine stamps DualStampRate letters per minute and uses
DualGlueUsage units of glue per minute. A single model stamping machine stamps
SingleStampRate letters per minute and uses SingleGlueUsage units of glue per
minute. The number of single model stamping machines must exceed the number of
dual model stamping machines. The post office must stamp at least
MinTotalLetters letters per minute and use at most MaxGlueUsage units of glue
per minute. The objective is to minimize the total number of stamping machines
purchased.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/67/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter DualStampRate @Def: Stamping rate of dual model stamping machine (letters per minute) @Shape: [] 
DualStampRate = data['DualStampRate']
# @Parameter DualGlueUsage @Def: Glue usage rate of dual model stamping machine (units per minute) @Shape: [] 
DualGlueUsage = data['DualGlueUsage']
# @Parameter SingleStampRate @Def: Stamping rate of single model stamping machine (letters per minute) @Shape: [] 
SingleStampRate = data['SingleStampRate']
# @Parameter SingleGlueUsage @Def: Glue usage rate of single model stamping machine (units per minute) @Shape: [] 
SingleGlueUsage = data['SingleGlueUsage']
# @Parameter MinTotalLetters @Def: Minimum total letters to be stamped per minute @Shape: [] 
MinTotalLetters = data['MinTotalLetters']
# @Parameter MaxGlueUsage @Def: Maximum total glue usage per minute @Shape: [] 
MaxGlueUsage = data['MaxGlueUsage']

# Variables 
# @Variable SingleStampMachines @Def: The number of single model stamping machines @Shape: ['Integer'] 
SingleStampMachines = model.addVar(vtype=GRB.INTEGER, name="SingleStampMachines")
# @Variable DualStampMachines @Def: The number of dual model stamping machines @Shape: ['Integer'] 
DualStampMachines = model.addVar(vtype=GRB.INTEGER, name="DualStampMachines")

# Constraints 
# @Constraint Constr_1 @Def: The number of single model stamping machines must exceed the number of dual model stamping machines.
model.addConstr(SingleStampMachines >= DualStampMachines + 1)
# @Constraint Constr_2 @Def: The post office must stamp at least MinTotalLetters letters per minute.
model.addConstr(SingleStampRate * SingleStampMachines + DualStampRate * DualStampMachines >= MinTotalLetters)
# @Constraint Constr_3 @Def: The post office must use at most MaxGlueUsage units of glue per minute.
model.addConstr(SingleGlueUsage * SingleStampMachines + DualGlueUsage * DualStampMachines <= MaxGlueUsage)

# Objective 
# @Objective Objective @Def: Minimize the total number of stamping machines purchased.
model.setObjective(SingleStampMachines + DualStampMachines, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SingleStampMachines'] = SingleStampMachines.x
variables['DualStampMachines'] = DualStampMachines.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
