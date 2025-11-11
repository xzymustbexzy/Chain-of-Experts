# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A farmer has TotalLand acres to cultivate turnips and pumpkins. Turnips require
WateringTimeTurnips minutes of watering and PesticideCostTurnips dollars worth
of pesticide per acre. Pumpkins require WateringTimePumpkins minutes of watering
and PesticideCostPumpkins dollars worth of pesticide per acre. The farmer has
TotalWateringTime minutes available for watering and TotalPesticideBudget
dollars available to spend on pesticide. The revenue per acre of turnips is
RevenueTurnips and the revenue per acre of pumpkins is RevenuePumpkins.
Determine the number of acres of each crop to maximize the farmer's total
revenue.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/39/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalLand @Def: Total land available for cultivation @Shape: [] 
TotalLand = data['TotalLand']
# @Parameter WateringTimeTurnips @Def: Watering time required per acre of turnips @Shape: [] 
WateringTimeTurnips = data['WateringTimeTurnips']
# @Parameter PesticideCostTurnips @Def: Pesticide cost per acre of turnips @Shape: [] 
PesticideCostTurnips = data['PesticideCostTurnips']
# @Parameter WateringTimePumpkins @Def: Watering time required per acre of pumpkins @Shape: [] 
WateringTimePumpkins = data['WateringTimePumpkins']
# @Parameter PesticideCostPumpkins @Def: Pesticide cost per acre of pumpkins @Shape: [] 
PesticideCostPumpkins = data['PesticideCostPumpkins']
# @Parameter TotalWateringTime @Def: Total available watering time @Shape: [] 
TotalWateringTime = data['TotalWateringTime']
# @Parameter TotalPesticideBudget @Def: Total pesticide budget @Shape: [] 
TotalPesticideBudget = data['TotalPesticideBudget']
# @Parameter RevenueTurnips @Def: Revenue per acre of turnips @Shape: [] 
RevenueTurnips = data['RevenueTurnips']
# @Parameter RevenuePumpkins @Def: Revenue per acre of pumpkins @Shape: [] 
RevenuePumpkins = data['RevenuePumpkins']

# Variables 
# @Variable LandTurnips @Def: The land allocated to turnips @Shape: [] 
LandTurnips = model.addVar(vtype=GRB.CONTINUOUS, name="LandTurnips")
# @Variable LandPumpkins @Def: The land allocated to pumpkins @Shape: [] 
LandPumpkins = model.addVar(vtype=GRB.CONTINUOUS, name="LandPumpkins")

# Constraints 
# @Constraint Constr_1 @Def: The total land allocated to turnips and pumpkins cannot exceed TotalLand.
model.addConstr(LandTurnips + LandPumpkins <= TotalLand)
# @Constraint Constr_2 @Def: The total watering time required for turnips and pumpkins cannot exceed TotalWateringTime.
model.addConstr(WateringTimeTurnips * LandTurnips + WateringTimePumpkins * LandPumpkins <= TotalWateringTime)
# @Constraint Constr_3 @Def: The total pesticide cost for turnips and pumpkins cannot exceed TotalPesticideBudget.
model.addConstr(PesticideCostTurnips * LandTurnips + PesticideCostPumpkins * LandPumpkins <= TotalPesticideBudget)

# Objective 
# @Objective Objective @Def: Total revenue is the sum of the revenue per acre of turnips and pumpkins. The objective is to maximize the total revenue.
model.setObjective(RevenueTurnips * LandTurnips + RevenuePumpkins * LandPumpkins, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['LandTurnips'] = LandTurnips.x
variables['LandPumpkins'] = LandPumpkins.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
