# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A student consumes calcium and vitamin D pills sequentially. Each calcium pill
requires TimeToEffectCalcium time to become effective, and each vitamin D pill
requires TimeToEffectVitaminD time to become effective. Over a month, the
student must ingest at least MinTotalPills pills in total, with a minimum of
MinVitaminDPills being vitamin D pills. Additionally, the number of calcium
pills taken must exceed the number of vitamin D pills. The objective is to
minimize the total time for the medication to become effective.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/220/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimeToEffectCalcium @Def: Time it takes for a calcium pill to be effective @Shape: [] 
TimeToEffectCalcium = data['TimeToEffectCalcium']
# @Parameter TimeToEffectVitaminD @Def: Time it takes for a vitamin D pill to be effective @Shape: [] 
TimeToEffectVitaminD = data['TimeToEffectVitaminD']
# @Parameter MinTotalPills @Def: Minimum total number of pills to be taken in a month @Shape: [] 
MinTotalPills = data['MinTotalPills']
# @Parameter MinVitaminDPills @Def: Minimum number of vitamin D pills to be taken in a month @Shape: [] 
MinVitaminDPills = data['MinVitaminDPills']

# Variables 
# @Variable NumberCalciumPills @Def: The number of Calcium pills taken in a month @Shape: ['Integer'] 
NumberCalciumPills = model.addVar(vtype=GRB.INTEGER, name="NumberCalciumPills")
# @Variable NumberVitaminDPills @Def: The number of Vitamin D pills taken in a month @Shape: ['Integer'] 
NumberVitaminDPills = model.addVar(vtype=GRB.INTEGER, lb=MinVitaminDPills, name="NumberVitaminDPills")
# @Variable TotalTime @Def: The total time for the medications to become effective. @Shape: ['Continuous'] 
TotalTime = model.addVar(vtype=GRB.CONTINUOUS, name="TotalTime")
# @Variable IsCalciumTaken @Def: Binary variable indicating whether any Calcium pills are taken. @Shape: ['Binary'] 
IsCalciumTaken = model.addVar(vtype=GRB.BINARY, name="IsCalciumTaken")
# @Variable IsVitaminDTaken @Def: Binary variable indicating whether any Vitamin D pills are taken. @Shape: ['Binary'] 
IsVitaminDTaken = model.addVar(vtype=GRB.BINARY, name="IsVitaminDTaken")

# Constraints 
# @Constraint Constr_1 @Def: The total number of pills ingested in a month must be at least MinTotalPills.
model.addConstr(NumberCalciumPills + NumberVitaminDPills >= MinTotalPills)
# @Constraint Constr_2 @Def: At least MinVitaminDPills of the pills ingested in a month must be vitamin D pills.
model.addConstr(NumberVitaminDPills >= MinVitaminDPills)
# @Constraint Constr_3 @Def: The number of calcium pills taken must exceed the number of vitamin D pills.
model.addConstr(NumberCalciumPills >= NumberVitaminDPills + 1)

# Objective 
# @Objective Objective @Def: Minimize the total time for the medications to become effective.
model.setObjective(TotalTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberCalciumPills'] = NumberCalciumPills.x
variables['NumberVitaminDPills'] = NumberVitaminDPills.x
variables['TotalTime'] = TotalTime.x
variables['IsCalciumTaken'] = IsCalciumTaken.x
variables['IsVitaminDTaken'] = IsVitaminDTaken.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
