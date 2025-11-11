# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A factory utilizes high intensity drills and low intensity drills. Each high
intensity drill processes GemsPerHigh gems per day and requires WaterPerHigh
units of water daily. Each low intensity drill processes GemsPerLow gems per day
and requires WaterPerLow units of water daily. The factory must process a total
of TotalGems gems each day and has AvailableWater units of water available for
dissipation. No more than MaxHighFraction of the total drills can be high
intensity to control noise pollution, and at least MinLowDrills low intensity
drills must be employed. The objective is to minimize the total number of drills
used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/41/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GemsPerHigh @Def: Number of gems processed per day by a high intensity drill. @Shape: [] 
GemsPerHigh = data['GemsPerHigh']
# @Parameter WaterPerHigh @Def: Units of water required per day to dissipate heat by a high intensity drill. @Shape: [] 
WaterPerHigh = data['WaterPerHigh']
# @Parameter GemsPerLow @Def: Number of gems processed per day by a low intensity drill. @Shape: [] 
GemsPerLow = data['GemsPerLow']
# @Parameter WaterPerLow @Def: Units of water required per day to dissipate heat by a low intensity drill. @Shape: [] 
WaterPerLow = data['WaterPerLow']
# @Parameter TotalGems @Def: Total number of gems that must be processed per day by the factory. @Shape: [] 
TotalGems = data['TotalGems']
# @Parameter AvailableWater @Def: Total units of water available per day for dissipating heat. @Shape: [] 
AvailableWater = data['AvailableWater']
# @Parameter MaxHighFraction @Def: Maximum fraction of drills that can be high intensity to limit noise pollution. @Shape: [] 
MaxHighFraction = data['MaxHighFraction']
# @Parameter MinLowDrills @Def: Minimum number of low intensity drills that must be used. @Shape: [] 
MinLowDrills = data['MinLowDrills']

# Variables 
# @Variable HighDrills @Def: The number of high intensity drills used @Shape: ['Integer'] 
HighDrills = model.addVar(vtype=GRB.INTEGER, name="HighDrills")
# @Variable LowDrills @Def: The number of low intensity drills used @Shape: ['Integer'] 
LowDrills = model.addVar(vtype=GRB.INTEGER, name="LowDrills")

# Constraints 
# @Constraint Constr_1 @Def: The total number of gems processed per day by high and low intensity drills must equal TotalGems.
model.addConstr(GemsPerHigh * HighDrills + GemsPerLow * LowDrills == TotalGems)
# @Constraint Constr_2 @Def: The total water usage by all drills must not exceed AvailableWater units per day.
model.addConstr(WaterPerHigh * HighDrills + WaterPerLow * LowDrills <= AvailableWater)
# @Constraint Constr_3 @Def: No more than MaxHighFraction of the total drills can be high intensity to limit noise pollution.
model.addConstr((1 - MaxHighFraction) * HighDrills <= MaxHighFraction * LowDrills)
# @Constraint Constr_4 @Def: At least MinLowDrills low intensity drills must be employed.
model.addConstr(LowDrills >= MinLowDrills)

# Objective 
# @Objective Objective @Def: Minimize the total number of drills used.
model.setObjective(HighDrills + LowDrills, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['HighDrills'] = HighDrills.x
variables['LowDrills'] = LowDrills.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
