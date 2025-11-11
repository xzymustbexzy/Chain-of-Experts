# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A pharmacy has TotalMorphine amount of morphine to produce painkiller and
sleeping pills. Each painkiller pill requires MorphinePerPainkiller of morphine
and DigestiveMedicinePerPainkiller units of digestive medicine. Each sleeping
pill requires MorphinePerSleepingPill of morphine and
DigestiveMedicinePerSleepingPill units of digestive medicine. The pharmacy must
produce at least MinPainkillerPills painkiller pills. Additionally, at least
MinSleepingPillsProportion proportion of the total pills produced should be
sleeping pills. The objective is to determine the number of each type of pill to
produce in order to minimize the total amount of digestive medicine used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/113/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalMorphine @Def: Total amount of morphine available @Shape: [] 
TotalMorphine = data['TotalMorphine']
# @Parameter MorphinePerPainkiller @Def: Amount of morphine required for one painkiller pill @Shape: [] 
MorphinePerPainkiller = data['MorphinePerPainkiller']
# @Parameter MorphinePerSleepingPill @Def: Amount of morphine required for one sleeping pill @Shape: [] 
MorphinePerSleepingPill = data['MorphinePerSleepingPill']
# @Parameter DigestiveMedicinePerPainkiller @Def: Amount of digestive medicine required for one painkiller pill @Shape: [] 
DigestiveMedicinePerPainkiller = data['DigestiveMedicinePerPainkiller']
# @Parameter DigestiveMedicinePerSleepingPill @Def: Amount of digestive medicine required for one sleeping pill @Shape: [] 
DigestiveMedicinePerSleepingPill = data['DigestiveMedicinePerSleepingPill']
# @Parameter MinPainkillerPills @Def: Minimum number of painkiller pills to be produced @Shape: [] 
MinPainkillerPills = data['MinPainkillerPills']
# @Parameter MinSleepingPillsProportion @Def: Minimum proportion of pills that should be sleeping pills @Shape: [] 
MinSleepingPillsProportion = data['MinSleepingPillsProportion']

# Variables 
# @Variable PainkillerPills @Def: The number of painkiller pills to be produced @Shape: [] 
PainkillerPills = model.addVar(vtype=GRB.INTEGER, lb=MinPainkillerPills, name="PainkillerPills")
# @Variable SleepingPills @Def: The number of sleeping pills to be produced @Shape: [] 
SleepingPills = model.addVar(vtype=GRB.CONTINUOUS, name="SleepingPills")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of morphine used for producing painkiller and sleeping pills does not exceed TotalMorphine.
model.addConstr(MorphinePerPainkiller * PainkillerPills + MorphinePerSleepingPill * SleepingPills <= TotalMorphine)
# @Constraint Constr_2 @Def: At least MinPainkillerPills painkiller pills must be produced.
model.addConstr(PainkillerPills >= MinPainkillerPills)
# @Constraint Constr_3 @Def: At least MinSleepingPillsProportion proportion of the total pills produced must be sleeping pills.
model.addConstr(SleepingPills >= MinSleepingPillsProportion * (PainkillerPills + SleepingPills))

# Objective 
# @Objective Objective @Def: The total amount of digestive medicine used is the sum of DigestiveMedicinePerPainkiller times the number of painkiller pills and DigestiveMedicinePerSleepingPill times the number of sleeping pills. The objective is to minimize the total amount of digestive medicine used.
model.setObjective(DigestiveMedicinePerPainkiller * PainkillerPills + DigestiveMedicinePerSleepingPill * SleepingPills, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['PainkillerPills'] = PainkillerPills.x
variables['SleepingPills'] = SleepingPills.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
