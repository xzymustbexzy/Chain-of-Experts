# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A repairman repairs WashingMachines and Freezers. Each WashingMachine requires
InspectionTimeWashingMachine minutes for inspection and FixingTimeWashingMachine
minutes for fixing, while each Freezer requires InspectionTimeFreezer minutes
for inspection and FixingTimeFreezer minutes for fixing. The total available
InspectionTime is TotalInspectionTime minutes and the total available schedule
time is TotalScheduleTime minutes. Repairing each WashingMachine yields
EarningsPerWashingMachine and each Freezer yields EarningsPerFreezer. Determine
the number of WashingMachines and Freezers to repair to maximize total earnings.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/205/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter InspectionTimeWashingMachine @Def: Time required to inspect one washing machine @Shape: [] 
InspectionTimeWashingMachine = data['InspectionTimeWashingMachine']
# @Parameter FixingTimeWashingMachine @Def: Time required to fix one washing machine @Shape: [] 
FixingTimeWashingMachine = data['FixingTimeWashingMachine']
# @Parameter InspectionTimeFreezer @Def: Time required to inspect one freezer @Shape: [] 
InspectionTimeFreezer = data['InspectionTimeFreezer']
# @Parameter FixingTimeFreezer @Def: Time required to fix one freezer @Shape: [] 
FixingTimeFreezer = data['FixingTimeFreezer']
# @Parameter TotalInspectionTime @Def: Total available time for inspections @Shape: [] 
TotalInspectionTime = data['TotalInspectionTime']
# @Parameter TotalScheduleTime @Def: Total available schedule time @Shape: [] 
TotalScheduleTime = data['TotalScheduleTime']
# @Parameter EarningsPerWashingMachine @Def: Earnings per washing machine repaired @Shape: [] 
EarningsPerWashingMachine = data['EarningsPerWashingMachine']
# @Parameter EarningsPerFreezer @Def: Earnings per freezer repaired @Shape: [] 
EarningsPerFreezer = data['EarningsPerFreezer']

# Variables 
# @Variable WashingMachinesInspected @Def: The number of washing machines to inspect @Shape: [] 
WashingMachinesInspected = model.addVar(vtype=GRB.CONTINUOUS, name="WashingMachinesInspected")
# @Variable FreezersInspected @Def: The number of freezers to inspect @Shape: [] 
FreezersInspected = model.addVar(vtype=GRB.CONTINUOUS, name="FreezersInspected")
# @Variable WashingMachinesRepaired @Def: The number of washing machines to repair @Shape: [] 
WashingMachinesRepaired = model.addVar(vtype=GRB.INTEGER, name="WashingMachinesRepaired")
# @Variable FreezersRepaired @Def: The number of freezers to repair @Shape: [] 
FreezersRepaired = model.addVar(vtype=GRB.CONTINUOUS, name="FreezersRepaired")

# Constraints 
# @Constraint Constr_1 @Def: The total inspection time for washing machines and freezers must not exceed the available TotalInspectionTime.
model.addConstr(InspectionTimeWashingMachine * WashingMachinesInspected + InspectionTimeFreezer * FreezersInspected <= TotalInspectionTime)
# @Constraint Constr_2 @Def: The total schedule time for repairing washing machines and freezers must not exceed the available TotalScheduleTime.
model.addConstr(FixingTimeWashingMachine * WashingMachinesRepaired + FixingTimeFreezer * FreezersRepaired <= TotalScheduleTime)

# Objective 
# @Objective Objective @Def: Total earnings is the sum of earnings from washing machines and freezers. The objective is to maximize the total earnings.
model.setObjective(EarningsPerWashingMachine * WashingMachinesRepaired + EarningsPerFreezer * FreezersRepaired, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['WashingMachinesInspected'] = WashingMachinesInspected.x
variables['FreezersInspected'] = FreezersInspected.x
variables['WashingMachinesRepaired'] = WashingMachinesRepaired.x
variables['FreezersRepaired'] = FreezersRepaired.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
