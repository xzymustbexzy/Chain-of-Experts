# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A science store produces NumBoxTypes different box types. Each box type requires
MetalPerBoxType units of metal and AcidPerBoxType units of acid to produce. Each
box type generates FoamPerBoxType units of foam and emits HeatPerBoxType units of heat. The store has MetalAvailable units of metal and AcidAvailable units of 
acid available. The total heat emitted by all produced boxes must not exceed
MaxHeat units. The objective is to determine the number of each box type to
produce in order to maximize the total amount of foam produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/112/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter MetalAvailable @Def: Total units of metal available @Shape: [] 
MetalAvailable = data['MetalAvailable']
# @Parameter AcidAvailable @Def: Total units of acid available @Shape: [] 
AcidAvailable = data['AcidAvailable']
# @Parameter MaxHeat @Def: Maximum units of heat that can be given off @Shape: [] 
MaxHeat = data['MaxHeat']
# @Parameter NumBoxTypes @Def: Number of different box types @Shape: [] 
NumBoxTypes = data['NumBoxTypes']
# @Parameter MetalPerBoxType @Def: Units of metal required per box type @Shape: ['NumBoxTypes'] 
MetalPerBoxType = data['MetalPerBoxType']
# @Parameter AcidPerBoxType @Def: Units of acid required per box type @Shape: ['NumBoxTypes'] 
AcidPerBoxType = data['AcidPerBoxType']
# @Parameter FoamPerBoxType @Def: Units of foam produced per box type @Shape: ['NumBoxTypes'] 
FoamPerBoxType = data['FoamPerBoxType']
# @Parameter HeatPerBoxType @Def: Units of heat given off per box type @Shape: ['NumBoxTypes'] 
HeatPerBoxType = data['HeatPerBoxType']
    
# Variables 
# @Variable BoxesProduced @Def: The number of boxes produced for each box type @Shape: ['NumBoxTypes'] 
BoxesProduced = model.addVars(NumBoxTypes, vtype=GRB.CONTINUOUS, name="BoxesProduced")
    
# Constraints 
# @Constraint Constr_1 @Def: The total metal used for production cannot exceed MetalAvailable units.
model.addConstr(quicksum(MetalPerBoxType[i] * BoxesProduced[i] for i in range(NumBoxTypes)) <= MetalAvailable)
# @Constraint Constr_2 @Def: The total acid used for production cannot exceed AcidAvailable units.
model.addConstr(quicksum(AcidPerBoxType[i] * BoxesProduced[i] for i in range(NumBoxTypes)) <= AcidAvailable)
# @Constraint Constr_3 @Def: The total heat emitted by all produced boxes must not exceed MaxHeat units.
model.addConstr(quicksum(HeatPerBoxType[i] * BoxesProduced[i] for i in range(NumBoxTypes)) <= MaxHeat)
    
# Objective 
# @Objective Objective @Def: Maximize the total foam produced, which is the sum of FoamPerBoxType units multiplied by the number of each box type produced.
model.setObjective(quicksum(FoamPerBoxType[i] * BoxesProduced[i] for i in range(NumBoxTypes)), GRB.MAXIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['BoxesProduced'] = [BoxesProduced[i].x for i in range(NumBoxTypes)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
