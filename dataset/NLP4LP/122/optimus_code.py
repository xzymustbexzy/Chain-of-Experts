# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A pharmaceutical company has TotalPainkillerUnits units of painkiller medicine
and produces daytime and nighttime pills. Each daytime pill contains
PainkillerPerDayPill units of painkiller and SleepPerDayPill units of sleep
medicine. Each nighttime pill contains PainkillerPerNightPill units of
painkiller and SleepPerNightPill units of sleep medicine. At least
MinDayPillPercentage of the total pills must be daytime pills, and at least
MinNightPills nighttime pills must be produced. The objective is to determine
the number of daytime and nighttime pills to minimize the total sleep medicine
required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/123/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalPainkillerUnits @Def: Total number of painkiller medicine units available @Shape: [] 
TotalPainkillerUnits = data['TotalPainkillerUnits']
# @Parameter PainkillerPerDayPill @Def: Units of painkiller medicine per daytime pill @Shape: [] 
PainkillerPerDayPill = data['PainkillerPerDayPill']
# @Parameter SleepPerDayPill @Def: Units of sleep medicine per daytime pill @Shape: [] 
SleepPerDayPill = data['SleepPerDayPill']
# @Parameter PainkillerPerNightPill @Def: Units of painkiller medicine per nighttime pill @Shape: [] 
PainkillerPerNightPill = data['PainkillerPerNightPill']
# @Parameter SleepPerNightPill @Def: Units of sleep medicine per nighttime pill @Shape: [] 
SleepPerNightPill = data['SleepPerNightPill']
# @Parameter MinDayPillPercentage @Def: Minimum percentage of pills that must be daytime pills @Shape: [] 
MinDayPillPercentage = data['MinDayPillPercentage']
# @Parameter MinNightPills @Def: Minimum number of nighttime pills to be made @Shape: [] 
MinNightPills = data['MinNightPills']

# Variables 
# @Variable NumberDaytimePills @Def: The number of daytime pills @Shape: [] 
NumberDaytimePills = model.addVar(vtype=GRB.CONTINUOUS, name="NumberDaytimePills")
# @Variable NumberNighttimePills @Def: The number of nighttime pills @Shape: [] 
NumberNighttimePills = model.addVar(vtype=GRB.CONTINUOUS, lb=MinNightPills, name="NumberNighttimePills")

# Constraints 
# @Constraint Constr_1 @Def: The total painkiller used in daytime and nighttime pills cannot exceed TotalPainkillerUnits.
model.addConstr(PainkillerPerDayPill * NumberDaytimePills + PainkillerPerNightPill * NumberNighttimePills <= TotalPainkillerUnits)
# @Constraint Constr_2 @Def: At least MinDayPillPercentage percentage of the total pills must be daytime pills.
model.addConstr(NumberDaytimePills >= MinDayPillPercentage * (NumberDaytimePills + NumberNighttimePills))
# @Constraint Constr_3 @Def: At least MinNightPills nighttime pills must be produced.
model.addConstr(NumberNighttimePills >= MinNightPills)

# Objective 
# @Objective Objective @Def: The total sleep medicine used is the sum of SleepPerDayPill units per daytime pill and SleepPerNightPill units per nighttime pill. The objective is to minimize the total sleep medicine required.
model.setObjective(SleepPerDayPill * NumberDaytimePills + SleepPerNightPill * NumberNighttimePills, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberDaytimePills'] = NumberDaytimePills.x
variables['NumberNighttimePills'] = NumberNighttimePills.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
