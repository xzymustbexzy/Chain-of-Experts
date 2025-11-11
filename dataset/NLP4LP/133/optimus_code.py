# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Two chemicals, Chlorine and WaterSoftener, need to be added to a pool. Each unit
of Chlorine becomes effective after ChlorineEffectivenessTime minutes, and each
unit of WaterSoftener becomes effective after WaterSoftenerEffectivenessTime
minutes. The amount of Chlorine must not exceed MaxChlorineToWaterSoftenerRatio
times the amount of WaterSoftener. At least MinChlorineUnits of Chlorine must be
added, and the total number of chemical units added must equal
TotalChemicalUnits. The objective is to determine the number of units of
Chlorine and WaterSoftener to add in order to minimize the total time for the
pool to be ready.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/134/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ChlorineEffectivenessTime @Def: The time in minutes for one unit of chlorine to become effective @Shape: [] 
ChlorineEffectivenessTime = data['ChlorineEffectivenessTime']
# @Parameter WaterSoftenerEffectivenessTime @Def: The time in minutes for one unit of water softener to become effective @Shape: [] 
WaterSoftenerEffectivenessTime = data['WaterSoftenerEffectivenessTime']
# @Parameter MaxChlorineToWaterSoftenerRatio @Def: The maximum allowed ratio of chlorine to water softener in the pool @Shape: [] 
MaxChlorineToWaterSoftenerRatio = data['MaxChlorineToWaterSoftenerRatio']
# @Parameter MinChlorineUnits @Def: The minimum required units of chlorine to be added to the pool @Shape: [] 
MinChlorineUnits = data['MinChlorineUnits']
# @Parameter TotalChemicalUnits @Def: The total number of chemical units to be added to the pool @Shape: [] 
TotalChemicalUnits = data['TotalChemicalUnits']

# Variables 
# @Variable ChlorineAmount @Def: The amount of Chlorine added to the pool @Shape: [] 
ChlorineAmount = model.addVar(vtype=GRB.CONTINUOUS, name="ChlorineAmount")
# @Variable WaterSoftenerAmount @Def: The amount of Water Softener added to the pool @Shape: [] 
WaterSoftenerAmount = model.addVar(vtype=GRB.CONTINUOUS, name="WaterSoftenerAmount")
# @Variable ChlorineUnits @Def: The number of Chlorine units added to the pool @Shape: [] 
ChlorineUnits = model.addVar(vtype=GRB.INTEGER, name="ChlorineUnits")
# @Variable WaterSoftenerUnits @Def: The number of Water Softener units added to the pool @Shape: [] 
WaterSoftenerUnits = model.addVar(vtype=GRB.INTEGER, name="WaterSoftenerUnits")
# @Variable TotalTime @Def: The total time for the pool to be ready @Shape: [] 
TotalTime = model.addVar(vtype=GRB.CONTINUOUS, name="TotalTime")

# Constraints 
# @Constraint Constr_1 @Def: The amount of Chlorine must not exceed MaxChlorineToWaterSoftenerRatio times the amount of WaterSoftener.
model.addConstr(ChlorineAmount <= MaxChlorineToWaterSoftenerRatio * WaterSoftenerAmount)
# @Constraint Constr_2 @Def: At least MinChlorineUnits of Chlorine must be added.
model.addConstr(ChlorineAmount >= MinChlorineUnits)
# @Constraint Constr_3 @Def: The total number of chemical units added must equal TotalChemicalUnits.
model.addConstr(ChlorineUnits + WaterSoftenerUnits == TotalChemicalUnits)

# Objective 
# @Objective Objective @Def: Determine the number of units of Chlorine and WaterSoftener to add in order to minimize the total time for the pool to be ready.
model.setObjective(TotalTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ChlorineAmount'] = ChlorineAmount.x
variables['WaterSoftenerAmount'] = WaterSoftenerAmount.x
variables['ChlorineUnits'] = ChlorineUnits.x
variables['WaterSoftenerUnits'] = WaterSoftenerUnits.x
variables['TotalTime'] = TotalTime.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
