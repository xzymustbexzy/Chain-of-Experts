# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A clinic administers two types of vaccines, Pill and Shot. Administering a Pill
vaccine takes TimePerPill minutes, while administering a Shot vaccine takes
TimePerShot minutes. The clinic must administer at least ShotToPillRatio times
as many Shots as Pills, and at least MinPills Pills. Given that the clinic
operates for TotalOperatingTime minutes, the goal is to maximize the number of
patients vaccinated.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/138/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimePerPill @Def: Time required to administer a pill vaccine @Shape: [] 
TimePerPill = data['TimePerPill']
# @Parameter TimePerShot @Def: Time required to administer a shot vaccine @Shape: [] 
TimePerShot = data['TimePerShot']
# @Parameter ShotToPillRatio @Def: Minimum ratio of shots to pills @Shape: [] 
ShotToPillRatio = data['ShotToPillRatio']
# @Parameter MinPills @Def: Minimum number of pill vaccines to administer @Shape: [] 
MinPills = data['MinPills']
# @Parameter TotalOperatingTime @Def: Total operating time of the clinic in minutes @Shape: [] 
TotalOperatingTime = data['TotalOperatingTime']

# Variables 
# @Variable NumberOfPills @Def: The number of pill vaccines to administer @Shape: [] 
NumberOfPills = model.addVar(vtype=GRB.INTEGER, lb=MinPills, name="NumberOfPills")
# @Variable NumberOfShots @Def: The number of shot vaccines to administer @Shape: [] 
NumberOfShots = model.addVar(vtype=GRB.INTEGER, name="NumberOfShots")

# Constraints 
# @Constraint Constr_1 @Def: The total time required to administer Pill vaccines and Shot vaccines must not exceed TotalOperatingTime minutes.
model.addConstr(TimePerPill * NumberOfPills + TimePerShot * NumberOfShots <= TotalOperatingTime)
# @Constraint Constr_2 @Def: The number of Shot vaccines administered must be at least ShotToPillRatio times the number of Pill vaccines administered.
model.addConstr(NumberOfShots >= ShotToPillRatio * NumberOfPills)
# @Constraint Constr_3 @Def: At least MinPills Pill vaccines must be administered.
model.addConstr(NumberOfPills >= MinPills, 'AtLeastMinPills')

# Objective 
# @Objective Objective @Def: Maximize the total number of patients vaccinated, which is the sum of Pill and Shot vaccines administered.
model.setObjective(NumberOfPills + NumberOfShots, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfPills'] = NumberOfPills.x
variables['NumberOfShots'] = NumberOfShots.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
