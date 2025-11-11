# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A cleaning company uses a cleansing chemical and an odor-removing chemical to
clean a house. Each unit of the cleansing chemical requires
CleansingChemicalTime to be effective, while each unit of the odor-removing
chemical requires OdorRemovingChemicalTime to be effective. The company must use
at least MinCleansingUnits of the cleansing chemical. The total number of
chemical units used per house cannot exceed MaxTotalUnits. Additionally, the
number of cleansing chemical units used cannot exceed MaxCleansingToOdorRatio
times the number of odor-removing chemical units used. Determine the number of
units of each chemical to minimize the total time it takes for a house to be
cleaned.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/95/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CleansingChemicalTime @Def: Time it takes for one unit of cleansing chemical to be effective @Shape: [] 
CleansingChemicalTime = data['CleansingChemicalTime']
# @Parameter OdorRemovingChemicalTime @Def: Time it takes for one unit of odor-removing chemical to be effective @Shape: [] 
OdorRemovingChemicalTime = data['OdorRemovingChemicalTime']
# @Parameter MinCleansingUnits @Def: Minimum number of units of cleansing chemical to be used per house @Shape: [] 
MinCleansingUnits = data['MinCleansingUnits']
# @Parameter MaxTotalUnits @Def: Maximum total number of chemical units used per house @Shape: [] 
MaxTotalUnits = data['MaxTotalUnits']
# @Parameter MaxCleansingToOdorRatio @Def: Maximum ratio of cleansing chemical units to odor-removing chemical units @Shape: [] 
MaxCleansingToOdorRatio = data['MaxCleansingToOdorRatio']

# Variables 
# @Variable CleansingChemicalUnits @Def: The number of units of cleansing chemical used per house @Shape: [] 
CleansingChemicalUnits = model.addVar(vtype=GRB.CONTINUOUS, lb=MinCleansingUnits, ub=MaxTotalUnits, name="CleansingChemicalUnits")
# @Variable OdorRemovingChemicalUnits @Def: The number of units of odor-removing chemical used per house @Shape: [] 
OdorRemovingChemicalUnits = model.addVar(vtype=GRB.CONTINUOUS, name="OdorRemovingChemicalUnits")

# Constraints 
# @Constraint Constr_1 @Def: The company must use at least MinCleansingUnits of the cleansing chemical per house.
model.addConstr(CleansingChemicalUnits >= MinCleansingUnits)
# @Constraint Constr_2 @Def: The total number of chemical units used per house cannot exceed MaxTotalUnits.
model.addConstr(CleansingChemicalUnits + OdorRemovingChemicalUnits <= MaxTotalUnits)
# @Constraint Constr_3 @Def: The number of cleansing chemical units used cannot exceed MaxCleansingToOdorRatio times the number of odor-removing chemical units used.
model.addConstr(CleansingChemicalUnits <= MaxCleansingToOdorRatio * OdorRemovingChemicalUnits)

# Objective 
# @Objective Objective @Def: Minimize the total cleaning time, which is the sum of CleansingChemicalTime multiplied by the number of cleansing chemical units and OdorRemovingChemicalTime multiplied by the number of odor-removing chemical units.
model.setObjective(CleansingChemicalTime * CleansingChemicalUnits + OdorRemovingChemicalTime * OdorRemovingChemicalUnits, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['CleansingChemicalUnits'] = CleansingChemicalUnits.x
variables['OdorRemovingChemicalUnits'] = OdorRemovingChemicalUnits.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
