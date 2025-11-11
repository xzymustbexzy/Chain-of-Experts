# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Determine the number of fertilizer units and seed units to minimize the total
time for the lawn to be ready, where the total time is the maximum of the
fertilizer units multiplied by TimePerFertilizer and the seed units multiplied
by TimePerSeeds. The combined units of fertilizer and seeds must not exceed
MaxTotalUnits, the fertilizer units must be at least MinFertilizer, and the
fertilizer units must not exceed MaxFertilizerRatio times the seed units.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/105/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimePerFertilizer @Def: Time one unit of fertilizer takes to be effective @Shape: [] 
TimePerFertilizer = data['TimePerFertilizer']
# @Parameter TimePerSeeds @Def: Time one unit of seeds takes to be effective @Shape: [] 
TimePerSeeds = data['TimePerSeeds']
# @Parameter MaxTotalUnits @Def: Maximum total units of fertilizer and seeds combined @Shape: [] 
MaxTotalUnits = data['MaxTotalUnits']
# @Parameter MinFertilizer @Def: Minimum units of fertilizer to be added @Shape: [] 
MinFertilizer = data['MinFertilizer']
# @Parameter MaxFertilizerRatio @Def: Maximum ratio of fertilizer to seeds @Shape: [] 
MaxFertilizerRatio = data['MaxFertilizerRatio']

# Variables 
# @Variable FertilizerUnits @Def: The number of units of fertilizer @Shape: [] 
FertilizerUnits = model.addVar(vtype=GRB.CONTINUOUS, lb=MinFertilizer, name="FertilizerUnits")
# @Variable SeedsUnits @Def: The number of units of seeds @Shape: [] 
SeedsUnits = model.addVar(vtype=GRB.CONTINUOUS, name="SeedsUnits")
# @Variable TotalTime @Def: The total time for the lawn to be ready @Shape: [] 
TotalTime = model.addVar(vtype=GRB.CONTINUOUS, name="TotalTime")

# Constraints 
# @Constraint Constr_1 @Def: The combined units of fertilizer and seeds must not exceed MaxTotalUnits.
model.addConstr(FertilizerUnits + SeedsUnits <= MaxTotalUnits)
# @Constraint Constr_2 @Def: The fertilizer units must be at least MinFertilizer.
model.addConstr(FertilizerUnits >= MinFertilizer)
# @Constraint Constr_3 @Def: The fertilizer units must not exceed MaxFertilizerRatio times the seed units.
model.addConstr(FertilizerUnits <= MaxFertilizerRatio * SeedsUnits)

# Objective 
# @Objective Objective @Def: The total time is the maximum of (fertilizer units multiplied by TimePerFertilizer) and (seed units multiplied by TimePerSeeds). The objective is to minimize the total time for the lawn to be ready.
model.setObjective(TotalTime, GRB.MINIMIZE)
model.addConstr(TotalTime >= FertilizerUnits * TimePerFertilizer, "Time_Fertilizer")
model.addConstr(TotalTime >= SeedsUnits * TimePerSeeds, "Time_Seeds")

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['FertilizerUnits'] = FertilizerUnits.x
variables['SeedsUnits'] = SeedsUnits.x
variables['TotalTime'] = TotalTime.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
